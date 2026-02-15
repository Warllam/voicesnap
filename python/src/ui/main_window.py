"""Main application window with settings and history"""

import customtkinter as ctk
from typing import Optional, Callable, List, Dict
import pyperclip

class MainWindow:
    """Main application window"""
    
    def __init__(self, title: str = "VoiceSnap"):
        """Initialize main window
        
        Args:
            title: Window title
        """
        # Configure CustomTkinter theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry("900x700")
        
        # Callbacks
        self.on_settings_changed: Optional[Callable] = None
        self.on_close: Optional[Callable] = None
        
        # Settings variables
        self.microphone_var = ctk.StringVar()
        self.model_var = ctk.StringVar(value="base")
        self.language_var = ctk.StringVar(value="French")
        self.hotkey_var = ctk.StringVar(value="Ctrl+Space")
        self.auto_paste_var = ctk.BooleanVar(value=True)
        self.minimize_to_tray_var = ctk.BooleanVar(value=True)
        
        # History data
        self.history_items: List[Dict] = []
        self.search_var = ctk.StringVar()
        
        # UI elements
        self.history_frame: Optional[ctk.CTkScrollableFrame] = None
        self.status_label: Optional[ctk.CTkLabel] = None
        
        # Build UI
        self._create_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_ui(self):
        """Create the user interface"""
        # Create tabview
        tabview = ctk.CTkTabview(self.root)
        tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add tabs
        tabview.add("History")
        tabview.add("Settings")
        tabview.add("About")
        
        # Build each tab
        self._create_history_tab(tabview.tab("History"))
        self._create_settings_tab(tabview.tab("Settings"))
        self._create_about_tab(tabview.tab("About"))
        
        # Status bar at bottom
        status_frame = ctk.CTkFrame(self.root)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="Ready",
            anchor="w"
        )
        self.status_label.pack(fill="x", padx=10, pady=5)
    
    def _create_history_tab(self, parent):
        """Create history tab
        
        Args:
            parent: Parent widget
        """
        # Search bar
        search_frame = ctk.CTkFrame(parent)
        search_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(search_frame, text="Search:").pack(side="left", padx=(0, 10))
        
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search transcriptions..."
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        search_btn = ctk.CTkButton(
            search_frame,
            text="Search",
            width=100,
            command=self._on_search
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        clear_btn = ctk.CTkButton(
            search_frame,
            text="Clear",
            width=100,
            command=self._on_clear_search
        )
        clear_btn.pack(side="left")
        
        # History list
        self.history_frame = ctk.CTkScrollableFrame(parent)
        self.history_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Placeholder
        placeholder = ctk.CTkLabel(
            self.history_frame,
            text="No transcriptions yet.\n\nPress your hotkey to start recording!",
            text_color="gray"
        )
        placeholder.pack(pady=50)
    
    def _create_settings_tab(self, parent):
        """Create settings tab
        
        Args:
            parent: Parent widget
        """
        # Audio Settings
        audio_frame = ctk.CTkFrame(parent)
        audio_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            audio_frame,
            text="Audio Settings",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Microphone selection
        mic_frame = ctk.CTkFrame(audio_frame)
        mic_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(mic_frame, text="Microphone:").pack(side="left", padx=(0, 10))
        
        self.microphone_menu = ctk.CTkOptionMenu(
            mic_frame,
            variable=self.microphone_var,
            values=["Default"],
            command=self._on_setting_changed
        )
        self.microphone_menu.pack(side="left", fill="x", expand=True)
        
        # Whisper Settings
        whisper_frame = ctk.CTkFrame(parent)
        whisper_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            whisper_frame,
            text="Whisper Settings",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Model selection
        model_frame = ctk.CTkFrame(whisper_frame)
        model_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(model_frame, text="Model:").pack(side="left", padx=(0, 10))
        
        ctk.CTkOptionMenu(
            model_frame,
            variable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            command=self._on_setting_changed
        ).pack(side="left", fill="x", expand=True)
        
        # Model info
        model_info = ctk.CTkLabel(
            whisper_frame,
            text="• tiny: Fast, good for simple transcriptions\n"
                 "• base: Balanced speed/accuracy (recommended)\n"
                 "• small: Better accuracy, slower\n"
                 "• medium: High accuracy, much slower\n"
                 "• large: Best accuracy, very slow",
            justify="left",
            text_color="gray",
            font=("Arial", 10)
        )
        model_info.pack(anchor="w", padx=10, pady=5)
        
        # Language selection
        lang_frame = ctk.CTkFrame(whisper_frame)
        lang_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(lang_frame, text="Language:").pack(side="left", padx=(0, 10))
        
        ctk.CTkOptionMenu(
            lang_frame,
            variable=self.language_var,
            values=["Auto-detect", "English", "French", "Spanish", "German", "Italian"],
            command=self._on_setting_changed
        ).pack(side="left", fill="x", expand=True)
        
        # Hotkey Settings
        hotkey_frame = ctk.CTkFrame(parent)
        hotkey_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            hotkey_frame,
            text="Hotkey Settings",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Hotkey display
        hk_frame = ctk.CTkFrame(hotkey_frame)
        hk_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(hk_frame, text="Current Hotkey:").pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            hk_frame,
            textvariable=self.hotkey_var,
            font=("Arial", 12, "bold")
        ).pack(side="left")
        
        ctk.CTkButton(
            hk_frame,
            text="Change Hotkey",
            command=self._on_change_hotkey
        ).pack(side="right")
        
        # Behavior Settings
        behavior_frame = ctk.CTkFrame(parent)
        behavior_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            behavior_frame,
            text="Behavior",
            font=("Arial", 16, "bold")
        ).pack(anchor="w", padx=10, pady=(10, 5))
        
        # Auto-paste checkbox
        ctk.CTkCheckBox(
            behavior_frame,
            text="Auto-paste transcription into active window",
            variable=self.auto_paste_var,
            command=self._on_setting_changed
        ).pack(anchor="w", padx=10, pady=5)
        
        # Minimize to tray checkbox
        ctk.CTkCheckBox(
            behavior_frame,
            text="Minimize to system tray",
            variable=self.minimize_to_tray_var,
            command=self._on_setting_changed
        ).pack(anchor="w", padx=10, pady=5)
    
    def _create_about_tab(self, parent):
        """Create about tab
        
        Args:
            parent: Parent widget
        """
        about_frame = ctk.CTkFrame(parent)
        about_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Logo/Title
        ctk.CTkLabel(
            about_frame,
            text="🎤 VoiceSnap",
            font=("Arial", 32, "bold")
        ).pack(pady=(20, 10))
        
        ctk.CTkLabel(
            about_frame,
            text="Version 2.0.0",
            font=("Arial", 14),
            text_color="gray"
        ).pack()
        
        # Description
        ctk.CTkLabel(
            about_frame,
            text="Local voice-to-text transcription with OpenAI Whisper\n"
                 "100% private, no cloud, no API keys required",
            font=("Arial", 12),
            justify="center"
        ).pack(pady=20)
        
        # Features
        features = ctk.CTkFrame(about_frame)
        features.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            features,
            text="Features:",
            font=("Arial", 14, "bold")
        ).pack(anchor="w", pady=(10, 5))
        
        feature_list = [
            "• Global hotkey for quick transcription",
            "• Real-time audio waveform visualization",
            "• Automatic transcription with Whisper AI",
            "• Auto-paste or clipboard copy",
            "• Searchable transcription history",
            "• System tray integration",
            "• 100% local processing"
        ]
        
        for feature in feature_list:
            ctk.CTkLabel(
                features,
                text=feature,
                justify="left",
                anchor="w"
            ).pack(anchor="w", padx=20, pady=2)
        
        # Footer
        ctk.CTkLabel(
            about_frame,
            text="Made with ❤️ by Warllam",
            font=("Arial", 10),
            text_color="gray"
        ).pack(side="bottom", pady=20)
        
        # GitHub link
        github_btn = ctk.CTkButton(
            about_frame,
            text="View on GitHub",
            command=lambda: self._open_url("https://github.com/Warllam/voicesnap")
        )
        github_btn.pack(side="bottom", pady=10)
    
    def _on_setting_changed(self, *args):
        """Handle settings change"""
        if self.on_settings_changed:
            self.on_settings_changed()
    
    def _on_change_hotkey(self):
        """Handle change hotkey button"""
        # TODO: Implement hotkey capture dialog
        self.set_status("Hotkey change not yet implemented")
    
    def _on_search(self):
        """Handle search button"""
        # TODO: Implement search
        self.set_status(f"Searching for: {self.search_var.get()}")
    
    def _on_clear_search(self):
        """Handle clear search button"""
        self.search_var.set("")
        self._on_search()
    
    def _on_close(self):
        """Handle window close"""
        if self.on_close:
            self.on_close()
        else:
            self.root.quit()
    
    def _open_url(self, url: str):
        """Open URL in browser"""
        import webbrowser
        webbrowser.open(url)
    
    def set_microphones(self, devices: List[Dict]):
        """Set available microphones
        
        Args:
            devices: List of device dictionaries
        """
        if not devices:
            values = ["Default (No devices found)"]
        else:
            values = [f"{d['name']} (#{d['index']})" for d in devices]
        
        self.microphone_menu.configure(values=values)
        if values:
            self.microphone_var.set(values[0])
    
    def update_history(self, transcriptions: List[Dict]):
        """Update history display
        
        Args:
            transcriptions: List of transcription dictionaries
        """
        # Clear existing items
        for widget in self.history_frame.winfo_children():
            widget.destroy()
        
        if not transcriptions:
            placeholder = ctk.CTkLabel(
                self.history_frame,
                text="No transcriptions found.",
                text_color="gray"
            )
            placeholder.pack(pady=50)
            return
        
        # Create history items
        for trans in transcriptions:
            self._create_history_item(trans)
    
    def _create_history_item(self, transcription: Dict):
        """Create a history item widget
        
        Args:
            transcription: Transcription dictionary
        """
        item_frame = ctk.CTkFrame(self.history_frame)
        item_frame.pack(fill="x", padx=5, pady=5)
        
        # Header with timestamp
        header_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        timestamp = transcription.get("timestamp", "")
        duration = transcription.get("duration", 0)
        language = transcription.get("detected_language", "")
        
        header_text = f"📅 {timestamp}"
        if duration:
            header_text += f"  •  ⏱️ {duration:.1f}s"
        if language:
            header_text += f"  •  🌍 {language}"
        
        ctk.CTkLabel(
            header_frame,
            text=header_text,
            font=("Arial", 10),
            text_color="gray"
        ).pack(side="left")
        
        # Text content
        text_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        text_frame.pack(fill="x", padx=10, pady=5)
        
        text = transcription.get("text", "")
        ctk.CTkLabel(
            text_frame,
            text=text,
            wraplength=800,
            justify="left",
            anchor="w"
        ).pack(fill="x")
        
        # Actions
        action_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        ctk.CTkButton(
            action_frame,
            text="Copy",
            width=80,
            command=lambda t=text: self._copy_text(t)
        ).pack(side="left", padx=(0, 5))
        
        ctk.CTkButton(
            action_frame,
            text="Paste",
            width=80,
            command=lambda t=text: self._paste_text(t)
        ).pack(side="left", padx=(0, 5))
        
        delete_btn = ctk.CTkButton(
            action_frame,
            text="Delete",
            width=80,
            fg_color="darkred",
            hover_color="red",
            command=lambda tid=transcription.get("id"): self._delete_transcription(tid)
        )
        delete_btn.pack(side="right")
    
    def _copy_text(self, text: str):
        """Copy text to clipboard"""
        pyperclip.copy(text)
        self.set_status("Copied to clipboard")
    
    def _paste_text(self, text: str):
        """Paste text to active window"""
        from pynput.keyboard import Controller, Key
        
        pyperclip.copy(text)
        
        keyboard = Controller()
        
        import sys
        if sys.platform == "darwin":
            keyboard.press(Key.cmd)
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release(Key.cmd)
        else:
            keyboard.press(Key.ctrl)
            keyboard.press('v')
            keyboard.release('v')
            keyboard.release(Key.ctrl)
        
        self.set_status("Text pasted")
    
    def _delete_transcription(self, transcription_id: int):
        """Delete transcription"""
        # TODO: Implement delete with callback
        self.set_status(f"Delete transcription #{transcription_id}")
    
    def set_status(self, message: str):
        """Set status bar message
        
        Args:
            message: Status message
        """
        if self.status_label:
            self.status_label.configure(text=message)
    
    def get_settings(self) -> Dict:
        """Get current settings
        
        Returns:
            Dictionary with settings
        """
        return {
            "microphone": self.microphone_var.get(),
            "model": self.model_var.get(),
            "language": self.language_var.get(),
            "hotkey": self.hotkey_var.get(),
            "auto_paste": self.auto_paste_var.get(),
            "minimize_to_tray": self.minimize_to_tray_var.get()
        }
    
    def set_settings(self, settings: Dict):
        """Set settings values
        
        Args:
            settings: Settings dictionary
        """
        if "model" in settings:
            self.model_var.set(settings["model"])
        if "language" in settings:
            self.language_var.set(settings["language"])
        if "hotkey" in settings:
            self.hotkey_var.set(settings["hotkey"])
        if "auto_paste" in settings:
            self.auto_paste_var.set(settings["auto_paste"])
        if "minimize_to_tray" in settings:
            self.minimize_to_tray_var.set(settings["minimize_to_tray"])
    
    def run(self):
        """Run the main loop"""
        self.root.mainloop()
    
    def hide(self):
        """Hide the window"""
        self.root.withdraw()
    
    def show(self):
        """Show the window"""
        self.root.deiconify()
        self.root.lift()
