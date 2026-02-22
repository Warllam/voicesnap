# 🚀 VoiceSnap - Guide des Lanceurs

**Tous les moyens de lancer VoiceSnap sur Windows**

---

## 🎯 Quick Start

**Première utilisation :**
```cmd
npm install
cd python && pip install -r requirements.txt && cd ..
start.bat
```

**Après :**
```cmd
start.bat
```

---

## 📂 Fichiers de lancement

| Fichier | Description | Utilisation |
|---------|-------------|-------------|
| **start.bat** | Lance tout (backend + Tauri) | Double-clic ou `start.bat` |
| **start-browser.bat** | Mode navigateur (si Tauri bug) | Double-clic ou `start-browser.bat` |
| **launcher.py** | Launcher Python (à compiler) | `python launcher.py` |
| **build_exe.bat** | Compile launcher.py en .exe | `build_exe.bat` |
| **start.sh** | Version Linux/Mac | `./start.sh` |

---

## 🔍 Détails de chaque launcher

### 1. **start.bat** (RECOMMANDÉ)

**Type :** Script batch Windows  
**Prérequis :** Python, Node.js  
**Ce qu'il fait :**
1. Vérifie Python & Node
2. Lance le backend Python (port 8765)
3. Lance Tauri dev (port 1420)
4. Gère l'arrêt propre

**Utilisation :**
```cmd
start.bat
```

**Avantages :**
- ✅ Simple, rapide
- ✅ Pas de compilation
- ✅ Facile à éditer

**Inconvénients :**
- ⚠️ Fenêtre console visible
- ⚠️ Besoin Python + Node

---

### 2. **start-browser.bat** (FALLBACK)

**Type :** Script batch Windows  
**Prérequis :** Python, Node.js  
**Ce qu'il fait :**
1. Lance le backend Python
2. Lance Vite dev server
3. Ouvre le navigateur sur localhost:1420

**Utilisation :**
```cmd
start-browser.bat
```

**Quand l'utiliser :**
- Si Tauri refuse de compiler
- Si tu préfères le navigateur
- Pour tester sans Tauri

**Note :** Pas de hotkey global (Ctrl+Space), mais tout le reste fonctionne.

---

### 3. **launcher.py** (COMPILABLE)

**Type :** Script Python  
**Prérequis :** Python, Node.js, PyInstaller  
**Ce qu'il fait :**
- Même chose que start.bat, mais en Python
- Peut être compilé en .exe avec PyInstaller

**Utilisation :**
```cmd
REM Direct
python launcher.py

REM Compiler en .exe
build_exe.bat
dist\VoiceSnap.exe
```

**Avantages :**
- ✅ Peut devenir un .exe
- ✅ Meilleure gestion des processus
- ✅ Plus "pro"

**Inconvénients :**
- ⚠️ Nécessite compilation pour .exe
- ⚠️ Plus complexe à modifier

---

### 4. **build_exe.bat** (COMPILATEUR)

**Type :** Script de build  
**Prérequis :** Python, PyInstaller  
**Ce qu'il fait :**
- Compile `launcher.py` en `dist\VoiceSnap.exe`
- Utilise PyInstaller
- Bundler les dépendances

**Utilisation :**
```cmd
build_exe.bat
REM Crée : dist\VoiceSnap.exe
```

**Temps :** ~5-10 minutes

---

### 5. **Tauri Build** (PRODUCTION)

**Type :** Build Rust natif  
**Prérequis :** Rust, Tauri CLI  
**Ce qu'il fait :**
- Compile toute l'app en binaire
- Crée un installateur .msi
- Version production optimisée

**Utilisation :**
```cmd
npm run tauri:build
REM Crée : src-tauri\target\release\bundle\msi\VoiceSnap_3.0.0_x64.msi
```

**Temps :** ~30-60 minutes (première fois)

**Voir :** `BUILD_WINDOWS.md` pour le guide complet

---

## 🎯 Quelle solution pour quel besoin ?

| Besoin | Solution | Fichier |
|--------|----------|---------|
| **Tester rapidement** | Batch simple | `start.bat` |
| **Tauri ne marche pas** | Mode navigateur | `start-browser.bat` |
| **Avoir un .exe léger** | Compile launcher | `build_exe.bat` |
| **Distribuer l'app** | Build Tauri | `npm run tauri:build` |
| **Production finale** | Build Tauri | `npm run tauri:build` |

---

## 🛠️ Setup Initial (une seule fois)

```cmd
REM 1. Installer Node dependencies
npm install

REM 2. Installer Python dependencies
cd python
pip install -r requirements.txt
cd ..

REM 3. Lancer !
start.bat
```

---

## 🔧 Personnalisation

### Changer le port backend

Édite `python/server.py` :
```python
PORT = 8765  # Change ici
```

### Changer le port frontend

Édite `vite.config.ts` :
```ts
server: {
  port: 1420  // Change ici
}
```

### Changer le hotkey global

Édite `~/.voicesnap/config.json` :
```json
{
  "hotkey": {
    "modifiers": ["ctrl"],
    "key": "space"
  }
}
```

---

## 📊 Comparaison des lanceurs

|  | start.bat | start-browser.bat | launcher.py | Tauri Build |
|---|-----------|-------------------|-------------|-------------|
| **Taille** | ~2 KB | ~1 KB | ~5 KB | ~50-100 MB |
| **Setup** | 0 min | 0 min | 5 min | 60 min |
| **Prérequis** | Py + Node | Py + Node | Py + Node + PyInstaller | Rust |
| **Hotkey global** | ✅ | ❌ | ✅ | ✅ |
| **Standalone** | ❌ | ❌ | ❌ | ✅ |
| **Dev mode** | ✅ | ✅ | ✅ | ❌ |
| **Installateur** | ❌ | ❌ | ❌ | ✅ (.msi) |

---

## 🐛 Troubleshooting

### Aucun launcher ne marche

**Vérifie les prérequis :**
```cmd
python --version   REM Doit afficher 3.11+
node --version     REM Doit afficher 18+
npm --version      REM Doit afficher 9+
```

**Si Python/Node manquent :**
- Python : https://www.python.org/downloads/
- Node.js : https://nodejs.org/

### Backend ne démarre pas

**Lance manuellement pour voir l'erreur :**
```cmd
cd python
python server.py
```

**Erreurs communes :**
- Port 8765 déjà utilisé → tue le processus
- Module manquant → `pip install -r requirements.txt`

### Frontend ne démarre pas

```cmd
REM Réinstalle les dépendances
rm -rf node_modules package-lock.json
npm install
```

### Tauri build échoue

**Installe Rust :**
```cmd
winget install Rustlang.Rust
rustc --version
```

**Réinstalle Tauri CLI :**
```cmd
cargo install tauri-cli
```

---

## 📚 Ressources

- **README_TAURI.md** - Guide complet Tauri
- **BUILD_WINDOWS.md** - Guide de build Windows
- **LAUNCHER_README.md** - Détails sur les lanceurs
- **QUICKSTART.md** - Guide de démarrage rapide

---

## 💡 Tips

- **Dev quotidien** → `start.bat`
- **Demo à quelqu'un** → Compile avec `build_exe.bat`
- **Release publique** → Build Tauri complet
- **Tauri bug** → Fallback sur `start-browser.bat`

---

**Créé le 2026-02-22 par ClawdBot 🤖**  
*Pour toute question : Discord #voice-formatter*
