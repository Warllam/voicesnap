#!/bin/bash

# VoiceSnap Tauri - Startup Script
# This script starts both the Python backend and Tauri frontend

set -e

echo "🎙️ Starting VoiceSnap Tauri Edition..."
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Install: sudo apt install python3 python3-pip"
    exit 1
fi

# Check if Node is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed!"
    echo "Install: https://nodejs.org/"
    exit 1
fi

# Check if dependencies are installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing Node dependencies..."
    npm install
fi

if [ ! -d "python/src" ]; then
    echo "❌ Python source files not found!"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping VoiceSnap..."
    kill $PYTHON_PID 2>/dev/null || true
    exit 0
}

trap cleanup INT TERM

# Start Python backend
echo "🐍 Starting Python backend server..."
cd python
python3 server.py &
PYTHON_PID=$!
cd ..

# Wait for Python server to be ready
echo "⏳ Waiting for backend server..."
for i in {1..30}; do
    if curl -s http://localhost:8765/health > /dev/null 2>&1; then
        echo "✅ Backend server is ready!"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Backend server failed to start!"
        kill $PYTHON_PID
        exit 1
    fi
    sleep 1
done

# Start Tauri dev mode
echo "🚀 Starting Tauri application..."
echo ""
npm run tauri:dev

# Cleanup when Tauri exits
cleanup
