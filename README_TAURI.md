# VoiceSnap Tauri Edition 🎙️✨

**Version 3.0.0** - Modern Voice Transcription with React + Tauri

Complete rebuild of VoiceSnap with a beautiful, modern UI built with:
- **Frontend**: React 18 + TypeScript + Tailwind CSS + Framer Motion
- **Backend**: Tauri 2.x (Rust) + Python (Whisper AI)
- **Design**: Discord/Linear/Raycast-inspired modern dark theme

---

## 🚀 Features

### ✨ Modern UI
- **Sidebar Navigation** - Discord-style icon sidebar with smooth animations
- **Glassmorphism Overlay** - Floating recording overlay at the top center
- **Real-time Waveform** - 60 FPS synchronized audio visualization
- **Dark Theme** - Beautiful GitHub Dark-inspired color palette
- **Smooth Animations** - Framer Motion for buttery-smooth transitions

### 🎯 Core Functionality
- **Global Hotkey** - `Ctrl+Space` to record from anywhere
- **Whisper AI** - Local transcription with OpenAI Whisper
- **Multi-language** - Support for 99+ languages
- **Auto-paste** - Transcribed text automatically pasted
- **Transcription History** - Searchable database with SQLite
- **Audio Devices** - Choose your microphone
- **Multiple Models** - tiny/base/small/medium/large Whisper models

---

## 📦 Installation

### Prerequisites

**1. System Requirements**
- Python 3.11+
- Node.js 18+
- Rust (for Tauri)
- FFmpeg (for audio processing)

**2. Install Rust** (if not already installed)
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**3. Install FFmpeg**
```bash
# Ubuntu/Debian
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows (use Scoop or Chocolatey)
scoop install ffmpeg
```

### Setup

**1. Clone the repository**
```bash
cd /home/warllam/clawd/voicesnap-tauri
```

**2. Install Python dependencies**
```bash
cd python
pip install -r requirements.txt
```

**3. Install Node dependencies**
```bash
cd ..
npm install
```

---

## 🏃 Running the App

### Development Mode

**Terminal 1: Start Python backend**
```bash
cd python
python server.py
```

The server will start on `http://localhost:8765`

**Terminal 2: Start Tauri dev mode**
```bash
npm run tauri:dev
```

This will:
1. Start Vite dev server on `http://localhost:1420`
2. Launch the Tauri window
3. Enable hot-reload for frontend changes

### Production Build

**Build the app**
```bash
npm run tauri:build
```

This creates:
- **Linux**: `.deb`, `.AppImage` in `src-tauri/target/release/bundle/`
- **Windows**: `.exe`, `.msi` in `src-tauri/target/release/bundle/`
- **macOS**: `.dmg`, `.app` in `src-tauri/target/release/bundle/`

---

## 🎨 Design Features

### Color Palette
- **Background**: `#0d1117` (GitHub dark)
- **Surface**: `#1f1f1f`
- **Surface Elevated**: `#2d2d2d`
- **Accent**: `#6366f1` (Indigo)
- **Text**: `#e5e5e5`
- **Text Muted**: `#8b949e`

### UI Components

**Sidebar (60px)**
- Icon-only navigation
- Active state indicator
- Smooth transitions
- Tooltips on hover

**Recording Overlay**
- Centered at top (~50px from top)
- Glassmorphism effect (backdrop-blur)
- Pulsing red dot when recording
- Real-time waveform visualization
- Timer display
- Stop button

**Transcription Cards**
- Modern card design with hover effects
- Metadata (timestamp, duration, language)
- Actions (copy, delete) visible on hover
- Smooth animations (fade in, slide)

**Settings Page**
- Organized sections with icons
- Modern dropdowns and toggles
- Generous spacing
- Clear visual hierarchy

### Animations
- Page transitions: 200ms fade + slide
- Button hover: 50ms scale
- Card hover: border color + shadow
- Waveform: 60 FPS canvas animation

---

## 🛠️ Architecture

### Frontend → Backend Communication

