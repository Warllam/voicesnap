# Changelog

All notable changes to VoiceSnap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.0] - 2026-02-15

### Added
- Complete rebuild with Tauri 2.x + React 18 + TypeScript
- Modern sidebar navigation (Discord-style, 60px icon bar)
- Glassmorphism recording overlay (centered at top)
- Real-time audio waveform visualization (60 FPS Canvas)
- Dark theme with Framer Motion animations
- Smooth page transitions and micro-interactions
- Search functionality in transcription history
- Better error handling and user feedback
- Comprehensive documentation (README_TAURI.md, QUICKSTART.md)
- Development startup script (start.sh)
- Migration guide from v2.x

### Changed
- **BREAKING**: UI framework changed from CustomTkinter to React/Tauri
- Frontend now uses React 18 + TypeScript + Tailwind CSS
- Backend communication via HTTP bridge (Flask on port 8765)
- Improved performance: 60 FPS UI, ~2s startup time
- Reduced bundle size: ~25 MB (vs ~50 MB in v2)
- Better memory usage: ~150 MB idle (vs ~200 MB in v2)

### Deprecated
- Python CustomTkinter UI (replaced by React)
- Direct Python UI bindings (now HTTP API)

### Removed
- CustomTkinter dependency
- Tkinter themes
- Old overlay implementations

### Fixed
- Waveform now truly synchronized with microphone input
- Recording overlay properly centered at top of screen
- Device list filtered to show only input devices
- Hotkey toggle works reliably in all scenarios

### Security
- All transcription still happens locally (no cloud)
- HTTP bridge only accessible on localhost
- No data exfiltration or external API calls

## [2.1.0] - 2026-02-13

### Added
- Apple-inspired redesign with CustomTkinter
- Single-page scrollable layout
- Theme toggle (light/dark)
- Collapsible settings sections
- Real-time search in transcriptions

### Changed
- Redesigned main window with generous whitespace
- Improved card-based transcription list
- Better visual hierarchy

### Fixed
- Initialization order bug in main window
- Hotkey toggle reliability
- Waveform display issues
- Audio device filtering

## [2.0.0] - 2026-02-12

### Added
- Desktop application with CustomTkinter
- Main window with tabs (History, Settings, About)
- Recording overlay with waveform
- System tray integration
- SQLite database for transcription history
- Config management with JSON
- Audio device selection
- Hotkey management
- Auto-paste functionality

### Changed
- Migrated from CLI to desktop GUI
- Added persistent configuration
- Improved audio handling

## [1.0.0] - 2026-02-07

### Added
- Initial CLI version
- Basic Whisper transcription
- Hotkey support (Ctrl+Shift+Space)
- Simple recording and transcription workflow
- Command-line interface

---

## Migration Guides

### v2.x to v3.0
See [MIGRATION.md](MIGRATION.md) for detailed migration instructions.

**Key points:**
- Database and config files are 100% compatible
- No data migration needed
- Install Node.js and Rust for v3.0
- Run `./start.sh` or follow QUICKSTART.md

### v1.x to v2.0
- Config moved to `~/.voicesnap/config.json`
- Database added at `~/.voicesnap/data/transcriptions.db`
- Install CustomTkinter: `pip install customtkinter`

---

## Roadmap

### v3.1 (Planned)
- [ ] Light theme support
- [ ] Custom hotkey configuration UI
- [ ] Export transcriptions (JSON, CSV, TXT)
- [ ] Voice activity detection (auto-start/stop)
- [ ] Multi-language UI (i18n)
- [ ] macOS/Windows installers
- [ ] System tray menu improvements
- [ ] Notification sounds

### v3.2 (Future)
- [ ] Cloud sync (optional, encrypted)
- [ ] Plugin system
- [ ] Custom models support
- [ ] Real-time streaming transcription
- [ ] Speaker diarization
- [ ] Timestamps in transcriptions

---

## Support

- **GitHub Issues**: https://github.com/Warllam/voicesnap/issues
- **Documentation**: See README_TAURI.md
- **Quick Start**: See QUICKSTART.md
