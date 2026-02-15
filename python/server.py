"""HTTP server bridge for Tauri frontend"""

import os
import sys
import json
import asyncio
import threading
from pathlib import Path
from typing import Optional, Dict, Any
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from src.core.recorder import AudioRecorder
from src.core.transcriber import Transcriber
from src.database import TranscriptionDB
from src.config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Tauri

# Global instances
config: Optional[Config] = None
recorder: Optional[AudioRecorder] = None
transcriber: Optional[Transcriber] = None
db: Optional[TranscriptionDB] = None

# Recording state
is_recording = False
current_audio = None
waveform_data_buffer = []

def init_app():
    """Initialize application components"""
    global config, recorder, transcriber, db
    
    # Load config
    config = Config()
    
    # Initialize database
    db_path = config.get_data_dir() / "transcriptions.db"
    db = TranscriptionDB(str(db_path))
    
    # Initialize recorder
    sample_rate = config.get("audio.sample_rate", 16000)
    channels = config.get("audio.channels", 1)
    device_index = config.get("audio.device_index")
    max_duration = config.get("audio.max_duration", 120)
    
    recorder = AudioRecorder(
        sample_rate=sample_rate,
        channels=channels,
        device_index=device_index,
        max_duration=max_duration
    )
    
    # Set waveform callback
    def waveform_callback(data):
        global waveform_data_buffer
        # Keep last 100 chunks for real-time visualization
        waveform_data_buffer.append(data.tolist())
        if len(waveform_data_buffer) > 100:
            waveform_data_buffer.pop(0)
    
    recorder.set_waveform_callback(waveform_callback)
    
    # Initialize transcriber
    model_name = config.get("whisper.model", "base")
    language = config.get("whisper.language", "fr")
    
    transcriber = Transcriber(model_name=model_name, language=language)
    
    # Load Whisper model in background
    def load_model():
        try:
            logger.info(f"Loading Whisper model '{model_name}'...")
            transcriber.load_model()
            logger.info("Whisper model loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load Whisper model: {e}")
    
    threading.Thread(target=load_model, daemon=True).start()
    
    logger.info("VoiceSnap server initialized")

# API Routes

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "success": True,
        "data": {
            "status": "healthy",
            "model_loaded": transcriber.model is not None if transcriber else False,
            "recording": is_recording
        }
    })

@app.route('/api/recording/start', methods=['POST'])
def start_recording():
    """Start audio recording"""
    global is_recording, waveform_data_buffer
    
    try:
        if is_recording:
            return jsonify({
                "success": False,
                "error": "Already recording"
            }), 400
        
        waveform_data_buffer = []
        recorder.start_recording()
        is_recording = True
        
        logger.info("Recording started")
        
        return jsonify({
            "success": True,
            "data": True
        })
    
    except Exception as e:
        logger.error(f"Failed to start recording: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_recording():
    """Stop recording and transcribe"""
    global is_recording, current_audio
    
    try:
        if not is_recording:
            return jsonify({
                "success": False,
                "error": "Not recording"
            }), 400
        
        # Stop recording
        audio = recorder.stop_recording()
        is_recording = False
        
        if audio is None or len(audio) == 0:
            return jsonify({
                "success": False,
                "error": "No audio data captured"
            }), 400
        
        logger.info(f"Recording stopped, duration: {recorder.get_duration():.2f}s")
        
        # Check if model is loaded
        if transcriber.model is None:
            return jsonify({
                "success": False,
                "error": "Whisper model not loaded yet. Please wait..."
            }), 503
        
        # Transcribe
        logger.info("Transcribing audio...")
        save_audio = config.get("behavior.save_audio_files", False)
        audio_cache_dir = config.get_audio_cache_dir() if save_audio else None
        
        result = transcriber.transcribe_audio(
            audio,
            sample_rate=recorder.sample_rate,
            save_audio=save_audio,
            audio_cache_dir=audio_cache_dir
        )
        
        logger.info(f"Transcription complete: {result['text'][:50]}...")
        
        # Save to database
        transcription_id = db.add_transcription(
            text=result['text'],
            language=config.get("whisper.language"),
            detected_language=result['language'],
            model=config.get("whisper.model"),
            duration=result['duration'],
            audio_file=result['audio_file'],
            pasted=False
        )
        
        # Auto-paste if enabled
        auto_paste = config.get("behavior.auto_paste", True)
        if auto_paste:
            # This will be handled by Tauri frontend
            pass
        
        return jsonify({
            "success": True,
            "data": {
                "id": transcription_id,
                "text": result['text'],
                "language": result['language'],
                "duration": result['duration'],
                "audio_file": result['audio_file']
            }
        })
    
    except Exception as e:
        is_recording = False
        logger.error(f"Failed to stop recording/transcribe: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recording/waveform', methods=['GET'])
def get_waveform():
    """Get current waveform data for visualization"""
    global waveform_data_buffer
    
    return jsonify({
        "success": True,
        "data": {
            "waveform": waveform_data_buffer,
            "is_recording": is_recording,
            "duration": recorder.get_duration() if is_recording else 0
        }
    })

@app.route('/api/devices', methods=['GET'])
def get_audio_devices():
    """Get list of audio input devices"""
    try:
        devices = AudioRecorder.list_devices()
        return jsonify({
            "success": True,
            "data": devices
        })
    except Exception as e:
        logger.error(f"Failed to get audio devices: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/transcriptions', methods=['GET'])
def get_transcriptions():
    """Get transcription history"""
    try:
        limit = request.args.get('limit', 100, type=int)
        transcriptions = db.get_recent_transcriptions(limit=limit)
        
        return jsonify({
            "success": True,
            "data": transcriptions
        })
    except Exception as e:
        logger.error(f"Failed to get transcriptions: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/transcriptions/<int:transcription_id>', methods=['DELETE'])
def delete_transcription(transcription_id):
    """Delete a transcription"""
    try:
        deleted = db.delete_transcription(transcription_id)
        
        if deleted:
            return jsonify({
                "success": True,
                "data": True
            })
        else:
            return jsonify({
                "success": False,
                "error": "Transcription not found"
            }), 404
    
    except Exception as e:
        logger.error(f"Failed to delete transcription: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get current configuration"""
    try:
        return jsonify({
            "success": True,
            "data": config.config
        })
    except Exception as e:
        logger.error(f"Failed to get config: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration"""
    try:
        new_config = request.json
        
        # Update config
        for key_path, value in flatten_dict(new_config).items():
            config.set(key_path, value, save=False)
        
        config.save()
        
        # Reload components if needed
        # TODO: Implement hot reload for recorder/transcriber settings
        
        return jsonify({
            "success": True,
            "data": True
        })
    
    except Exception as e:
        logger.error(f"Failed to update config: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/paste', methods=['POST'])
def paste_text():
    """Simulate paste action (will be handled by Tauri frontend)"""
    try:
        data = request.json
        text = data.get('text', '')
        
        # In Tauri, we'll use clipboard API on the frontend
        # This endpoint is just for compatibility
        
        return jsonify({
            "success": True,
            "data": True
        })
    
    except Exception as e:
        logger.error(f"Failed to paste: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

def flatten_dict(d: Dict, parent_key: str = '', sep: str = '.') -> Dict:
    """Flatten nested dictionary to dot notation"""
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)

def main():
    """Start the server"""
    init_app()
    
    # Run Flask server
    port = int(os.environ.get('PORT', 8765))
    logger.info(f"Starting VoiceSnap server on http://localhost:{port}")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )

if __name__ == '__main__':
    main()
