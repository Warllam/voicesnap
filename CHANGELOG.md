# Changelog

All notable changes to VoiceSnap will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2025-02-15

### 🍎 Apple-Inspired Redesign - Professional Polish

Complete UI/UX overhaul with Apple's design language. Ultra-clean, minimal, and elegant.

### Added

#### Visual Design
- **Apple Design System Colors**
  - Light theme: Pure white (#FFFFFF), subtle grays (#F5F5F7)
  - Dark theme: Deep blacks (#1C1C1E), warm grays
  - Accent: Apple Blue (#007AFF)
  - System fonts: SF Pro Display/Text (macOS), Segoe UI (Windows)
  
- **Single-Page Layout** (No Tabs!)
  - Vertical scrolling layout
  - Everything accessible on one screen
  - Collapsible settings sections
  - Generous whitespace and spacing
  - Clean visual hierarchy
  
- **Transcription Cards**
  - Soft rounded corners (12px radius)
  - Subtle shadows and borders
  - Metadata badges (timestamp, duration, language)
  - Inline actions (Copy, Paste, Delete)
  - Clean typography with SF Pro fonts
  
- **Search Bar**
  - Minimal rounded design
  - Real-time filtering
  - Integrated search icon
  - Smooth interactions

#### Recording Overlay
- **Two Styles Available**
  - `floating`: Centered card with glassmorphism effect (320x100px)
  - `bar`: Full-width minimal bar at top/center
  
- **Apple-Style Elements**
  - Pulsing recording dot (subtle animation)
  - Clean timer display (MM:SS format)
  - Minimal waveform visualization (bar style)
  - Translucent background with blur effect
  - Soft rounded corners
  
- **Smooth Animations**
  - 30 FPS fluid animations
  - Pulsing dot with sine wave
  - Fade in/out transitions
  - Responsive to audio levels

#### Settings UI
- **Collapsible Sections** (Accordion Style)
  - Audio settings
  - Whisper model configuration
  - Hotkey display
  - Behavior toggles
  - Expand/collapse with smooth animations
  
- **Improved Layout**
  - Clear section headers
  - Descriptive help text
  - Inline model information
  - Better spacing between elements

#### Theme System
- **Light/Dark Mode Toggle**
  - Button in header (🌙 / ☀️)
  - Smooth theme transitions
  - Persists across sessions
  - Respects system preferences
  
- **Consistent Color Palette**
  - All UI elements follow theme
  - Overlay syncs with main window theme
  - Accessible contrast ratios
  - Apple-accurate colors

#### Status & Feedback
- **Refined Status Bar**
  - Green dot indicator (● Ready)
  - Minimalist text formatting
  - Context-aware messages
  - Version badge

### Changed

#### UI/UX Improvements
- **Removed Tab Navigation** - Single scrollable page is cleaner
- **Improved Button Styles** - Rounded, minimal, with hover effects
- **Better Spacing** - More breathing room, less cluttered
- **Enhanced Typography** - SF Pro fonts, clear hierarchy
- **Refined Colors** - Softer palette, no harsh contrasts
- **Smoother Interactions** - Better hover states and transitions

#### Component Architecture
- New `main_window_apple.py` with Apple-style components
- New `overlay_apple.py` with glassmorphism overlay
- New `voicesnap_apple.py` main entry point
- Custom `AppleButton` component class
- `TranscriptionCard` component for clean history display
- `CollapsibleSection` component for settings

#### Performance
- Optimized overlay animations (30 FPS)
- Reduced UI complexity for better responsiveness
- Lazy loading for heavy components
- Efficient redraw logic

### Technical Details

#### New Files
```
src/ui/
├── main_window_apple.py    # Apple-style main window (26KB)
└── overlay_apple.py         # Minimal overlay with glassmorphism (12KB)

voicesnap_apple.py           # v2.1 main entry point (15KB)
run_apple.sh                 # Launcher script
```

#### Design Specifications
- **Colors**: Apple's exact HEX values (#007AFF, #FF3B30, etc.)
- **Corner Radius**: 8-12px for cards, 6px for buttons
- **Shadows**: Subtle (#00000008 for light theme)
- **Fonts**: SF Pro Display (headers), SF Pro Text (body)
- **Spacing**: Multiples of 4px (8, 12, 16, 24)
- **Animation**: ease-in-out, ~300ms transitions

#### Inspiration
- macOS Big Sur+ design language
- iOS Settings app structure
- Apple Music cards
- Linear.app minimalism
- Notion clean layouts

### Compatibility

- ✅ Backward compatible with v2.0 config files
- ✅ Same backend (recorder, transcriber unchanged)
- ✅ Cross-platform (Windows/macOS/Linux)
- ✅ All v2.0 features retained
- ✅ Can run alongside v2.0 (`voicesnap_v2.py` still available)

### Known Limitations

- Full theme refresh requires app restart (partial refresh works)
- Glassmorphism effect varies by platform (best on macOS)
- SF Pro fonts auto-fallback to system fonts on non-Apple platforms

### Migration

Run the new Apple edition:
```bash
python3 voicesnap_apple.py
# or
./run_apple.sh
```

Legacy v2.0 interface still available:
```bash
python3 voicesnap_v2.py
```

---

## [2.0.0] - 2025-02-13

### 🎉 Major Release - Complete Desktop Application

VoiceSnap v2 is a complete rewrite with a modern desktop interface, inspired by SuperWhisper.

### Added

#### Core Features
- **Global Hotkey System**
  - Toggle mode (press once to start, again to stop)
  - Push-to-talk mode (hold to record, release to stop)
  - Default hotkey: `Ctrl+Space`
  - Customizable via config file
  
- **Recording Overlay**
  - Minimal, always-on-top overlay during recording
  - Real-time audio waveform visualization
  - Recording duration counter
  - Red recording indicator dot
  - Configurable position (top/bottom of screen)
  
- **Desktop GUI** (CustomTkinter)
  - Main window with tabbed interface
  - History tab with searchable transcriptions
  - Settings tab for configuration
  - About tab with app information
  - Modern dark theme
  
- **Transcription History**
  - SQLite database for persistent storage
  - Full-text search with FTS5
  - Displays: timestamp, duration, detected language
  - Actions: Copy, Paste, Delete
  - Stores up to unlimited transcriptions
  
- **System Tray Integration**
  - App runs in background
  - Tray icon changes when recording (red dot)
  - Context menu: Show, Settings, Quit
  - Desktop notifications for completed transcriptions
  - Minimize to tray option

#### Configuration
- **JSON Configuration File** (`~/.voicesnap/config.json`)
  - Audio settings (sample rate, device selection)
  - Whisper settings (model, language, task)
  - Hotkey configuration
  - Behavior settings (auto-paste, minimize to tray)
  - UI settings (theme, overlay position)
  
- **Settings UI**
  - Microphone selection dropdown
  - Whisper model selection (tiny/base/small/medium/large)
  - Language selection (Auto-detect or 19+ languages)
  - Auto-paste toggle
  - Minimize to tray toggle

#### Audio & Transcription
- **Enhanced Audio Recorder**
  - Real-time waveform data for visualization
  - Configurable sample rate and channels
  - Max duration limit (default 120s)
  - Audio caching option
  - Device selection support
  
- **Whisper Transcriber**
  - Background model loading
  - Progress callbacks for UI updates
  - Support for all Whisper models
  - Language auto-detection
  - Segment information with timestamps
  - Audio file caching

#### Workflow
- **Auto-Paste Mode**
  - Transcription automatically pasted into active window
  - Cross-platform keyboard simulation (Ctrl+V / Cmd+V)
  - Optional clipboard-only mode
  
- **Smart Clipboard**
  - Always copies to clipboard (backup)
  - Works even if auto-paste fails
  - Manual paste available from history

### Technical Improvements

- **Modular Architecture**
  - Separated core logic from UI
  - Clean separation of concerns
  - Easy to extend and maintain
  
- **Database**
  - SQLite with full-text search (FTS5)
  - Indexed queries for performance
  - Automatic schema creation
  - Migration support for future versions
  
- **Threading**
  - Non-blocking UI operations
  - Background model loading
  - Async transcription
  - Smooth waveform animation
  
- **Cross-Platform Support**
  - Tested on Linux, macOS, Windows
  - Platform-specific hotkey handling
  - Adaptive keyboard shortcuts
  - System tray icons

### Developer Experience

- **Clean Codebase**
  - Type hints throughout
  - Comprehensive docstrings
  - Organized module structure
  - Easy to read and contribute to
  
- **Configuration System**
  - Default config with sensible values
  - Automatic config file creation
  - Backwards-compatible config loading
  - Dot notation for nested settings

### Files Added

```
src/
├── __init__.py
├── config.py              # Configuration management
├── database.py            # SQLite history database
├── core/
│   ├── __init__.py
│   ├── recorder.py        # Audio recording
│   ├── transcriber.py     # Whisper transcription
│   └── hotkey_manager.py  # Global hotkey handling
└── ui/
    ├── __init__.py
    ├── main_window.py     # Main GUI
    ├── overlay.py         # Recording overlay
    └── system_tray.py     # System tray icon

voicesnap_v2.py            # Main application
requirements_v2.txt        # V2 dependencies
assets/
├── icon.png               # App icon
└── create_icon.py         # Icon generator
```

### Dependencies Added

- `customtkinter` - Modern UI framework
- `pystray` - System tray integration  
- `pillow` - Icon image processing
- `python-dotenv` - Environment variable support
- `pyobjc-framework-Cocoa` - macOS integration (macOS only)
- `pywin32` - Windows integration (Windows only)

### Changed

- Reorganized project structure (v1 CLI kept as `voicesnap.py`)
- Updated README with comprehensive v2 documentation
- Improved error handling throughout
- Better user feedback (status messages, notifications)

### Known Issues

- Hotkey change UI not yet implemented (can edit config file manually)
- No standalone executable builds yet (planned for v2.1)
- First model load requires internet connection (Whisper model download)

### Migration from v1

V1 (CLI) is still available as `voicesnap.py`. V2 is the new default with `voicesnap_v2.py`.

To migrate:
1. Install new dependencies: `pip install -r requirements_v2.txt`
2. Run v2: `python3 voicesnap_v2.py`
3. V1 history is not automatically imported (both versions can coexist)

---

## [1.0.0] - 2024-XX-XX

### Initial Release - CLI Version

- Basic CLI voice-to-text transcription
- Hotkey: `Ctrl+Shift+Space` (hold to record)
- Auto-paste after transcription
- Whisper integration (base model)
- Cross-platform support
- Simple and lightweight

### Features

- Push-to-talk recording with global hotkey
- Whisper transcription (local)
- Automatic clipboard copy
- Auto-paste with keyboard simulation
- No dependencies on cloud services
- French language support

---

## Version History

- **v2.0.0** - Desktop app with GUI, history, overlay (Current)
- **v1.0.0** - CLI version (Legacy, still available)

---

[2.0.0]: https://github.com/Warllam/voicesnap/releases/tag/v2.0.0
[1.0.0]: https://github.com/Warllam/voicesnap/releases/tag/v1.0.0
