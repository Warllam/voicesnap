# VoiceSnap 🎤 v2.1 - Apple Edition

> **Beautiful, minimal, local voice-to-text** - Now with Apple-inspired design

Transform your voice into text instantly with OpenAI Whisper. 100% local, no cloud, no API keys. Now featuring a stunning Apple-style interface.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Version](https://img.shields.io/badge/version-2.1.0-blue.svg)](https://github.com/Warllam/voicesnap)

![VoiceSnap Apple Edition](assets/screenshot_apple.png)

## ✨ What's New in v2.1

### 🍎 Complete Apple-Inspired Redesign

**Ultra-minimal. Ultra-clean. Ultra-professional.**

- **Single-page layout** - No tabs, everything on one beautiful scrolling page
- **Apple Design System** - SF Pro fonts, precise colors (#007AFF blue), perfect spacing
- **Floating overlay** - Glassmorphism recording indicator with pulsing dot
- **Light/Dark modes** - Beautiful themes that match macOS
- **Smooth animations** - Butter-smooth 30 FPS, subtle transitions
- **Card-based history** - Clean transcription cards with soft shadows
- **Collapsible settings** - Accordion-style sections that expand when needed

### Before & After

| v2.0 (Old) | v2.1 (Apple Edition) |
|------------|----------------------|
| Dark theme by default | Light theme by default |
| 3 tabs navigation | Single scrolling page |
| Dense layout | Generous whitespace |
| Standard UI elements | Apple-style components |
| Busy interface | Minimal, focused |
| Full-screen overlay | Floating glassmorphism |

## 🚀 Quick Start

### Installation

```bash
# Clone the repo
git clone https://github.com/Warllam/voicesnap.git
cd voicesnap

# Install dependencies
pip install -r requirements_v2.txt

# Run Apple Edition
python3 voicesnap_apple.py
# or
./run_apple.sh
```

### First Use

1. **Launch VoiceSnap** - Window opens with light Apple-style theme
2. **Wait for model load** - Status shows "Ready • Model loaded" (first time downloads ~150MB)
3. **Press Ctrl+Space** - Floating overlay appears, recording starts
4. **Speak clearly** - Watch the minimal waveform animation
5. **Press Ctrl+Space again** - Recording stops, transcription happens
6. **Text auto-pastes** - Transcription appears where you're typing

## 🎨 Design Highlights

### Color Palette

**Light Theme** (default)
- Background: `#FFFFFF` (Pure white)
- Secondary: `#F5F5F7` (Light gray)
- Text: `#1D1D1F` (Near black)
- Accent: `#007AFF` (Apple blue)
- Success: `#34C759` (Green)
- Danger: `#FF3B30` (Red)

**Dark Theme**
- Background: `#1C1C1E` (Deep black)
- Secondary: `#2C2C2E` (Dark gray)
- Text: `#FFFFFF` (White)
- Accent: `#0A84FF` (Bright blue)

### Typography

- **Headers**: SF Pro Display (bold, 18-24pt)
- **Body**: SF Pro Text (regular, 13-14pt)
- **Metadata**: SF Pro Text (11pt, secondary color)
- **Fallbacks**: Segoe UI (Windows), system fonts (Linux)

### Spacing & Layout

- **Corner radius**: 12px (cards), 10px (buttons), 8px (inputs)
- **Padding**: 16px (cards), 20px (sections)
- **Margins**: 8px (between elements), 16px (between sections)
- **Card shadows**: Subtle `#00000008` blur

### Components

#### Transcription Cards
```
┌─────────────────────────────────────┐
│ 📅 Feb 15, 2025  •  ⏱ 3.2s  •  🌍 FR │  ← Metadata
├─────────────────────────────────────┤
│ This is the transcribed text...     │  ← Content
│                                     │
│ [Copy] [Paste]           [Delete]  │  ← Actions
└─────────────────────────────────────┘
```

#### Floating Overlay
```
┌──────────────────────────────────┐
│  ● 0:05  ▁▃▂▅▃▁▂▄▃▁▂▃▁  │  ← Glassmorphism
└──────────────────────────────────┘
   ↑    ↑         ↑
  Pulse Timer  Waveform
```

#### Collapsible Settings
```
▸ Audio                    ← Collapsed
▾ Whisper Model            ← Expanded
  ┌──────────────────────┐
  │ Model Size: base     │
  │ Language: French     │
  └──────────────────────┘
▸ Hotkey
▸ Behavior
```

## 📖 Features

### Core Features (from v2.0)

- ✅ **100% Local** - Zero cloud dependency, complete privacy
- ✅ **Global Hotkey** - Ctrl+Space from anywhere
- ✅ **Live Waveform** - Real-time audio visualization
- ✅ **AI Transcription** - OpenAI Whisper (state-of-the-art)
- ✅ **Auto-Paste** - Text appears where you're typing
- ✅ **Multi-Language** - 99+ languages supported
- ✅ **History** - Searchable SQLite database
- ✅ **System Tray** - Background operation
- ✅ **Cross-Platform** - Windows, macOS, Linux

### New in v2.1

- 🍎 **Apple Design** - Professional minimal aesthetic
- 🌓 **Theme Toggle** - Light/dark mode button in header
- 📜 **Single Page** - No tab navigation needed
- 🔍 **Smart Search** - Real-time history filtering
- 🎴 **Card Layout** - Clean transcription display
- 📁 **Collapsible Settings** - Expand only what you need
- ⏺️ **Floating Overlay** - Glassmorphism recording indicator
- 🎭 **Smooth Animations** - 30 FPS fluid motion

## ⚙️ Settings

### Audio

- **Microphone**: Select input device
- Auto-detects all system microphones
- Defaults to system default

### Whisper Model

| Model | Size | Speed | Accuracy | Best For |
|-------|------|-------|----------|----------|
| tiny | 75 MB | ⚡⚡⚡ | ⭐⭐ | Quick notes |
| **base** | 150 MB | ⚡⚡ | ⭐⭐⭐ | **Recommended** |
| small | 500 MB | ⚡ | ⭐⭐⭐⭐ | Important work |
| medium | 1.5 GB | 🐌 | ⭐⭐⭐⭐⭐ | High accuracy |
| large | 3 GB | 🐌🐌 | ⭐⭐⭐⭐⭐⭐ | Professional |

### Language

- **Auto-detect** (recommended) - Whisper identifies language
- **Manual**: French, English, Spanish, German, Italian, Portuguese, Japanese, Chinese, Russian, +90 more

### Hotkey

- **Default**: `Ctrl+Space`
- **Mode**: Toggle (press to start, press to stop)
- Customizable in config: `~/.voicesnap/config.json`

### Behavior

- ☑️ **Auto-paste after transcription** - Text inserts automatically
- ☑️ **Minimize to system tray** - Stays in background
- Text always copies to clipboard (even if auto-paste off)

## 🎨 Overlay Styles

Choose your overlay style in config:

### Floating (Default)
```json
{
  "ui": {
    "overlay_style": "floating",
    "overlay_position": "top"
  }
}
```
- Centered card (320x100px)
- Glassmorphism effect
- Pulsing recording dot
- Clean timer + waveform

### Bar
```json
{
  "ui": {
    "overlay_style": "bar",
    "overlay_position": "top"
  }
}
```
- Full-width bar
- Top or center position
- Minimal design
- More screen space

## 🗂️ File Structure

```
voicesnap/
├── voicesnap_apple.py       # v2.1 Apple Edition (main entry)
├── voicesnap_v2.py          # v2.0 legacy interface
├── voicesnap.py             # v1.0 CLI version
├── src/
│   ├── config.py            # Configuration management
│   ├── database.py          # SQLite history
│   ├── core/
│   │   ├── recorder.py      # Audio recording
│   │   ├── transcriber.py   # Whisper transcription
│   │   └── hotkey_manager.py # Global hotkey
│   └── ui/
│       ├── main_window_apple.py   # 🍎 Apple-style UI (v2.1)
│       ├── overlay_apple.py       # 🍎 Minimal overlay (v2.1)
│       ├── main_window.py         # v2.0 UI
│       ├── overlay.py             # v2.0 overlay
│       └── system_tray.py         # System tray icon
├── assets/
│   └── icon.png             # App icon
├── run_apple.sh             # Quick launcher
├── requirements_v2.txt      # Dependencies
├── CHANGELOG.md             # Version history
└── README_APPLE.md          # This file
```

## 🔧 Configuration

Config file: `~/.voicesnap/config.json`

```json
{
  "version": "2.1.0",
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "device_index": null,
    "max_duration": 120
  },
  "whisper": {
    "model": "base",
    "language": "fr",
    "task": "transcribe"
  },
  "hotkey": {
    "modifiers": ["ctrl"],
    "key": "space",
    "toggle_mode": true
  },
  "behavior": {
    "auto_paste": true,
    "copy_to_clipboard": true,
    "minimize_to_tray": true
  },
  "ui": {
    "theme": "light",
    "overlay_position": "top",
    "overlay_style": "floating",
    "show_notifications": true
  }
}
```

## 🐛 Troubleshooting

### App won't start
```bash
# Check Python version (needs 3.8+)
python3 --version

# Reinstall dependencies
pip install -r requirements_v2.txt --force-reinstall

# Check for errors
python3 voicesnap_apple.py
```

### Fonts look wrong
- **macOS**: SF Pro installed by default ✅
- **Windows**: Falls back to Segoe UI (looks great)
- **Linux**: Uses system sans-serif (install SF Pro for pixel-perfect)

### Overlay not showing
- Check if another app is blocking always-on-top windows
- Try changing overlay style in config (`"overlay_style": "bar"`)
- macOS: Grant accessibility permissions

### Theme toggle doesn't work
- Current limitation: Full theme refresh needs restart
- Basic toggle works, some elements update on next action
- Full dynamic theming coming in v2.2

## 🗺️ Roadmap

### v2.2 (Next)
- [ ] Full dynamic theme switching (no restart)
- [ ] Interactive hotkey capture in UI
- [ ] Export history (CSV, JSON, TXT)
- [ ] Custom color themes
- [ ] Keyboard shortcuts guide

### v2.5
- [ ] Standalone executables (.exe, .app)
- [ ] macOS native window chrome
- [ ] Windows 11 mica background
- [ ] Linux Wayland support improvements

### v3.0
- [ ] LLM post-processing (Ollama integration)
- [ ] Prompt templates (email, code, professional)
- [ ] Voice commands ("format this", "code style")
- [ ] Multi-window support
- [ ] Plugin system

## 🤝 Contributing

Love the design? Want to improve it?

**Ways to contribute:**
- 🎨 Design improvements and refinements
- 🐛 Bug reports and fixes
- 🌍 Translations (UI localization)
- 📚 Documentation
- ✨ New features

**Design principles:**
- Minimal over maximal
- Whitespace is your friend
- Subtle animations only
- Respect Apple HIG (Human Interface Guidelines)
- Accessibility first

## 📄 License

MIT License - See [LICENSE](LICENSE)

## 🙏 Credits

- **OpenAI Whisper** - Incredible speech recognition
- **CustomTkinter** - Modern Python UI framework
- **Apple** - Design inspiration (no affiliation)
- **SuperWhisper** - UX inspiration
- **Linear** - Minimalist aesthetic

## 💬 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/Warllam/voicesnap/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/Warllam/voicesnap/discussions)
- ⭐ **Star the repo** if you love the redesign!

---

Made with ❤️ and attention to detail by [Warllam](https://github.com/Warllam)

**Privacy First** • **100% Local** • **Apple-Beautiful** • **Open Source**

---

## Screenshots

### Main Window (Light Theme)
![Main Window Light](assets/screenshot_main_light.png)

### Recording Overlay (Floating)
![Overlay Floating](assets/screenshot_overlay_floating.png)

### Dark Mode
![Dark Mode](assets/screenshot_dark.png)

### Collapsible Settings
![Settings](assets/screenshot_settings.png)

---

**Tip**: Press `Cmd/Ctrl + +` to make VoiceSnap even more beautiful with larger text!
