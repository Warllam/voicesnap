#!/usr/bin/env python3
"""
VoiceSnap Launcher
Démarre le backend Python + l'interface Tauri
"""

import os
import sys
import subprocess
import time
import signal
import requests
from pathlib import Path

class VoiceSnapLauncher:
    def __init__(self):
        self.base_dir = Path(__file__).parent.absolute()
        self.python_dir = self.base_dir / "python"
        self.backend_process = None
        self.frontend_process = None
        
    def check_dependencies(self):
        """Vérifie que les dépendances sont installées"""
        print("🔍 Vérification des dépendances...")
        
        # Check Python
        if sys.version_info < (3, 11):
            print("❌ Python 3.11+ requis !")
            return False
        
        # Check Node
        try:
            subprocess.run(["node", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ Node.js non installé !")
            return False
        
        # Check npm dependencies
        if not (self.base_dir / "node_modules").exists():
            print("📦 Installation des dépendances Node...")
            subprocess.run(["npm", "install"], cwd=self.base_dir, check=True)
        
        print("✅ Dépendances OK")
        return True
    
    def start_backend(self):
        """Démarre le serveur Python"""
        print("🐍 Démarrage du backend Python...")
        
        server_script = self.python_dir / "server.py"
        if not server_script.exists():
            print(f"❌ Fichier introuvable : {server_script}")
            return False
        
        # Démarrer le serveur
        self.backend_process = subprocess.Popen(
            [sys.executable, "server.py"],
            cwd=self.python_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Attendre que le serveur soit prêt
        print("⏳ Attente du serveur backend...")
        for i in range(30):
            try:
                response = requests.get("http://localhost:8765/health", timeout=1)
                if response.status_code == 200:
                    print("✅ Backend démarré !")
                    return True
            except:
                pass
            time.sleep(1)
        
        print("❌ Le backend n'a pas démarré à temps")
        return False
    
    def start_frontend(self):
        """Démarre l'interface Tauri"""
        print("🚀 Démarrage de l'interface Tauri...")
        
        self.frontend_process = subprocess.Popen(
            ["npm", "run", "tauri:dev"],
            cwd=self.base_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("✅ Interface lancée !")
        return True
    
    def cleanup(self):
        """Arrête proprement les processus"""
        print("\n🛑 Arrêt de VoiceSnap...")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
        
        print("✅ Arrêté proprement")
    
    def run(self):
        """Lance l'application complète"""
        print("🎙️ VoiceSnap Launcher v3.0.0")
        print("=" * 50)
        print()
        
        try:
            # Vérifier les dépendances
            if not self.check_dependencies():
                return 1
            
            # Démarrer le backend
            if not self.start_backend():
                return 1
            
            # Démarrer le frontend
            if not self.start_frontend():
                return 1
            
            print()
            print("=" * 50)
            print("✨ VoiceSnap est prêt !")
            print("=" * 50)
            print()
            print("📌 Backend : http://localhost:8765")
            print("📌 Frontend : http://localhost:1420")
            print()
            print("Appuyez sur Ctrl+C pour arrêter")
            print()
            
            # Attendre que le frontend se termine
            self.frontend_process.wait()
            
        except KeyboardInterrupt:
            print("\n⚠️ Interruption par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur : {e}")
            return 1
        finally:
            self.cleanup()
        
        return 0

def main():
    launcher = VoiceSnapLauncher()
    sys.exit(launcher.run())

if __name__ == "__main__":
    main()
