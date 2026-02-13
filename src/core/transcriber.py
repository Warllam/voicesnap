"""Whisper transcription manager"""

import os
import tempfile
import threading
from pathlib import Path
from typing import Optional, Dict, Callable
import numpy as np
import soundfile as sf
import whisper

class Transcriber:
    """Manages Whisper model and transcription"""
    
    def __init__(
        self,
        model_name: str = "base",
        language: Optional[str] = "fr",
        device: Optional[str] = None
    ):
        """Initialize transcriber
        
        Args:
            model_name: Whisper model name (tiny, base, small, medium, large)
            language: Language code (fr, en, etc.) or None for auto-detect
            device: Device to use (cuda, cpu) or None for auto-detect
        """
        self.model_name = model_name
        self.language = language
        self.device = device
        
        self.model: Optional[whisper.Whisper] = None
        self.is_loading = False
        self.is_transcribing = False
        
        self._lock = threading.Lock()
    
    def load_model(self, progress_callback: Optional[Callable[[str], None]] = None):
        """Load Whisper model
        
        Args:
            progress_callback: Optional callback for progress updates
        """
        if self.model is not None:
            return
        
        with self._lock:
            if self.is_loading:
                return
            self.is_loading = True
        
        try:
            if progress_callback:
                progress_callback(f"Loading Whisper model '{self.model_name}'...")
            
            self.model = whisper.load_model(self.model_name, device=self.device)
            
            if progress_callback:
                progress_callback(f"Model '{self.model_name}' loaded successfully")
                
        except Exception as e:
            if progress_callback:
                progress_callback(f"Error loading model: {e}")
            raise
        finally:
            self.is_loading = False
    
    def transcribe_audio(
        self,
        audio: np.ndarray,
        sample_rate: int = 16000,
        save_audio: bool = False,
        audio_cache_dir: Optional[Path] = None
    ) -> Dict:
        """Transcribe audio data
        
        Args:
            audio: Audio data as numpy array
            sample_rate: Sample rate of the audio
            save_audio: Whether to save audio file
            audio_cache_dir: Directory to save audio files
            
        Returns:
            Dictionary with transcription results:
                - text: Transcribed text
                - language: Detected language
                - segments: List of segments with timestamps
                - duration: Audio duration
                - audio_file: Path to saved audio file (if saved)
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        
        with self._lock:
            if self.is_transcribing:
                raise RuntimeError("Already transcribing")
            self.is_transcribing = True
        
        audio_file = None
        
        try:
            # Create temporary audio file
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                sf.write(tmp_file.name, audio, sample_rate)
                tmp_path = tmp_file.name
            
            # Transcribe with Whisper
            transcribe_options = {
                "language": self.language,
                "task": "transcribe",
                "fp16": False  # Use fp32 for CPU compatibility
            }
            
            result = self.model.transcribe(tmp_path, **transcribe_options)
            
            # Get audio duration
            duration = len(audio) / sample_rate
            
            # Save audio file if requested
            if save_audio and audio_cache_dir:
                from datetime import datetime
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                audio_file = audio_cache_dir / f"recording_{timestamp}.wav"
                sf.write(str(audio_file), audio, sample_rate)
            
            # Clean up temporary file
            try:
                os.unlink(tmp_path)
            except Exception:
                pass
            
            return {
                "text": result["text"].strip(),
                "language": result.get("language"),
                "segments": result.get("segments", []),
                "duration": duration,
                "audio_file": str(audio_file) if audio_file else None
            }
            
        except Exception as e:
            raise RuntimeError(f"Transcription failed: {e}")
        
        finally:
            self.is_transcribing = False
    
    def change_model(self, model_name: str, progress_callback: Optional[Callable[[str], None]] = None):
        """Change Whisper model
        
        Args:
            model_name: New model name
            progress_callback: Optional callback for progress updates
        """
        if self.is_transcribing:
            raise RuntimeError("Cannot change model while transcribing")
        
        self.model_name = model_name
        self.model = None
        self.load_model(progress_callback)
    
    def set_language(self, language: Optional[str]):
        """Set transcription language
        
        Args:
            language: Language code or None for auto-detect
        """
        self.language = language
    
    @staticmethod
    def get_available_models() -> list:
        """Get list of available Whisper models"""
        return ["tiny", "base", "small", "medium", "large"]
    
    @staticmethod
    def get_model_info(model_name: str) -> Dict:
        """Get information about a Whisper model
        
        Args:
            model_name: Model name
            
        Returns:
            Dictionary with model info
        """
        model_info = {
            "tiny": {
                "size": "~75 MB",
                "speed": "Very fast",
                "accuracy": "Good for simple transcriptions"
            },
            "base": {
                "size": "~150 MB",
                "speed": "Fast",
                "accuracy": "Good balance speed/accuracy"
            },
            "small": {
                "size": "~500 MB",
                "speed": "Moderate",
                "accuracy": "Better accuracy"
            },
            "medium": {
                "size": "~1.5 GB",
                "speed": "Slower",
                "accuracy": "High accuracy"
            },
            "large": {
                "size": "~3 GB",
                "speed": "Slow",
                "accuracy": "Best accuracy"
            }
        }
        
        return model_info.get(model_name, {"size": "Unknown", "speed": "Unknown", "accuracy": "Unknown"})
    
    @staticmethod
    def get_supported_languages() -> list:
        """Get list of supported languages"""
        # Common languages - Whisper supports 99+ languages
        return [
            ("Auto-detect", None),
            ("English", "en"),
            ("French", "fr"),
            ("Spanish", "es"),
            ("German", "de"),
            ("Italian", "it"),
            ("Portuguese", "pt"),
            ("Dutch", "nl"),
            ("Russian", "ru"),
            ("Chinese", "zh"),
            ("Japanese", "ja"),
            ("Korean", "ko"),
            ("Arabic", "ar"),
            ("Turkish", "tr"),
            ("Polish", "pl"),
            ("Ukrainian", "uk"),
            ("Swedish", "sv"),
            ("Danish", "da"),
            ("Norwegian", "no"),
            ("Finnish", "fi")
        ]
