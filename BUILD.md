# Building VoiceSnap Standalone Executables

This guide explains how to create standalone executables for VoiceSnap on different platforms.

## Prerequisites

```bash
pip install pyinstaller
```

## Windows (.exe)

### Method 1: Simple Build

```bash
pyinstaller --onefile --windowed \
  --name VoiceSnap \
  --icon assets/icon.png \
  --add-data "src;src" \
  voicesnap_v2.py
```

### Method 2: Spec File (Recommended)

Create `VoiceSnap.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['voicesnap_v2.py'],
    pathex=[],
    binaries=[],
    datas=[('src', 'src'), ('assets', 'assets')],
    hiddenimports=['customtkinter', 'pystray', 'whisper', 'sounddevice'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='VoiceSnap',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,  # No console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.png',
)
```

Build:
```bash
pyinstaller VoiceSnap.spec
```

### Notes for Windows:
- ffmpeg.exe must be in PATH or bundled
- To bundle ffmpeg: `--add-binary "path/to/ffmpeg.exe;."`
- First run will still download Whisper models

## macOS (.app)

### Method 1: PyInstaller

```bash
pyinstaller --onefile --windowed \
  --name VoiceSnap \
  --icon assets/icon.png \
  --add-data "src:src" \
  --osx-bundle-identifier com.warllam.voicesnap \
  voicesnap_v2.py
```

### Method 2: py2app

Install:
```bash
pip install py2app
```

Create `setup.py`:
```python
from setuptools import setup

APP = ['voicesnap_v2.py']
DATA_FILES = [('src', ['src']), ('assets', ['assets'])]
OPTIONS = {
    'argv_emulation': True,
    'packages': ['customtkinter', 'whisper', 'sounddevice', 'pystray'],
    'includes': ['tkinter', 'PIL'],
    'iconfile': 'assets/icon.png',
    'plist': {
        'CFBundleName': 'VoiceSnap',
        'CFBundleDisplayName': 'VoiceSnap',
        'CFBundleIdentifier': 'com.warllam.voicesnap',
        'CFBundleVersion': '2.0.0',
        'CFBundleShortVersionString': '2.0.0',
        'NSMicrophoneUsageDescription': 'VoiceSnap needs microphone access for voice transcription',
        'NSHighResolutionCapable': True,
    },
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
```

Build:
```bash
python setup.py py2app
```

### macOS Permissions

Add to Info.plist:
```xml
<key>NSMicrophoneUsageDescription</key>
<string>VoiceSnap needs microphone access for voice transcription</string>
<key>NSAccessibilityUsageDescription</key>
<string>VoiceSnap needs accessibility access for auto-paste functionality</string>
```

### Code Signing (for distribution)

```bash
codesign --deep --force --verify --verbose \
  --sign "Developer ID Application: Your Name" \
  dist/VoiceSnap.app
```

### Notarization (for Gatekeeper)

```bash
# Create DMG
hdiutil create -volname VoiceSnap -srcfolder dist/VoiceSnap.app -ov -format UDZO VoiceSnap.dmg

# Notarize
xcrun notarytool submit VoiceSnap.dmg \
  --apple-id your@email.com \
  --team-id TEAMID \
  --password app-specific-password

# Staple
xcrun stapler staple VoiceSnap.dmg
```

## Linux (AppImage)

### Using PyInstaller + AppImage

1. Build with PyInstaller:
```bash
pyinstaller --onefile \
  --name VoiceSnap \
  --add-data "src:src" \
  voicesnap_v2.py
```

2. Create AppImage structure:
```bash
mkdir -p VoiceSnap.AppDir/usr/bin
mkdir -p VoiceSnap.AppDir/usr/share/icons
mkdir -p VoiceSnap.AppDir/usr/share/applications

cp dist/VoiceSnap VoiceSnap.AppDir/usr/bin/
cp assets/icon.png VoiceSnap.AppDir/usr/share/icons/voicesnap.png
```

3. Create desktop file (`VoiceSnap.AppDir/VoiceSnap.desktop`):
```ini
[Desktop Entry]
Type=Application
Name=VoiceSnap
Comment=Local voice-to-text transcription
Exec=VoiceSnap
Icon=voicesnap
Categories=Utility;Audio;
Terminal=false
```

4. Download and run appimagetool:
```bash
wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
chmod +x appimagetool-x86_64.AppImage
./appimagetool-x86_64.AppImage VoiceSnap.AppDir VoiceSnap-x86_64.AppImage
```

## Cross-Platform Considerations

### Whisper Models
- Models are NOT bundled (too large)
- First run downloads models (~150MB - 3GB depending on model)
- Models cached in user's home directory
- Document this in user guide

### ffmpeg Dependency
- Users must install ffmpeg separately
- Cannot easily bundle due to licensing
- Provide clear installation instructions per platform

### Configuration
- Stored in user's home directory (`~/.voicesnap/`)
- Survives app updates
- Not bundled with executable

### Audio Devices
- Detection is platform-specific
- Test on each platform
- Provide fallback to default device

## Testing Checklist

Before releasing built executables:

- [ ] App launches without errors
- [ ] Microphone detection works
- [ ] Hotkey registration works
- [ ] Recording overlay displays correctly
- [ ] Transcription completes successfully
- [ ] Auto-paste works
- [ ] History saves and loads
- [ ] Settings persist across restarts
- [ ] System tray icon appears
- [ ] Notifications work
- [ ] App quits cleanly
- [ ] No console window appears (Windows/macOS)
- [ ] Permissions requested (macOS)

## Distribution

### GitHub Releases

1. Create release on GitHub
2. Upload binaries:
   - `VoiceSnap-Windows.exe`
   - `VoiceSnap-macOS.dmg` or `.app.zip`
   - `VoiceSnap-Linux.AppImage`
3. Include installation instructions
4. Include SHA256 checksums

### File Sizes (Approximate)

- Windows .exe: 200-300 MB
- macOS .app: 250-350 MB
- Linux AppImage: 200-300 MB

(Large size due to bundling Python, CustomTkinter, PyTorch, etc.)

### Future: Reduce Size

Consider splitting into:
- Core app (small)
- Whisper models (separate download)
- User chooses model during setup

## Automated Builds

### GitHub Actions (example)

```yaml
name: Build Executables

on:
  release:
    types: [created]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements_v2.txt pyinstaller
      - run: pyinstaller VoiceSnap.spec
      - uses: actions/upload-artifact@v3
        with:
          name: VoiceSnap-Windows
          path: dist/VoiceSnap.exe

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements_v2.txt pyinstaller
      - run: pyinstaller VoiceSnap.spec
      - run: hdiutil create -volname VoiceSnap -srcfolder dist/VoiceSnap.app -ov -format UDZO VoiceSnap.dmg
      - uses: actions/upload-artifact@v3
        with:
          name: VoiceSnap-macOS
          path: VoiceSnap.dmg

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements_v2.txt pyinstaller
      - run: pyinstaller VoiceSnap.spec
      # ... AppImage steps ...
```

## Support

For build issues, check:
- PyInstaller documentation
- Platform-specific packaging guides
- VoiceSnap GitHub issues

---

**Note:** This is a work in progress. Contributions welcome!
