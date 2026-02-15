# 🚀 VoiceSnap Tauri - Quick Start

## Installation rapide (5 minutes)

### 1. Prérequis

```bash
# Installer FFmpeg (nécessaire pour Whisper)
sudo apt install ffmpeg python3-pip

# Vérifier les installations
python3 --version  # Doit être 3.11+
node --version     # Doit être 18+
cargo --version    # Rust/Cargo
```

### 2. Setup Python

```bash
cd python
pip install -r requirements.txt
```

Première installation : Whisper téléchargera automatiquement le modèle (~150 MB pour 'base')

### 3. Lancer l'application

**Option A : Script automatique** (recommandé)
```bash
./start.sh
```

**Option B : Manuel (2 terminaux)**

Terminal 1 - Backend Python :
```bash
cd python
python server.py
```

Terminal 2 - Frontend Tauri :
```bash
npm run tauri:dev
```

### 4. Utilisation

1. **Lancer l'enregistrement** : `Ctrl+Space`
2. **Parler** dans le micro
3. **Arrêter** : `Ctrl+Space` à nouveau
4. **Résultat** : Transcription automatique + copie dans le presse-papier !

---

## 🎨 Interface

### Navigation Sidebar (gauche)
- 🏠 **Transcriptions** : Historique complet
- ⚙️ **Settings** : Configuration
- ℹ️ **About** : À propos

### Recording Overlay (top center)
Quand tu enregistres :
- Waveform en temps réel
- Timer
- Bouton Stop

### Transcription Cards
- Design moderne avec hover effects
- Actions : Copier / Supprimer
- Métadonnées : date, durée, langue

---

## ⚙️ Configuration (Settings page)

### Audio
- Choisis ton micro
- Plusieurs devices supportés

### Transcription
- **Modèle Whisper** :
  - `tiny` : Ultra rapide, précision correcte
  - `base` : ✨ **Recommandé** - Bon équilibre
  - `small` : Meilleure précision
  - `medium`/`large` : Précision maximale (lent, GPU recommandé)

- **Langue** :
  - Auto-detect (par défaut)
  - Français, Anglais, Espagnol, etc. (99+ langues)

### Behavior
- **Auto-paste** : Colle automatiquement après transcription
- **Hotkey** : `Ctrl+Space` (global, marche même app en arrière-plan)

---

## 📁 Fichiers importants

```
~/.voicesnap/
├── config.json           # Configuration
├── data/
│   └── transcriptions.db # Base de données SQLite
└── audio_cache/          # Fichiers audio (optionnel)
```

---

## 🐛 Problèmes courants

### "Server Not Connected"
→ Vérifie que le backend Python tourne : `python python/server.py`
→ Port 8765 doit être libre : `lsof -i :8765`

### "Whisper model not loaded yet"
→ Premier lancement : attends ~30s (téléchargement du modèle)
→ Modèles stockés dans `~/.cache/whisper/`

### Pas d'audio capturé
→ Vérifie les permissions du micro
→ Teste dans Settings > Audio Settings
→ Essaie un autre device

### Build Tauri échoue
```bash
# Linux: installer les dépendances système
sudo apt install libwebkit2gtk-4.1-dev \
  libappindicator3-dev librsvg2-dev patchelf

# Clear cache
rm -rf node_modules src-tauri/target
npm install
```

---

## 🚀 Build Production

```bash
npm run tauri:build
```

Créé :
- **Linux** : `.deb` + `.AppImage`
- **Windows** : `.exe` + `.msi`
- **macOS** : `.dmg` + `.app`

Dans `src-tauri/target/release/bundle/`

---

## 💡 Tips

1. **Premier lancement** : Le modèle Whisper se télécharge automatiquement
2. **Performance** : Utilise `base` pour l'usage quotidien, `small` si tu as un GPU
3. **Raccourci global** : `Ctrl+Space` marche même dans d'autres apps !
4. **Recherche** : Barre de recherche dans la page Transcriptions
5. **Copie rapide** : Hover sur une card → bouton copier

---

## 🎯 Workflow typique

```
1. Travail dans n'importe quelle app
2. Ctrl+Space → Commence à parler
3. Ctrl+Space → Stop
4. ✨ Texte transcrit copié automatiquement
5. Ctrl+V pour coller où tu veux !
```

---

**Enjoy! 🎉**

Feedback / Issues : https://github.com/Warllam/voicesnap/issues
