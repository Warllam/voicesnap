# VoiceSnap 🎤

> **Local voice-to-text transcription** - Your private SuperWhisper alternative

Transform your voice into text instantly with OpenAI Whisper, 100% local, no cloud, no API keys.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

![VoiceSnap Screenshot](assets/screenshot.png)

## ✨ Features

### 🎯 Core Features
- 🔒 **100% Local** - All processing happens on your machine, zero cloud dependency
- ⚡ **Global Hotkey** - Ctrl+Space to start/stop recording from anywhere
- 📊 **Live Waveform** - Real-time audio visualization during recording
- 🤖 **AI Transcription** - Powered by OpenAI Whisper (state-of-the-art accuracy)
- 📋 **Auto-Paste** - Transcription automatically inserted where you're typing
- 🌍 **Multi-Language** - Supports 99+ languages (French, English, Spanish, etc.)

### 🎨 Interface
- 🖥️ **Desktop App** - Clean, modern interface with CustomTkinter
- 🔝 **Recording Overlay** - Minimal overlay shows recording status and waveform
- 📚 **History** - Searchable history of all transcriptions
- ⚙️ **Settings** - Customize hotkey, model, language, behavior
- 🔔 **System Tray** - Runs in background, accessible from tray icon

### 🛠️ Advanced
- 📁 **SQLite Database** - All transcriptions stored locally with full-text search
- 🎙️ **Device Selection** - Choose your preferred microphone
- 🧠 **Model Options** - Tiny (fast) to Large (most accurate)
- 🔄 **Cross-Platform** - Works on Windows, macOS, and Linux

## 🚀 Installation

### Prerequisites

1. **Python 3.8+**
   ```bash
   python3 --version
   ```

