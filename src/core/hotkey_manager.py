"""Global hotkey manager"""

import threading
from typing import Callable, List, Optional, Set
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

class HotkeyManager:
    """Manages global hotkeys"""
    
    MODIFIER_MAP = {
        "ctrl": Key.ctrl,
        "alt": Key.alt,
        "shift": Key.shift,
        "cmd": Key.cmd,  # macOS
        "super": Key.cmd  # Linux
    }
    
    def __init__(self):
        """Initialize hotkey manager"""
        self.listener: Optional[keyboard.Listener] = None
        self.current_keys: Set = set()
        self.hotkey_combo: Set = set()
        self.toggle_mode = True
        self.is_active = False
        
        self.on_activate: Optional[Callable] = None
        self.on_deactivate: Optional[Callable] = None
        
        self._lock = threading.Lock()
    
    def set_hotkey(self, modifiers: List[str], key: str, toggle_mode: bool = True):
        """Set hotkey combination
        
        Args:
            modifiers: List of modifier keys (ctrl, alt, shift, cmd)
            key: Main key (e.g., 'space', 'a', 'f1')
            toggle_mode: True for toggle, False for push-to-talk
        """
        self.toggle_mode = toggle_mode
        self.hotkey_combo = set()
        
        # Add modifiers
        for mod in modifiers:
            mod_lower = mod.lower()
            if mod_lower in self.MODIFIER_MAP:
                self.hotkey_combo.add(self.MODIFIER_MAP[mod_lower])
        
        # Add main key
        key_lower = key.lower()
        
        # Check if it's a special key
        special_keys = {
            "space": Key.space,
            "enter": Key.enter,
            "tab": Key.tab,
            "backspace": Key.backspace,
            "delete": Key.delete,
            "esc": Key.esc,
            "up": Key.up,
            "down": Key.down,
            "left": Key.left,
            "right": Key.right,
            "home": Key.home,
            "end": Key.end,
            "page_up": Key.page_up,
            "page_down": Key.page_down,
        }
        
        # Add function keys
        for i in range(1, 13):
            special_keys[f"f{i}"] = getattr(Key, f"f{i}")
        
        if key_lower in special_keys:
            self.hotkey_combo.add(special_keys[key_lower])
        else:
            # Regular character key
            self.hotkey_combo.add(KeyCode.from_char(key_lower))
    
    def set_callbacks(
        self,
        on_activate: Optional[Callable] = None,
        on_deactivate: Optional[Callable] = None
    ):
        """Set callback functions for hotkey events
        
        Args:
            on_activate: Called when hotkey is activated
            on_deactivate: Called when hotkey is deactivated
        """
        self.on_activate = on_activate
        self.on_deactivate = on_deactivate
    
    def start(self):
        """Start listening for hotkeys"""
        if self.listener is not None:
            return
        
        def on_press(key):
            """Handle key press"""
            self.current_keys.add(key)
            
            # Check if hotkey combo is pressed
            if self._is_hotkey_pressed():
                with self._lock:
                    if self.toggle_mode:
                        # Toggle mode: switch state
                        if not self.is_active:
                            self.is_active = True
                            if self.on_activate:
                                threading.Thread(target=self.on_activate, daemon=True).start()
                    else:
                        # Push-to-talk mode: activate when pressed
                        if not self.is_active:
                            self.is_active = True
                            if self.on_activate:
                                threading.Thread(target=self.on_activate, daemon=True).start()
        
        def on_release(key):
            """Handle key release"""
            if key in self.current_keys:
                self.current_keys.discard(key)
            
            # In push-to-talk mode, deactivate when keys are released
            if not self.toggle_mode and self.is_active:
                if not self._is_hotkey_pressed():
                    with self._lock:
                        self.is_active = False
                        if self.on_deactivate:
                            threading.Thread(target=self.on_deactivate, daemon=True).start()
            
            # In toggle mode, second press deactivates
            elif self.toggle_mode and self.is_active:
                if self._is_hotkey_pressed():
                    with self._lock:
                        self.is_active = False
                        if self.on_deactivate:
                            threading.Thread(target=self.on_deactivate, daemon=True).start()
        
        self.listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        self.listener.start()
    
    def stop(self):
        """Stop listening for hotkeys"""
        if self.listener is not None:
            self.listener.stop()
            self.listener = None
        
        self.current_keys.clear()
        self.is_active = False
    
    def _is_hotkey_pressed(self) -> bool:
        """Check if the hotkey combination is currently pressed"""
        # Normalize keys for comparison
        current_normalized = self._normalize_keys(self.current_keys)
        hotkey_normalized = self._normalize_keys(self.hotkey_combo)
        
        return hotkey_normalized.issubset(current_normalized)
    
    def _normalize_keys(self, keys: Set) -> Set:
        """Normalize keys for comparison (handle left/right modifiers)"""
        normalized = set()
        
        for key in keys:
            # Handle left/right variants of modifiers
            if hasattr(key, 'name'):
                # It's a Key object
                name = key.name
                if name in ['ctrl_l', 'ctrl_r']:
                    normalized.add(Key.ctrl)
                elif name in ['alt_l', 'alt_r']:
                    normalized.add(Key.alt)
                elif name in ['shift_l', 'shift_r']:
                    normalized.add(Key.shift)
                elif name in ['cmd_l', 'cmd_r']:
                    normalized.add(Key.cmd)
                else:
                    normalized.add(key)
            else:
                # It's a KeyCode
                normalized.add(key)
        
        return normalized
    
    def get_hotkey_string(self) -> str:
        """Get human-readable hotkey string
        
        Returns:
            String like "Ctrl+Space" or "Cmd+Shift+A"
        """
        if not self.hotkey_combo:
            return "Not set"
        
        parts = []
        
        # Add modifiers first
        if Key.ctrl in self.hotkey_combo:
            parts.append("Ctrl")
        if Key.alt in self.hotkey_combo:
            parts.append("Alt")
        if Key.shift in self.hotkey_combo:
            parts.append("Shift")
        if Key.cmd in self.hotkey_combo:
            parts.append("Cmd")
        
        # Add main key
        for key in self.hotkey_combo:
            if key not in [Key.ctrl, Key.alt, Key.shift, Key.cmd]:
                if hasattr(key, 'name'):
                    parts.append(key.name.title())
                elif hasattr(key, 'char'):
                    parts.append(key.char.upper())
                else:
                    parts.append(str(key))
        
        return "+".join(parts)
    
    @staticmethod
    def get_available_modifiers() -> List[str]:
        """Get list of available modifier keys"""
        import sys
        
        modifiers = ["ctrl", "alt", "shift"]
        
        if sys.platform == "darwin":
            modifiers.append("cmd")
        else:
            modifiers.append("super")
        
        return modifiers
    
    @staticmethod
    def get_available_keys() -> List[str]:
        """Get list of common keys for hotkey binding"""
        keys = ["space", "enter", "tab"]
        
        # Function keys
        keys.extend([f"f{i}" for i in range(1, 13)])
        
        # Letters
        keys.extend([chr(i) for i in range(ord('a'), ord('z') + 1)])
        
        # Numbers
        keys.extend([str(i) for i in range(10)])
        
        return keys
