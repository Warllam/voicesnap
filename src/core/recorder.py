"""Audio recorder with real-time waveform data"""

import threading
import time
import numpy as np
import sounddevice as sd
import soundfile as sf
from pathlib import Path
from typing import Optional, Callable, List
from collections import deque

class AudioRecorder:
    """Records audio with real-time waveform data for visualization"""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        device_index: Optional[int] = None,
        max_duration: int = 120
    ):
        """Initialize audio recorder
        
        Args:
            sample_rate: Sample rate in Hz
            channels: Number of audio channels
            device_index: Audio device index (None = default)
            max_duration: Maximum recording duration in seconds
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.device_index = device_index
        self.max_duration = max_duration
        
        self.is_recording = False
        self.audio_data: List[np.ndarray] = []
        self.stream: Optional[sd.InputStream] = None
        self.start_time: Optional[float] = None
        
        # For real-time waveform visualization
        self.waveform_buffer = deque(maxlen=100)  # Keep last 100 chunks
        self.waveform_callback: Optional[Callable] = None
        
        self._lock = threading.Lock()
    
    def set_waveform_callback(self, callback: Callable[[np.ndarray], None]):
        """Set callback for real-time waveform data
        
        Args:
            callback: Function that receives waveform data (numpy array)
        """
        self.waveform_callback = callback
    
    def start_recording(self):
        """Start audio recording"""
        if self.is_recording:
            return
        
        with self._lock:
            self.is_recording = True
            self.audio_data = []
            self.waveform_buffer.clear()
            self.start_time = time.time()
        
        def audio_callback(indata, frames, time_info, status):
            """Callback for audio stream"""
            if status:
                print(f"Audio status: {status}")
            
            if self.is_recording:
                # Store audio data
                self.audio_data.append(indata.copy())
                
                # Update waveform buffer for visualization
                self.waveform_buffer.append(indata.copy())
                
                # Call waveform callback if set
                if self.waveform_callback:
                    try:
                        self.waveform_callback(indata.copy())
                    except Exception as e:
                        print(f"Waveform callback error: {e}")
        
        try:
            self.stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                device=self.device_index,
                callback=audio_callback
            )
            self.stream.start()
            
            # Auto-stop after max duration
            def auto_stop():
                time.sleep(self.max_duration)
                if self.is_recording:
                    print(f"Max duration reached ({self.max_duration}s), stopping recording")
                    self.stop_recording()
            
            threading.Thread(target=auto_stop, daemon=True).start()
            
        except Exception as e:
            self.is_recording = False
            raise RuntimeError(f"Failed to start recording: {e}")
    
    def stop_recording(self) -> Optional[np.ndarray]:
        """Stop recording and return audio data
        
        Returns:
            Recorded audio as numpy array, or None if no data
        """
        if not self.is_recording:
            return None
        
        with self._lock:
            self.is_recording = False
        
        # Stop and close stream
        if self.stream:
            self.stream.stop()
            self.stream.close()
            self.stream = None
        
        # Concatenate all audio chunks
        if not self.audio_data:
            return None
        
        audio = np.concatenate(self.audio_data, axis=0)
        
        return audio
    
    def get_duration(self) -> float:
        """Get current recording duration in seconds"""
        if not self.start_time:
            return 0.0
        return time.time() - self.start_time
    
    def get_waveform_data(self) -> Optional[np.ndarray]:
        """Get current waveform data for visualization
        
        Returns:
            Recent waveform data as numpy array
        """
        if not self.waveform_buffer:
            return None
        
        try:
            return np.concatenate(list(self.waveform_buffer), axis=0)
        except Exception:
            return None
    
    def save_audio(self, audio: np.ndarray, filepath: Path):
        """Save audio to file
        
        Args:
            audio: Audio data as numpy array
            filepath: Path to save file
        """
        sf.write(str(filepath), audio, self.sample_rate)
    
    @staticmethod
    def list_devices() -> List[dict]:
        """List available audio input devices
        
        Returns:
            List of device dictionaries with 'index', 'name', 'channels'
        """
        devices = []
        
        for i, device in enumerate(sd.query_devices()):
            if device['max_input_channels'] > 0:
                devices.append({
                    'index': i,
                    'name': device['name'],
                    'channels': device['max_input_channels'],
                    'sample_rate': device['default_samplerate']
                })
        
        return devices
    
    @staticmethod
    def get_default_device() -> Optional[int]:
        """Get default input device index"""
        try:
            return sd.default.device[0]  # Input device
        except Exception:
            return None
