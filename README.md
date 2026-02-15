# VoiceSnap

> Modern voice-to-text transcription with OpenAI Whisper

Local, private, and professional desktop application for speech-to-text transcription.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-3.0.0-blue.svg)](https://github.com/Warllam/voicesnap/releases)
[![Tauri](https://img.shields.io/badge/Tauri-2.x-blue.svg)](https://tauri.app/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)

## Version 3.0 - Tauri Edition

Complete rebuild with modern web technologies for a native desktop experience.

### Features

- **100% Local Processing** - All transcription happens on your machine
- **Modern UI** - React + TypeScript + Tailwind CSS
- **Real-time Waveform** - 60 FPS audio visualization
- **Global Hotkey** - Ctrl+Space works from anywhere
- **Multi-language** - Support for 99+ languages
- **Searchable History** - SQLite database with full-text search
- **Auto-paste** - Transcribed text automatically inserted
- **Native Performance** - Tauri + Rust backend

### Technology Stack

**Frontend:**
- React 18
- TypeScript
- Tailwind CSS
- Framer Motion (animations)
- Zustand (state management)

**Backend:**
- Tauri 2.x (Rust)
- Python 3.11+ (Flask bridge)
- OpenAI Whisper (transcription)
- SQLite (database)

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Rust (install from https://rustup.rs)
- FFmpeg

### Installation

```bash
# Clone the repository
git clone https://github.com/Warllam/voicesnap.git
cd voicesnap

# Checkout v3-tauri branch
git checkout v3-tauri

# Install Python dependencies
cd python
pip install -r requirements.txt
cd ..

# Install Node dependencies
npm install
```

### Running in Development

```bash
# Start the development environment
./start.sh
```

Or manually in two terminals:

```bash
# Terminal 1: Python backend
cd python
python server.py

# Terminal 2: Tauri frontend
npm run tauri:dev
```

### Building for Production

```bash
npm run tauri:build
```

Builds are created in `src-tauri/target/release/bundle/`:
- Windows: `.exe` and `.msi`
- macOS: `.dmg` and `.app`
- Linux: `.deb` and `.AppImage`

## Documentation

- **[Quick Start Guide](QUICKSTART.md)** - Get up and running in 5 minutes
- **[Technical Documentation](README_TAURI.md)** - Complete technical reference
- **[Migration Guide](MIGRATION.md)** - Upgrading from v2.x
- **[Changelog](CHANGELOG.md)** - Version history and release notes

## Usage

1. Launch the application
2. Press `Ctrl+Space` to start recording
3. Speak into your microphone
4. Press `Ctrl+Space` again to stop
5. Transcription is automatically copied and pasted

## Configuration

Configuration file: `~/.voicesnap/config.json`

Key settings:
- Audio device selection
- Whisper model (tiny/base/small/medium/large)
- Language preference
- Auto-paste behavior
- Theme (dark/light)

## Architecture

```
Frontend (React/Tauri) <-> HTTP Bridge (port 8765) <-> Python Backend (Whisper)
```

- **Frontend**: Modern web UI with Tauri
- **Bridge**: Flask HTTP server for IPC
- **Backend**: Python with Whisper AI for transcription

## Performance

- Bundle size: ~25 MB
- Startup time: ~2 seconds
- Memory usage: ~150 MB idle, ~500 MB during transcription
- UI framerate: 60 FPS
- Transcription speed: Depends on Whisper model (base: ~2x realtime)

## Troubleshooting

### Python server won't start
- Check Python version: `python --version` (need 3.11+)
- Install dependencies: `pip install -r python/requirements.txt`
- Check port 8765 is free: `lsof -i :8765`

### Whisper model not loading
- First run downloads model automatically (~150 MB for 'base')
- Models stored in `~/.cache/whisper/`
- Check internet connection and disk space

### Audio not recording
- Check microphone permissions in system settings
- Test device in Settings page
- Try different audio device

### Build fails
- Install system dependencies (Linux):
  ```bash
  sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev \
    librsvg2-dev patchelf
  ```
- Clear build cache: `rm -rf node_modules src-tauri/target && npm install`

## Roadmap

See [CHANGELOG.md](CHANGELOG.md) for planned features.

### v3.1 (Next Release)
- Light theme support
- Custom hotkey configuration
- Export functionality (JSON, CSV, TXT)
- Voice activity detection
- System tray enhancements

## Contributing

This is a personal project, but contributions are welcome!

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

- **OpenAI Whisper** - Speech recognition model
- **Tauri** - Desktop application framework
- **React** - UI framework
- Design inspiration: Discord, Linear, Raycast

## Support

- **GitHub Issues**: https://github.com/Warllam/voicesnap/issues
- **Documentation**: See README_TAURI.md
- **Author**: Warllam

---

**Made with modern web technologies for a native desktop experience**
