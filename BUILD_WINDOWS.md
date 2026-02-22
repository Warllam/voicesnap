# 🪟 VoiceSnap - Build Windows .exe

Guide pour créer un exécutable Windows qui lance VoiceSnap en un clic.

---

## 📋 Prérequis

### Sur Windows (PC PA - 192.168.1.193)

1. **Python 3.11+**
   ```cmd
   python --version
   ```
   Si absent : https://www.python.org/downloads/

2. **Node.js 18+**
   ```cmd
   node --version
   ```
   Si absent : https://nodejs.org/

3. **Rust + Tauri CLI** (pour build Tauri complet)
   ```cmd
   winget install Rustlang.Rust
   ```

4. **Git** (pour cloner le projet)
   ```cmd
   winget install Git.Git
   ```

---

## 🚀 Option 1 : Launcher Simple (.exe léger)

**Avantages :** Rapide, facile, fonctionne partout  
**Inconvénients :** Lance le dev mode (pas un vrai standalone)

### Étapes

1. **Transférer le projet sur Windows**
   ```cmd
   cd C:\Users\PA\Projects
   scp -r warllam@192.168.1.x:/home/warllam/clawd/voicesnap .
   ```
   *(ou cloner depuis Git)*

2. **Installer les dépendances**
   ```cmd
   cd voicesnap
   
   REM Node
   npm install
   
   REM Python
   cd python
   pip install -r requirements.txt
   cd ..
   ```

3. **Compiler le launcher en .exe**
   ```cmd
   build_exe.bat
   ```

4. **Lancer l'app**
   ```cmd
   dist\VoiceSnap.exe
   ```

**Résultat :** Un .exe (~10 MB) qui lance automatiquement :
- Le serveur Python backend (port 8765)
- L'interface Tauri dev (port 1420)

---

## 🏗️ Option 2 : Build Tauri Complet (Standalone)

**Avantages :** Vrai .exe standalone, professionnel, installable  
**Inconvénients :** Plus long, nécessite Rust

### Étapes

1. **Installer Rust**
   ```cmd
   winget install Rustlang.Rust
   rustc --version
   ```

2. **Installer Tauri CLI**
   ```cmd
   npm install -g @tauri-apps/cli
   ```

3. **Build l'application**
   ```cmd
   cd voicesnap
   npm run tauri:build
   ```

4. **Récupérer l'installateur**
   ```
   src-tauri\target\release\bundle\msi\VoiceSnap_3.0.0_x64.msi
   src-tauri\target\release\VoiceSnap.exe
   ```

**Résultat :** Un .exe (~50-100 MB) complètement standalone avec :
- Tout intégré (Rust backend + React frontend)
- Installateur Windows (.msi)
- Icône système, raccourci, etc.

---

## 🎯 Quelle option choisir ?

| Critère | Option 1 (Launcher) | Option 2 (Tauri Build) |
|---------|---------------------|------------------------|
| **Rapidité** | ⚡ 5 minutes | 🐢 30-60 minutes |
| **Taille** | 📦 10 MB | 📦 50-100 MB |
| **Dépendances** | Python + Node requis | ✅ Standalone |
| **Professionnel** | ⚠️ Dev mode | ✅ Production |
| **Hotkey global** | ❌ Non | ✅ Oui (Ctrl+Space) |

**Recommandation :** 
- **Pour tester rapidement** → Option 1
- **Pour distribuer/utiliser vraiment** → Option 2

---

## 🐛 Troubleshooting

### PyInstaller ne trouve pas les modules
```cmd
pip install --upgrade pyinstaller requests
```

### Tauri build échoue
```cmd
REM Installer les dépendances Windows
npm install
cd python
pip install -r requirements.txt
cd ..

REM Réinstaller Tauri CLI
cargo install tauri-cli
```

### L'exe lance mais ne marche pas
- Vérifier que Python est dans le PATH
- Vérifier que Node est dans le PATH
- Lancer depuis un terminal pour voir les erreurs

### Port 8765 déjà utilisé
```cmd
REM Tuer le processus qui utilise le port
netstat -ano | findstr :8765
taskkill /PID <PID> /F
```

---

## 📝 Notes

- **Launcher** : Lance le mode dev (hot-reload actif)
- **Tauri Build** : Compile tout en binaire Rust optimisé
- **Python backend** : Doit toujours tourner (même en build Tauri)

Le backend Python ne peut pas être compilé dans le .exe Tauri car Whisper nécessite Python. Il faut soit :
1. Bundler Python avec l'app (PyInstaller)
2. Demander Python comme prérequis
3. Utiliser une API Whisper externe (pas de Python local)

---

## 🔗 Liens

- [Tauri Build Guide](https://tauri.app/v2/guides/building/)
- [PyInstaller Docs](https://pyinstaller.org/en/stable/)
- [Whisper AI](https://github.com/openai/whisper)

---

**Créé le 2026-02-22 par ClawdBot 🤖**
