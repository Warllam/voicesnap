#!/bin/bash
# Quick start script for VoiceSnap v2

echo "🎤 VoiceSnap v2 - Starting..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

# Check ffmpeg
if ! command -v ffmpeg &> /dev/null; then
    echo "⚠️  ffmpeg not found!"
    echo "Install with:"
    echo "  macOS:   brew install ffmpeg"
    echo "  Linux:   sudo apt install ffmpeg"
    echo "  Windows: choco install ffmpeg"
    exit 1
fi

# Check if dependencies are installed
if ! python3 -c "import customtkinter" 2> /dev/null; then
    echo "📦 Installing dependencies..."
    pip install -r requirements_v2.txt
fi

# Run VoiceSnap
echo "🚀 Launching VoiceSnap v2..."
python3 voicesnap_v2.py
