"""Configuration manager for VoiceSnap"""

import json
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Manages application configuration with JSON storage"""
    
    DEFAULT_CONFIG = {
        "version": "2.0.0",
        "audio": {
            "sample_rate": 16000,
            "channels": 1,
            "device_index": None,  # None = default device
            "max_duration": 120    # seconds
        },
        "whisper": {
            "model": "base",       # tiny, base, small, medium, large
            "language": "fr",      # fr, en, None for auto-detect
            "task": "transcribe"   # transcribe or translate
        },
        "hotkey": {
            "modifiers": ["ctrl"],
            "key": "space",
            "toggle_mode": True    # True = toggle, False = push-to-talk
        },
        "behavior": {
            "auto_paste": True,    # Auto-paste after transcription
            "copy_to_clipboard": True,
            "minimize_to_tray": True,
            "start_minimized": False,
            "run_on_startup": False
        },
        "ui": {
            "theme": "dark",       # dark or light
            "overlay_position": "top",  # top, bottom
            "overlay_height": 80,
            "show_notifications": True
        }
    }
    
    def __init__(self, config_dir: str = None):
        """Initialize configuration manager
        
        Args:
            config_dir: Directory to store config file (default: ~/.voicesnap)
        """
        if config_dir is None:
            config_dir = os.path.join(str(Path.home()), ".voicesnap")
        
        self.config_dir = Path(config_dir)
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        self.config_file = self.config_dir / "config.json"
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default"""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    # Merge with defaults to handle new keys
                    return self._merge_configs(self.DEFAULT_CONFIG, config)
            except Exception as e:
                print(f"Error loading config: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self.save()
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Recursively merge user config with defaults"""
        result = default.copy()
        for key, value in user.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_configs(result[key], value)
            else:
                result[key] = value
        return result
    
    def save(self):
        """Save current configuration to file"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def get(self, key_path: str, default=None):
        """Get configuration value using dot notation
        
        Args:
            key_path: Path to config key (e.g., "audio.sample_rate")
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        keys = key_path.split('.')
        value = self.config
        
        for key in keys:
            if isinstance(value, dict) and key in value:
                value = value[key]
            else:
                return default
        
        return value
    
    def set(self, key_path: str, value: Any, save: bool = True):
        """Set configuration value using dot notation
        
        Args:
            key_path: Path to config key (e.g., "audio.sample_rate")
            value: Value to set
            save: Whether to save to file immediately
        """
        keys = key_path.split('.')
        config = self.config
        
        # Navigate to the parent dict
        for key in keys[:-1]:
            if key not in config:
                config[key] = {}
            config = config[key]
        
        # Set the value
        config[keys[-1]] = value
        
        if save:
            self.save()
    
    def reset(self):
        """Reset configuration to defaults"""
        self.config = self.DEFAULT_CONFIG.copy()
        self.save()
    
    def get_data_dir(self) -> Path:
        """Get data directory path"""
        data_dir = self.config_dir / "data"
        data_dir.mkdir(exist_ok=True)
        return data_dir
    
    def get_audio_cache_dir(self) -> Path:
        """Get audio cache directory path"""
        cache_dir = self.config_dir / "audio_cache"
        cache_dir.mkdir(exist_ok=True)
        return cache_dir
