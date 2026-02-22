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
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s'
)
logger = logging.getLogger(__name__)

# Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for Tauri

# Request logging middleware
@app.before_request
def log_request():
    logger.debug(f"📨 {request.method} {request.path} from {request.remote_addr}")

@app.after_request
def log_response(response):
    logger.debug(f"📤 {request.method} {request.path} -> {response.status_code}")
    return response

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
    
    logger.info("=" * 60)
    logger.info("🎙️  VoiceSnap Backend Server - Initializing")
    logger.info("=" * 60)
    
    # Load config
    logger.info("📋 Loading configuration...")
    config = Config()
    logger.debug(f"📁 Config directory: {config.config_dir}")
    
    # Initialize database
    db_path = config.get_data_dir() / "transcriptions.db"
    logger.info(f"💾 Initializing database: {db_path}")
    db = TranscriptionDB(str(db_path))
    
    # Initialize recorder
    sample_rate = config.get("audio.sample_rate", 16000)
    channels = config.get("audio.channels", 1)
    device_index = config.get("audio.device_index")
    max_duration = config.get("audio.max_duration", 120)
    
    logger.info(f"🎙️  Initializing audio recorder...")
    logger.debug(f"   Sample rate: {sample_rate} Hz")
    logger.debug(f"   Channels: {channels}")
    logger.debug(f"   Device index: {device_index}")
    logger.debug(f"   Max duration: {max_duration}s")
    
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
    logger.debug("✅ Waveform callback registered")
    
    # Initialize transcriber
    model_name = config.get("whisper.model", "base")
    language = config.get("whisper.language", "fr")
    
    logger.info(f"🤖 Initializing Whisper transcriber...")
    logger.debug(f"   Model: {model_name}")
    logger.debug(f"   Language: {language}")
    
    transcriber = Transcriber(model_name=model_name, language=language)
    
    # Load Whisper model in background
    def load_model():
        try:
            logger.info(f"⏬ Loading Whisper model '{model_name}' (this may take a while)...")
            transcriber.load_model()
            logger.info("✅ Whisper model loaded successfully!")
        except Exception as e:
            logger.error(f"❌ Failed to load Whisper model: {e}", exc_info=True)
    
    threading.Thread(target=load_model, daemon=True).start()
    
    logger.info("=" * 60)
    logger.info("✅ VoiceSnap server initialized successfully!")
    logger.info("=" * 60)

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
    
    logger.info("📥 START RECORDING request received")
    
    try:
        if is_recording:
            logger.warning("⚠️ Already recording!")
            return jsonify({
                "success": False,
                "error": "Already recording"
            }), 400
        
        logger.debug("🔄 Clearing waveform buffer...")
        waveform_data_buffer = []
        
        logger.debug("🎙️ Starting recorder...")
        recorder.start_recording()
        is_recording = True
        
        logger.info("✅ Recording started successfully")
        
        return jsonify({
            "success": True,
            "data": True
        })
    
    except Exception as e:
        logger.error(f"❌ Failed to start recording: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recording/stop', methods=['POST'])
def stop_recording():
    """Stop recording and transcribe"""
    global is_recording, current_audio
    
    logger.info("📥 STOP RECORDING request received")
    
    try:
        if not is_recording:
            logger.warning("⚠️ Not recording!")
            return jsonify({
                "success": False,
                "error": "Not recording"
            }), 400
        
        # Stop recording
        logger.debug("🛑 Stopping recorder...")
        audio = recorder.stop_recording()
        is_recording = False
        
        if audio is None or len(audio) == 0:
            logger.error("❌ No audio data captured!")
            return jsonify({
                "success": False,
                "error": "No audio data captured"
            }), 400
        
        duration = recorder.get_duration()
        audio_length = len(audio)
        logger.info(f"✅ Recording stopped - Duration: {duration:.2f}s, Samples: {audio_length}")
        
        # Check if model is loaded
        if transcriber.model is None:
            logger.warning("⚠️ Whisper model not loaded yet!")
            return jsonify({
                "success": False,
                "error": "Whisper model not loaded yet. Please wait..."
            }), 503
        
        # Transcribe
        logger.info("🔄 Starting transcription...")
        save_audio = config.get("behavior.save_audio_files", False)
        audio_cache_dir = config.get_audio_cache_dir() if save_audio else None
        
        logger.debug(f"📝 Transcription params - save_audio: {save_audio}, cache_dir: {audio_cache_dir}")
        
        result = transcriber.transcribe_audio(
            audio,
            sample_rate=recorder.sample_rate,
            save_audio=save_audio,
            audio_cache_dir=audio_cache_dir
        )
        
        logger.info(f"✅ Transcription complete!")
        logger.info(f"📝 Text (preview): {result['text'][:100]}...")
        logger.info(f"🌍 Language: {result['language']}")
        
        # Save to database
        logger.debug("💾 Saving to database...")
        transcription_id = db.add_transcription(
            text=result['text'],
            language=config.get("whisper.language"),
            detected_language=result['language'],
            model=config.get("whisper.model"),
            duration=result['duration'],
            audio_file=result['audio_file'],
            pasted=False
        )
        
        logger.info(f"✅ Saved to DB with ID: {transcription_id}")
        
        # Auto-paste if enabled
        auto_paste = config.get("behavior.auto_paste", True)
        if auto_paste:
            logger.debug("📋 Auto-paste enabled (handled by frontend)")
        
        response_data = {
            "id": transcription_id,
            "text": result['text'],
            "language": result['language'],
            "duration": result['duration'],
            "audio_file": result['audio_file']
        }
        
        logger.info(f"📤 Sending response with transcription ID {transcription_id}")
        
        return jsonify({
            "success": True,
            "data": response_data
        })
    
    except Exception as e:
        is_recording = False
        logger.error(f"❌ Failed to stop recording/transcribe: {e}", exc_info=True)
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@app.route('/api/recording/waveform', methods=['GET'])
def get_waveform():
    """Get current waveform data for visualization"""
    global waveform_data_buffer
    
    duration = recorder.get_duration() if is_recording else 0
    buffer_size = len(waveform_data_buffer)
    
    # Log only every 10th request to avoid spam
    if buffer_size % 10 == 0:
        logger.debug(f"📊 Waveform request - Recording: {is_recording}, Duration: {duration:.2f}s, Buffer: {buffer_size} chunks")
    
    return jsonify({
        "success": True,
        "data": {
            "waveform": waveform_data_buffer,
            "is_recording": is_recording,
            "duration": duration
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
    print("\n" + "=" * 60)
    print("🎙️  VoiceSnap Backend Server")
    print("=" * 60 + "\n")
    
    init_app()
    
    # Run Flask server
    port = int(os.environ.get('PORT', 8765))
    
    print("\n" + "=" * 60)
    print(f"🚀 Server starting on http://localhost:{port}")
    print("=" * 60)
    print(f"\n📌 Health check: http://localhost:{port}/health")
    print(f"📌 API base URL: http://localhost:{port}/api")
    print("\n🔍 Logging level: DEBUG (verbose)")
    print("\n⏸️  Press Ctrl+C to stop\n")
    print("=" * 60 + "\n")
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )

if __name__ == '__main__':
    main()
