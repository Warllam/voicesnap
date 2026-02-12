# VoiceSnap 🎤

> **Transcription vocale locale ultra-rapide** - Le clone open-source de SuperWhisper

Transformez votre voix en texte instantanément avec Whisper d'OpenAI, 100% local et gratuit.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

## ✨ Features

- 🔒 **100% Local** - Aucune donnée ne quitte votre machine
- ⚡ **Ultra-rapide** - Transcription en temps réel
- 🎯 **Hotkey global** - Ctrl+Shift+Space depuis n'importe quelle app
- 📋 **Auto-paste** - Le texte s'insère directement où vous tapez
- 🌍 **Multi-langue** - Français, anglais, et 95+ autres langues
- 🖥️ **Cross-platform** - Windows, macOS, Linux

## 🎯 Fonctionnement

1. **Appuyez et maintenez** `Ctrl+Shift+Space`
2. **Parlez** dans votre micro
3. **Relâchez** les touches
4. Le texte transcrit est automatiquement collé dans l'application active

## 📦 Installation

### Prérequis
- Python 3.8+
- ffmpeg (requis par Whisper)

#### Installer ffmpeg

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Télécharger depuis https://ffmpeg.org/download.html ou via chocolatey:
```bash
choco install ffmpeg
```

**Linux:**
```bash
sudo apt install ffmpeg  # Debian/Ubuntu
sudo dnf install ffmpeg  # Fedora
```

### Installation des dépendances Python

```bash
pip install -r requirements.txt
```

⚠️ **Note:** Le premier lancement téléchargera le modèle Whisper (~150 MB pour le modèle "base")

## 🚀 Utilisation

```bash
python voicesnap.py
```

Le programme reste actif en arrière-plan. Utilisez `Ctrl+C` pour quitter.

## ⚙️ Configuration

Dans `voice_formatter.py`, vous pouvez modifier :

- **Modèle Whisper** (ligne 95 et 110) :
  - `tiny` - le plus rapide, moins précis (~40 MB)
  - `base` - bon compromis vitesse/précision (~150 MB) ⭐️ par défaut
  - `small` - plus précis (~500 MB)
  - `medium` - très précis (~1.5 GB)
  - `large` - meilleur qualité (~3 GB)

- **Langue** (ligne 95) :
  - `language="fr"` pour français
  - `language="en"` pour anglais
  - `language=None` pour détection auto

- **Hotkey** (ligne 14) :
  - Actuellement: `Ctrl+Shift+Space`
  - Modifier `HOTKEY` pour personnaliser

## 🔧 Troubleshooting

**Problème: Le micro n'enregistre rien**
- Vérifiez les permissions micro de votre OS
- Testez avec un autre logiciel d'enregistrement

**Problème: Erreur ffmpeg**
- Vérifiez que ffmpeg est dans votre PATH : `ffmpeg -version`

**Problème: Le paste ne fonctionne pas**
- Vérifiez les permissions accessibilité (macOS)
- Le texte est toujours copié dans le clipboard même si le paste échoue

## 📝 TODO (améliorations futures)

- [ ] UI overlay pour feedback visuel
- [ ] Reformulation IA avec LLM local (ollama?)
- [ ] Presets de prompts (professionnel, casual, etc.)
- [ ] Détection de langue automatique
- [ ] Packaging en .app (macOS) / .exe (Windows)

## 📄 License

MIT - Faites-en ce que vous voulez
