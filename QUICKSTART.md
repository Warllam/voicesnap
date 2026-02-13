# VoiceSnap v2 - Quick Start Guide

Get up and running with VoiceSnap in 5 minutes!

## 🎯 What is VoiceSnap?

VoiceSnap is a **local voice-to-text transcription app** that works 100% offline. No cloud, no API keys, no subscriptions. Just press a hotkey, speak, and your words appear as text.

Think of it as a free, open-source alternative to SuperWhisper.

## 🚀 Installation (3 Steps)

### Step 1: Install Prerequisites

**ffmpeg** (required for audio processing):

```bash
# macOS
brew install ffmpeg

# Linux (Ubuntu/Debian)
sudo apt update && sudo apt install ffmpeg

# Windows
choco install ffmpeg
# or download from https://ffmpeg.org/download.html
```

**Python 3.8+** (check if you have it):
```bash
python3 --version
```

### Step 2: Clone & Install

```bash
# Clone repository
git clone https://github.com/Warllam/voicesnap.git
cd voicesnap

# Install Python dependencies
pip install -r requirements_v2.txt

# Wait a few minutes for PyTorch, Whisper, etc. to install
```

### Step 3: Run VoiceSnap

```bash
# Quick start script
./run.sh

# Or directly
python3 voicesnap_v2.py
```

**First launch**: Whisper will download the model (~150MB). This happens once.

## 🎤 Usage

### Basic Workflow

1. **Launch VoiceSnap**
   - The main window appears
   - Wait for "Model loaded" in status bar
   - You can minimize to tray

2. **Press Hotkey** (default: `Ctrl+Space`)
   - Recording overlay appears at top of screen
   - See waveform animation and timer
   - Speak clearly into your microphone

3. **Press Hotkey Again** to stop
   - Overlay disappears
   - Transcription happens (a few seconds)
   - Text is auto-pasted where you were typing!

4. **View History**
   - All transcriptions saved in History tab
   - Search, copy, or re-paste old transcriptions

### Tips for Best Results

✅ **DO:**
- Speak clearly and at normal pace
- Use a decent microphone (built-in is fine)
- Keep recordings under 30 seconds for fast results
- Check your language setting matches what you're speaking

❌ **DON'T:**
- Speak too fast or mumble
- Record in very noisy environments
- Expect perfect transcription (it's AI, not magic)
- Use for real-time conversations (latency is 3-10s)

## ⚙️ Settings

### Change Whisper Model

**Settings Tab → Model**

- `tiny` - ⚡ Super fast, lower accuracy (casual notes)
- `base` - ⚡ Fast, good accuracy (default, recommended)
- `small` - Medium speed, better accuracy
- `medium` - Slower, high accuracy
- `large` - Very slow, best accuracy (professional use)

First time switching downloads the new model.

### Change Language

**Settings Tab → Language**

Select your language or use "Auto-detect". Supports:
- French, English, Spanish, German, Italian, Portuguese
- Japanese, Chinese, Korean, Russian, Arabic, Turkish
- And 80+ more languages!

### Change Hotkey

**Current:** Edit `~/.voicesnap/config.json` manually:

```json
{
  "hotkey": {
    "modifiers": ["ctrl", "shift"],
    "key": "space",
    "toggle_mode": true
  }
}
```

**Coming soon:** Interactive hotkey capture in Settings UI.

### Disable Auto-Paste

**Settings Tab → Behavior**

Uncheck "Auto-paste transcription into active window"

Transcription will only copy to clipboard. You manually paste with Ctrl+V.

## 🗂️ Where Are My Files?

### Configuration & Data

All files stored in: `~/.voicesnap/`

```
~/.voicesnap/
├── config.json              # Your settings
├── data/
│   └── transcriptions.db    # History database
└── audio_cache/             # Saved recordings (if enabled)
```

### Whisper Models

Cached by Whisper itself: `~/.cache/whisper/`

## 🔧 Troubleshooting

### "Model not loading" / Stuck on startup

**Solution:**
- Check internet connection (first run only)
- Try smaller model (Settings → Model → tiny)
- Delete `~/.cache/whisper/` and restart (re-downloads model)

### "No microphone found"

**Solution:**
- Check system microphone permissions
- **macOS:** System Preferences → Security → Privacy → Microphone → Add Python/VoiceSnap
- **Linux:** Check `arecord -l` shows your mic
- Try different microphone in Settings tab

### "Hotkey doesn't work"

**Solution:**
- Check another app isn't using the same hotkey
- Try different hotkey combination
- **macOS:** Grant Accessibility permissions (System Preferences → Security → Accessibility)
- **Linux:** Some DEs block global hotkeys (try running with sudo or use custom hotkey)

### "Auto-paste doesn't work"

**Solution:**
- On **macOS:** Grant Accessibility permissions
- On **Linux:** Install `xdotool` if needed
- Text is always copied to clipboard - you can manually paste with Ctrl+V
- Disable auto-paste in Settings if it's problematic

### "Transcription is wrong/bad"

**Solutions:**
- Try larger model (Settings → Model → small or medium)
- Check language setting matches what you spoke
- Speak more clearly and slowly
- Reduce background noise
- Try recording shorter clips
- Some accents/dialects may work better than others

### "App crashes"

**Solution:**
1. Run from terminal to see error:
   ```bash
   python3 voicesnap_v2.py
   ```
2. Check all dependencies installed:
   ```bash
   python3 test_install.py
   ```
3. Report issue on GitHub with error message

## 📊 Performance

### Model Comparison (approximate)

| Model | Download Size | Memory Usage | CPU Time (10s audio) |
|-------|---------------|--------------|----------------------|
| tiny  | 75 MB         | ~1 GB RAM    | ~2 seconds           |
| base  | 150 MB        | ~1 GB RAM    | ~3 seconds           |
| small | 500 MB        | ~2 GB RAM    | ~10 seconds          |
| medium| 1.5 GB        | ~5 GB RAM    | ~30 seconds          |
| large | 3 GB          | ~10 GB RAM   | ~60 seconds          |

*Times vary by CPU. GPU not required but speeds things up if available.*

### Disk Space

- App + dependencies: ~1-2 GB
- Whisper models: 75 MB - 3 GB (depending on model)
- History database: Grows over time (~1 MB per 1000 transcriptions)

## 🎓 Next Steps

### Customize Your Experience

- Experiment with different models
- Try different languages
- Set custom hotkey
- Explore history search

### Advanced

- Read [BUILD.md](BUILD.md) to create standalone executables
- Check `~/.voicesnap/config.json` for all settings
- Contribute to the project on GitHub

### Get Help

- 📖 [Full README](README.md)
- 🐛 [Report bugs](https://github.com/Warllam/voicesnap/issues)
- 💬 [Discussions](https://github.com/Warllam/voicesnap/discussions)

## 🎉 You're Ready!

Press `Ctrl+Space`, speak, and watch your words appear. Enjoy! 🎤✨

---

**Questions?** Check the [full README](README.md) or open an issue on GitHub.
