#!/usr/bin/env python3
"""
VoiceSnap - Ultra-fast local voice-to-text with Whisper
Hotkey: Ctrl+Shift+Space (customizable)
"""

import os
import sys
import tempfile
import sounddevice as sd
import soundfile as sf
import numpy as np
import pyperclip
import whisper
from pynput import keyboard
from pynput.keyboard import Key, Controller

# Configuration
HOTKEY = {keyboard.Key.ctrl, keyboard.Key.shift, keyboard.Key.space}
SAMPLE_RATE = 16000  # Whisper expects 16kHz
MAX_DURATION = 30  # secondes max d'enregistrement

# État global
current_keys = set()
recording = False
audio_data = []
keyboard_controller = Controller()


def on_press(key):
    """Détecte la combinaison de touches"""
    global current_keys, recording
    
    current_keys.add(key)
    
    # Si hotkey détectée et pas déjà en train d'enregistrer
    if HOTKEY.issubset(current_keys) and not recording:
        print("\n🎤 Enregistrement démarré... (relâchez les touches pour arrêter)")
        start_recording()


def on_release(key):
    """Arrête l'enregistrement quand les touches sont relâchées"""
    global current_keys, recording
    
    if key in current_keys:
        current_keys.remove(key)
    
    # Si on était en train d'enregistrer et que les touches hotkey sont relâchées
    if recording and not HOTKEY.issubset(current_keys):
        stop_recording()


def start_recording():
    """Démarre l'enregistrement audio"""
    global recording, audio_data
    recording = True
    audio_data = []
    
    def callback(indata, frames, time, status):
        if status:
            print(f"⚠️  {status}")
        if recording:
            audio_data.append(indata.copy())
    
    # Stream audio depuis le micro
    global stream
    stream = sd.InputStream(
        samplerate=SAMPLE_RATE,
        channels=1,
        callback=callback
    )
    stream.start()


def stop_recording():
    """Arrête l'enregistrement et lance la transcription"""
    global recording, audio_data, stream
    recording = False
    stream.stop()
    stream.close()
    
    if not audio_data:
        print("❌ Pas d'audio enregistré")
        return
    
    print("⏳ Transcription en cours...")
    
    # Concatener les chunks audio
    audio = np.concatenate(audio_data, axis=0)
    
    # Sauver temporairement (Whisper attend un fichier)
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
        sf.write(tmp_file.name, audio, SAMPLE_RATE)
        tmp_path = tmp_file.name
    
    try:
        # Transcription avec Whisper
        model = whisper.load_model("base")  # Options: tiny, base, small, medium, large
        result = model.transcribe(tmp_path, language="fr")  # Adapte la langue si besoin
        text = result["text"].strip()
        
        if text:
            print(f"✅ Transcrit: {text}")
            
            # Copier dans le clipboard
            pyperclip.copy(text)
            
            # Simuler Cmd+V (Mac) ou Ctrl+V (Windows)
            if sys.platform == "darwin":
                keyboard_controller.press(Key.cmd)
                keyboard_controller.press('v')
                keyboard_controller.release('v')
                keyboard_controller.release(Key.cmd)
            else:
                keyboard_controller.press(Key.ctrl)
                keyboard_controller.press('v')
                keyboard_controller.release('v')
                keyboard_controller.release(Key.ctrl)
            
            print("📋 Texte collé dans l'application active")
        else:
            print("❌ Aucun texte détecté")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    finally:
        # Nettoyer le fichier temporaire
        os.unlink(tmp_path)


def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🎙️  VoiceSnap - Whisper Local")
    print("=" * 60)
    print(f"Hotkey: Ctrl+Shift+Space")
    print("Maintenez la combinaison, parlez, puis relâchez pour transcrire")
    print("Appuyez sur Ctrl+C pour quitter")
    print("=" * 60)
    
    # Charger le modèle Whisper au démarrage
    print("⏳ Chargement du modèle Whisper...")
    global model
    model = whisper.load_model("base")
    print("✅ Modèle chargé\n")
    
    # Démarrer l'écoute des touches
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Arrêt du programme")
        sys.exit(0)