2. **ffmpeg** (required by Whisper)
   
   **macOS:**
   ```bash
   brew install ffmpeg
   ```
   
   **Linux (Ubuntu/Debian):**
   ```bash
   sudo apt update && sudo apt install ffmpeg
   ```
   
   **Windows:**
   Download from [ffmpeg.org](https://ffmpeg.org/download.html) or use chocolatey:
   ```bash
   choco install ffmpeg
   ```

### Install VoiceSnap

1. **Clone the repository**
   ```bash
   git clone https://github.com/Warllam/voicesnap.git
   cd voicesnap
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_v2.txt
   ```
   
   ⚠️ **Note:** First run will download the Whisper model (~150MB for "base" model)

3. **Run VoiceSnap**
   ```bash
   python3 voicesnap_v2.py
   ```

## 📖 Usage

### Quick Start

1. **Launch VoiceSnap**
   ```bash
   python3 voicesnap_v2.py
   ```

2. **Wait for "Model loaded"** in the status bar

3. **Press your hotkey** (default: `Ctrl+Space`)
   - Recording overlay appears at the top of your screen
   - Speak into your microphone
   - Press hotkey again to stop

4. **Transcription happens automatically**
   - Text is transcribed
   - Copied to clipboard
   - Auto-pasted into your active window (if enabled)
   - Saved to history

### Interface Overview

#### Main Window
- **History Tab**: View, search, copy, or re-paste past transcriptions
- **Settings Tab**: Configure microphone, model, language, hotkey, behavior
- **About Tab**: Version info and features list

#### Recording Overlay
- Appears only when recording
- Shows:
  - 🔴 Recording indicator
  - ⏱️ Duration counter
  - 📊 Live audio waveform
  - Always on top of other windows

#### System Tray
- **Show VoiceSnap**: Open main window
- **Settings**: Quick access to settings
- **Quit**: Exit application

### Hotkey Modes

**Toggle Mode** (default):
- 1st press: Start recording
- 2nd press: Stop recording + transcribe

**Push-to-Talk Mode**:
- Hold hotkey: Record
- Release hotkey: Stop + transcribe

Change mode in Settings → Hotkey Settings

## ⚙️ Configuration

### Whisper Models

Choose speed vs. accuracy trade-off:

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| `tiny` | ~75 MB | ⚡⚡⚡ | ⭐⭐ | Quick notes, simple speech |
| `base` | ~150 MB | ⚡⚡ | ⭐⭐⭐ | **Recommended** - Best balance |
| `small` | ~500 MB | ⚡ | ⭐⭐⭐⭐ | Important transcriptions |
| `medium` | ~1.5 GB | 🐌 | ⭐⭐⭐⭐⭐ | High accuracy needed |
| `large` | ~3 GB | 🐌🐌 | ⭐⭐⭐⭐⭐⭐ | Professional use |

### Languages

VoiceSnap supports 99+ languages. Common ones:
- 🇫🇷 French (`fr`)
- 🇬🇧 English (`en`)
- 🇪🇸 Spanish (`es`)
- 🇩🇪 German (`de`)
- 🇮🇹 Italian (`it`)
- 🇵🇹 Portuguese (`pt`)
- 🇯🇵 Japanese (`ja`)
- 🇨🇳 Chinese (`zh`)
- 🇷🇺 Russian (`ru`)
- And many more...

Select "Auto-detect" to let Whisper identify the language.

### Custom Hotkey

Change hotkey in Settings → Hotkey Settings (Coming soon: interactive hotkey capture)

Edit config file manually: `~/.voicesnap/config.json`
```json
{
  "hotkey": {
    "modifiers": ["ctrl", "shift"],
    "key": "space",
    "toggle_mode": true
  }
}
```

## 🗂️ File Structure

```
~/.voicesnap/
├── config.json          # User configuration
├── data/
│   └── transcriptions.db # SQLite database
└── audio_cache/         # Saved recordings (optional)
```

## 🔧 Troubleshooting

### "No microphone found"
- Check system microphone permissions
- On macOS: System Preferences → Security & Privacy → Microphone
- Try selecting a different microphone in Settings

### "ffmpeg not found"
- Verify installation: `ffmpeg -version`
- Make sure ffmpeg is in your PATH
- Restart terminal/app after installing

### "Auto-paste doesn't work"
- On macOS: Grant Accessibility permissions
  - System Preferences → Security & Privacy → Accessibility → Add Python/VoiceSnap
- On Linux: Install `xdotool` for some environments
- Text is always copied to clipboard even if paste fails

### "Model download stuck"
- Check internet connection (only needed for first run)
- Whisper models are cached in `~/.cache/whisper/`
- Manually download from [OpenAI Whisper releases](https://github.com/openai/whisper)

### "App crashes on startup"
- Check Python version: `python3 --version` (needs 3.8+)
- Reinstall dependencies: `pip install -r requirements_v2.txt --force-reinstall`
- Check console output for specific errors

## 🏗️ Development

### Project Structure
```
voicesnap/
├── voicesnap_v2.py       # Main application entry point
├── voicesnap.py          # Legacy CLI version (v1)
├── src/
│   ├── config.py         # Configuration management
│   ├── database.py       # SQLite transcription history
│   ├── core/
│   │   ├── recorder.py   # Audio recording with waveform
│   │   ├── transcriber.py # Whisper transcription
│   │   └── hotkey_manager.py # Global hotkey handling
│   └── ui/
│       ├── main_window.py    # Main GUI window
│       ├── overlay.py        # Recording overlay
│       └── system_tray.py    # System tray icon
├── assets/
│   └── icon.png          # Application icon
├── requirements_v2.txt   # Python dependencies
└── README.md             # This file
```

### Running from Source
```bash
git clone https://github.com/Warllam/voicesnap.git
cd voicesnap
pip install -r requirements_v2.txt
python3 voicesnap_v2.py
```

### Building Standalone Executable
(Coming soon: PyInstaller scripts for .exe and .app)

## 🗺️ Roadmap

### v2.1 (Planned)
- [ ] Interactive hotkey capture in settings
- [ ] Export history to CSV/JSON
- [ ] Custom themes and colors
- [ ] Recording duration limit setting
- [ ] Pause/resume recording

### v2.5 (Future)
- [ ] Standalone executables (.exe for Windows, .app for macOS)
- [ ] Audio playback in history
- [ ] Multi-language UI
- [ ] Plugins system for post-processing

### v3.0 (Ideas)
- [ ] LLM integration for text formatting (Ollama)
- [ ] Prompt templates (professional, casual, code comments)
- [ ] Voice commands ("insert code", "format email")
- [ ] Cloud sync (optional, encrypted)

## 🤝 Contributing

Contributions welcome! Areas that need help:
- 🐛 Bug fixes
- 🌍 Translations
- 📚 Documentation
- ✨ Feature implementations
- 🧪 Testing on different platforms

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🙏 Acknowledgments

- **OpenAI Whisper** - Amazing open-source speech recognition
- **CustomTkinter** - Modern UI framework
- **SuperWhisper** - Inspiration for the UX

## 💬 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Warllam/voicesnap/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/Warllam/voicesnap/discussions)
- ⭐ **Star the repo** if you find it useful!

---

Made with ❤️ by [Warllam](https://github.com/Warllam)

**Privacy First** • **100% Local** • **Open Source**
