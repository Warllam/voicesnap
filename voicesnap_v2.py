#!/usr/bin/env python3
"""
VoiceSnap v2 - Desktop Voice-to-Text Application
Local transcription with OpenAI Whisper
"""

import sys
import os
import threading
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.config import Config
from src.database import TranscriptionDB
from src.core.recorder import AudioRecorder
from src.core.transcriber import Transcriber
from src.core.hotkey_manager import HotkeyManager
from src.ui.main_window import MainWindow
from src.ui.overlay import RecordingOverlay
from src.ui.system_tray import SystemTray

import pyperclip
from pynput.keyboard import Controller, Key


class VoiceSnapApp:
    """Main VoiceSnap application"""
    
    def __init__(self):
        """Initialize the application"""
        print("🎤 VoiceSnap v2 - Starting...")
        
        # Load configuration
        self.config = Config()
        print(f"✓ Configuration loaded from {self.config.config_file}")
        
        # Initialize database
        db_path = self.config.get_data_dir() / "transcriptions.db"
        self.db = TranscriptionDB(str(db_path))
        print(f"✓ Database initialized at {db_path}")
        
        # Initialize core components
        self.recorder = AudioRecorder(
            sample_rate=self.config.get("audio.sample_rate"),
            channels=self.config.get("audio.channels"),
            device_index=self.config.get("audio.device_index"),
            max_duration=self.config.get("audio.max_duration")
        )
        print("✓ Audio recorder initialized")
        
        self.transcriber = Transcriber(
            model_name=self.config.get("whisper.model"),
            language=self.config.get("whisper.language")
        )
        print("✓ Transcriber initialized")
        
        self.hotkey_manager = HotkeyManager()
        self._setup_hotkey()
        print("✓ Hotkey manager initialized")
        
        # Initialize UI components
        self.main_window = MainWindow("VoiceSnap v2")
        print("✓ Main window created")
        
        self.overlay: RecordingOverlay = None
        self.system_tray = SystemTray("VoiceSnap")
        print("✓ System tray initialized")
        
        # State
        self.is_recording = False
        self.keyboard_controller = Controller()
        
        # Setup UI callbacks
        self._setup_ui_callbacks()
        
        # Load Whisper model in background
        threading.Thread(target=self._load_model, daemon=True).start()
        
        # Load initial data
        self._load_history()
        self._load_audio_devices()
        
        print("✅ VoiceSnap v2 ready!")
        self.main_window.set_status("Ready - Press hotkey to start recording")
    
    def _setup_hotkey(self):
        """Setup global hotkey"""
        modifiers = self.config.get("hotkey.modifiers", ["ctrl"])
        key = self.config.get("hotkey.key", "space")
        toggle_mode = self.config.get("hotkey.toggle_mode", True)
        
        self.hotkey_manager.set_hotkey(modifiers, key, toggle_mode)
        self.hotkey_manager.set_callbacks(
            on_activate=self._on_hotkey_activate,
            on_deactivate=self._on_hotkey_deactivate
        )
        
        # Update UI
        hotkey_str = self.hotkey_manager.get_hotkey_string()
        self.main_window.hotkey_var.set(hotkey_str)
    
    def _setup_ui_callbacks(self):
        """Setup UI callbacks"""
        self.main_window.on_settings_changed = self._on_settings_changed
        self.main_window.on_close = self._on_window_close
        
        self.system_tray.on_show = lambda: self.main_window.show()
        self.system_tray.on_settings = lambda: self.main_window.show()
        self.system_tray.on_quit = self._quit_application
    
    def _load_model(self):
        """Load Whisper model in background"""
        def progress(msg):
            print(f"Model: {msg}")
            self.main_window.set_status(msg)
        
        try:
            self.transcriber.load_model(progress_callback=progress)
            self.main_window.set_status("Model loaded - Ready to transcribe!")
        except Exception as e:
            error_msg = f"Error loading model: {e}"
            print(f"❌ {error_msg}")
            self.main_window.set_status(error_msg)
    
    def _load_history(self):
        """Load transcription history"""
        try:
            transcriptions = self.db.get_recent_transcriptions(limit=50)
            self.main_window.update_history(transcriptions)
        except Exception as e:
            print(f"Error loading history: {e}")
    
    def _load_audio_devices(self):
        """Load available audio devices"""
        try:
            devices = AudioRecorder.list_devices()
            self.main_window.set_microphones(devices)
        except Exception as e:
            print(f"Error loading audio devices: {e}")
    
    def _on_hotkey_activate(self):
        """Handle hotkey activation (start recording)"""
        if self.is_recording:
            # Already recording, stop it
            self._stop_recording()
        else:
            # Start recording
            self._start_recording()
    
    def _on_hotkey_deactivate(self):
        """Handle hotkey deactivation (stop recording)"""
        # In toggle mode, this is handled by _on_hotkey_activate
        # In push-to-talk mode, stop recording when key is released
        if not self.config.get("hotkey.toggle_mode", True):
            self._stop_recording()
    
    def _start_recording(self):
        """Start audio recording"""
        if self.is_recording:
            return
        
        print("🎤 Recording started...")
        self.is_recording = True
        
        # Update UI
        self.main_window.set_status("🔴 Recording...")
        self.system_tray.update_icon(recording=True)
        
        # Show overlay
        self.overlay = RecordingOverlay(
            position=self.config.get("ui.overlay_position", "top"),
            height=self.config.get("ui.overlay_height", 80)
        )
        self.overlay.show(self.main_window.root)
        
        # Setup waveform callback
        def waveform_callback(audio_data):
            if self.overlay:
                self.overlay.update_waveform(audio_data)
        
        self.recorder.set_waveform_callback(waveform_callback)
        
        # Start recording
        try:
            self.recorder.start_recording()
            
            # Update overlay duration
            def update_duration():
                while self.is_recording:
                    duration = self.recorder.get_duration()
                    if self.overlay:
                        self.overlay.update_duration(duration)
                    time.sleep(0.1)
            
            threading.Thread(target=update_duration, daemon=True).start()
            
        except Exception as e:
            print(f"❌ Error starting recording: {e}")
            self.main_window.set_status(f"Error: {e}")
            self._stop_recording()
    
    def _stop_recording(self):
        """Stop audio recording and transcribe"""
        if not self.is_recording:
            return
        
        print("⏹️ Recording stopped")
        self.is_recording = False
        
        # Hide overlay
        if self.overlay:
            self.overlay.hide()
            self.overlay = None
        
        # Update UI
        self.main_window.set_status("⏳ Transcribing...")
        self.system_tray.update_icon(recording=False)
        
        # Stop recording and get audio
        audio = self.recorder.stop_recording()
        
        if audio is None or len(audio) == 0:
            print("❌ No audio recorded")
            self.main_window.set_status("No audio recorded")
            return
        
        # Transcribe in background thread
        def transcribe_thread():
            try:
                # Transcribe
                save_audio = True  # Save audio for history
                audio_cache_dir = self.config.get_audio_cache_dir()
                
                result = self.transcriber.transcribe_audio(
                    audio,
                    sample_rate=self.config.get("audio.sample_rate"),
                    save_audio=save_audio,
                    audio_cache_dir=audio_cache_dir
                )
                
                text = result["text"]
                
                if not text:
                    print("❌ No text transcribed")
                    self.main_window.set_status("No text detected")
                    return
                
                print(f"✅ Transcribed: {text}")
                
                # Save to database
                auto_paste = self.config.get("behavior.auto_paste", True)
                
                transcription_id = self.db.add_transcription(
                    text=text,
                    language=self.config.get("whisper.language"),
                    detected_language=result.get("language"),
                    model=self.config.get("whisper.model"),
                    duration=result.get("duration"),
                    audio_file=result.get("audio_file"),
                    pasted=auto_paste
                )
                
                print(f"✓ Saved to database (ID: {transcription_id})")
                
                # Copy to clipboard
                if self.config.get("behavior.copy_to_clipboard", True):
                    pyperclip.copy(text)
                    print("✓ Copied to clipboard")
                
                # Auto-paste if enabled
                if auto_paste:
                    time.sleep(0.2)  # Small delay to ensure clipboard is updated
                    self._paste_text()
                    print("✓ Auto-pasted")
                
                # Update UI
                self.main_window.set_status(f"✅ Transcribed: {text[:50]}...")
                
                # Show notification
                if self.config.get("ui.show_notifications", True):
                    self.system_tray.show_notification(
                        "Transcription Complete",
                        text[:100] + ("..." if len(text) > 100 else "")
                    )
                
                # Reload history
                self._load_history()
                
            except Exception as e:
                error_msg = f"Error during transcription: {e}"
                print(f"❌ {error_msg}")
                self.main_window.set_status(error_msg)
        
        threading.Thread(target=transcribe_thread, daemon=True).start()
    
    def _paste_text(self):
        """Paste text using keyboard shortcut"""
        try:
            if sys.platform == "darwin":
                self.keyboard_controller.press(Key.cmd)
                self.keyboard_controller.press('v')
                self.keyboard_controller.release('v')
                self.keyboard_controller.release(Key.cmd)
            else:
                self.keyboard_controller.press(Key.ctrl)
                self.keyboard_controller.press('v')
                self.keyboard_controller.release('v')
                self.keyboard_controller.release(Key.ctrl)
        except Exception as e:
            print(f"Error pasting: {e}")
    
    def _on_settings_changed(self):
        """Handle settings changes"""
        settings = self.main_window.get_settings()
        
        # Update model if changed
        current_model = self.config.get("whisper.model")
        new_model = settings.get("model")
        
        if new_model and new_model != current_model:
            self.config.set("whisper.model", new_model)
            
            def change_model():
                self.main_window.set_status(f"Loading {new_model} model...")
                try:
                    self.transcriber.change_model(
                        new_model,
                        progress_callback=lambda msg: self.main_window.set_status(msg)
                    )
                    self.main_window.set_status(f"Switched to {new_model} model")
                except Exception as e:
                    self.main_window.set_status(f"Error loading model: {e}")
            
            threading.Thread(target=change_model, daemon=True).start()
        
        # Update language if changed
        lang_map = {
            "Auto-detect": None,
            "English": "en",
            "French": "fr",
            "Spanish": "es",
            "German": "de",
            "Italian": "it"
        }
        
        new_language = lang_map.get(settings.get("language"))
        if new_language != self.config.get("whisper.language"):
            self.config.set("whisper.language", new_language)
            self.transcriber.set_language(new_language)
        
        # Update behavior settings
        if "auto_paste" in settings:
            self.config.set("behavior.auto_paste", settings["auto_paste"])
        
        if "minimize_to_tray" in settings:
            self.config.set("behavior.minimize_to_tray", settings["minimize_to_tray"])
        
        print("✓ Settings updated")
    
    def _on_window_close(self):
        """Handle main window close"""
        if self.config.get("behavior.minimize_to_tray", True):
            # Minimize to tray instead of closing
            self.main_window.hide()
        else:
            # Quit application
            self._quit_application()
    
    def _quit_application(self):
        """Quit the application"""
        print("\n👋 Shutting down VoiceSnap...")
        
        # Stop recording if active
        if self.is_recording:
            self.recorder.stop_recording()
        
        # Stop hotkey listener
        self.hotkey_manager.stop()
        
        # Stop system tray
        self.system_tray.stop()
        
        # Close database
        self.db.close()
        
        # Quit GUI
        self.main_window.root.quit()
        
        print("✓ Goodbye!")
        sys.exit(0)
    
    def run(self):
        """Run the application"""
        # Start hotkey listener
        self.hotkey_manager.start()
        print(f"✓ Hotkey listener started: {self.hotkey_manager.get_hotkey_string()}")
        
        # Start system tray
        self.system_tray.start()
        print("✓ System tray started")
        
        # Run main window (blocking)
        print("✓ Starting GUI...")
        self.main_window.run()


def main():
    """Main entry point"""
    try:
        app = VoiceSnapApp()
        app.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