**Tauri IPC Commands** (Rust)
```rust
start_recording()       // Start audio recording
stop_recording()        // Stop and transcribe
get_transcriptions()    // Fetch history
delete_transcription()  // Delete entry
get_config()            // Get settings
update_config()         // Update settings
get_audio_devices()     // List microphones
```

**Python HTTP Server** (`localhost:8765`)
```
GET  /health                     // Health check
POST /api/recording/start        // Start recording
POST /api/recording/stop         // Stop & transcribe
GET  /api/recording/waveform     // Waveform data
GET  /api/devices                // Audio devices
GET  /api/transcriptions         // History
DELETE /api/transcriptions/:id   // Delete
GET  /api/config                 // Get config
POST /api/config                 // Update config
```

### File Structure
```
voicesnap-tauri/
├── src/                        # React frontend
│   ├── components/
│   │   ├── Sidebar.tsx
│   │   ├── RecordingOverlay.tsx
│   │   ├── Waveform.tsx
│   │   └── TranscriptionCard.tsx
│   ├── pages/
│   │   ├── TranscriptionsPage.tsx
│   │   ├── SettingsPage.tsx
│   │   └── AboutPage.tsx
│   ├── lib/
│   │   ├── api.ts             # Tauri invoke wrappers
│   │   └── utils.ts           # Helper functions
│   ├── store/
│   │   └── useAppStore.ts     # Zustand state
│   ├── App.tsx
│   └── main.tsx
├── src-tauri/                  # Rust backend
│   ├── src/main.rs            # Tauri commands
│   └── tauri.conf.json        # Tauri config
├── python/                     # Python backend
│   ├── server.py              # Flask HTTP server
│   ├── src/
│   │   ├── core/
│   │   │   ├── recorder.py    # Audio recording
│   │   │   ├── transcriber.py # Whisper AI
│   │   │   └── hotkey_manager.py
│   │   ├── database.py        # SQLite
│   │   └── config.py          # Config manager
│   └── requirements.txt
└── package.json
```

---

## ⚙️ Configuration

Config file location: `~/.voicesnap/config.json`

**Default settings:**
```json
{
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
    "theme": "dark",
    "overlay_position": "center"
  }
}
```

---

## 🐛 Troubleshooting

### Python server won't start
- Check Python version: `python --version` (need 3.11+)
- Install dependencies: `pip install -r python/requirements.txt`
- Check port 8765 is free: `lsof -i :8765`

### Whisper model not loading
- First run downloads the model (~150 MB for 'base')
- Check internet connection
- Check disk space
- Models stored in `~/.cache/whisper/`

### Audio not recording
- Check microphone permissions
- Test device in Settings page
- Check `audio.device_index` in config
- Try different audio device

### Waveform not showing
- WebSocket connection to backend
- Check browser console for errors
- Make sure Python server is running

### Build fails
- Install Rust: `curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh`
- Install build deps: `sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf`
- Clear build cache: `rm -rf node_modules src-tauri/target && npm install`

---

## 🎯 Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Space` | Start/Stop recording (global) |

---

## 📊 Performance

- **Bundle size**: < 30 MB (Tauri binary + frontend)
- **Memory usage**: ~150 MB idle, ~500 MB during transcription
- **Waveform**: 60 FPS smooth canvas animation
- **Startup time**: < 2 seconds

---

## 🚀 Roadmap v3.1

- [ ] Light theme support
- [ ] Custom hotkey configuration
- [ ] Export transcriptions (JSON, CSV, TXT)
- [ ] Voice activity detection (auto-start/stop)
- [ ] Multi-language UI (i18n)
- [ ] macOS/Windows installers
- [ ] System tray menu
- [ ] Notification sounds

---

## 🤝 Contributing

This is a personal project but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🙏 Credits

- **Whisper AI** - OpenAI
- **Tauri** - The Tauri team
- **Design inspiration** - Discord, Linear, Raycast, Spotify

---

## 📞 Support

- **GitHub Issues**: https://github.com/Warllam/voicesnap/issues
- **Author**: Warllam

---

**Made with ❤️ and modern web technologies**
