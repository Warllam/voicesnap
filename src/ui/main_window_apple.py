"""Apple-inspired minimalist main window"""

import customtkinter as ctk
from typing import Optional, Callable, List, Dict
import pyperclip
from PIL import Image, ImageFilter, ImageDraw, ImageTk
import math

# Apple Design System Colors
COLORS_LIGHT = {
    "bg_primary": "#FFFFFF",
    "bg_secondary": "#F5F5F7",
    "bg_tertiary": "#E8E8ED",
    "text_primary": "#1D1D1F",
    "text_secondary": "#86868B",
    "accent": "#007AFF",
    "accent_hover": "#0051D5",
    "success": "#34C759",
    "danger": "#FF3B30",
    "border": "#D2D2D7",
    "card_shadow": "#00000008"
}

COLORS_DARK = {
    "bg_primary": "#1C1C1E",
    "bg_secondary": "#2C2C2E",
    "bg_tertiary": "#3A3A3C",
    "text_primary": "#FFFFFF",
    "text_secondary": "#98989D",
    "accent": "#0A84FF",
    "accent_hover": "#409CFF",
    "success": "#30D158",
    "danger": "#FF453A",
    "border": "#38383A",
    "card_shadow": "#00000020"
}


class AppleButton(ctk.CTkButton):
    """Custom Apple-style button with subtle animations"""
    
    def __init__(self, master, **kwargs):
        # Extract custom params
        style = kwargs.pop('style', 'primary')
        
        # Set Apple-style defaults
        defaults = {
            "corner_radius": 10,
            "border_width": 0,
            "font": ("SF Pro Display", 13),
            "height": 36,
            "cursor": "hand2"
        }
        
        if style == 'primary':
            defaults.update({
                "fg_color": COLORS_LIGHT["accent"],
                "hover_color": COLORS_LIGHT["accent_hover"],
                "text_color": "#FFFFFF"
            })
        elif style == 'secondary':
            defaults.update({
                "fg_color": COLORS_LIGHT["bg_tertiary"],
                "hover_color": COLORS_LIGHT["border"],
                "text_color": COLORS_LIGHT["text_primary"]
            })
        elif style == 'danger':
            defaults.update({
                "fg_color": COLORS_LIGHT["danger"],
                "hover_color": "#CC0000",
                "text_color": "#FFFFFF"
            })
        elif style == 'minimal':
            defaults.update({
                "fg_color": "transparent",
                "hover_color": COLORS_LIGHT["bg_tertiary"],
                "text_color": COLORS_LIGHT["accent"]
            })
        
        # Merge with user params
        defaults.update(kwargs)
        super().__init__(master, **defaults)


class TranscriptionCard(ctk.CTkFrame):
    """Individual transcription card with Apple styling"""
    
    def __init__(self, master, transcription: Dict, on_copy: Callable, on_paste: Callable, 
                 on_delete: Callable, theme: str = "light", **kwargs):
        colors = COLORS_LIGHT if theme == "light" else COLORS_DARK
        
        super().__init__(
            master,
            fg_color=colors["bg_primary"],
            corner_radius=12,
            border_width=1,
            border_color=colors["border"],
            **kwargs
        )
        
        self.transcription = transcription
        self.colors = colors
        
        # Card padding
        self.grid_columnconfigure(0, weight=1)
        
        # Header with metadata
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", padx=16, pady=(12, 8))
        header_frame.grid_columnconfigure(0, weight=1)
        
        timestamp = transcription.get("timestamp", "")
        duration = transcription.get("duration", 0)
        language = transcription.get("detected_language", "")
        
        # Metadata text
        meta_parts = []
        if timestamp:
            meta_parts.append(f"📅 {timestamp}")
        if duration:
            meta_parts.append(f"⏱ {duration:.1f}s")
        if language:
            meta_parts.append(f"🌍 {language.upper()}")
        
        meta_text = "  •  ".join(meta_parts)
        
        meta_label = ctk.CTkLabel(
            header_frame,
            text=meta_text,
            font=("SF Pro Text", 11),
            text_color=colors["text_secondary"],
            anchor="w"
        )
        meta_label.grid(row=0, column=0, sticky="w")
        
        # Transcription text
        text = transcription.get("text", "")
        text_label = ctk.CTkLabel(
            self,
            text=text,
            font=("SF Pro Text", 14),
            text_color=colors["text_primary"],
            anchor="w",
            justify="left",
            wraplength=700
        )
        text_label.grid(row=1, column=0, sticky="ew", padx=16, pady=(0, 12))
        
        # Action buttons
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=2, column=0, sticky="ew", padx=16, pady=(0, 12))
        
        copy_btn = AppleButton(
            action_frame,
            text="Copy",
            style="secondary",
            width=70,
            height=28,
            font=("SF Pro Text", 12),
            command=lambda: on_copy(text)
        )
        copy_btn.pack(side="left", padx=(0, 6))
        
        paste_btn = AppleButton(
            action_frame,
            text="Paste",
            style="secondary",
            width=70,
            height=28,
            font=("SF Pro Text", 12),
            command=lambda: on_paste(text)
        )
        paste_btn.pack(side="left", padx=(0, 6))
        
        delete_btn = AppleButton(
            action_frame,
            text="Delete",
            style="minimal",
            width=70,
            height=28,
            font=("SF Pro Text", 12),
            command=lambda: on_delete(transcription.get("id"))
        )
        delete_btn.pack(side="right")


class CollapsibleSection(ctk.CTkFrame):
    """Collapsible section for settings"""
    
    def __init__(self, master, title: str, theme: str = "light", **kwargs):
        colors = COLORS_LIGHT if theme == "light" else COLORS_DARK
        
        super().__init__(
            master,
            fg_color="transparent",
            **kwargs
        )
        
        self.colors = colors
        self.is_expanded = False
        
        # Header button
        self.header_btn = ctk.CTkButton(
            self,
            text=f"▸ {title}",
            anchor="w",
            fg_color="transparent",
            hover_color=colors["bg_tertiary"],
            text_color=colors["text_primary"],
            font=("SF Pro Display", 15, "bold"),
            height=40,
            corner_radius=8,
            command=self.toggle
        )
        self.header_btn.pack(fill="x")
        
        # Content frame (hidden by default)
        self.content = ctk.CTkFrame(
            self,
            fg_color=colors["bg_secondary"],
            corner_radius=10
        )
        self.title = title
    
    def toggle(self):
        """Toggle section expansion"""
        self.is_expanded = not self.is_expanded
        
        if self.is_expanded:
            self.header_btn.configure(text=f"▾ {self.title}")
            self.content.pack(fill="x", pady=(4, 0))
        else:
            self.header_btn.configure(text=f"▸ {self.title}")
            self.content.pack_forget()
    
    def get_content_frame(self):
        """Get the content frame for adding widgets"""
        return self.content


class MainWindowApple:
    """Apple-inspired main window with single-page layout"""
    
    def __init__(self, title: str = "VoiceSnap"):
        """Initialize main window"""
        self.theme = "light"  # Start with light theme
        self.colors = COLORS_LIGHT
        
        # Configure CustomTkinter
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title(title)
        self.root.geometry("800x900")
        self.root.minsize(700, 600)
        
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
        self.search_var.trace('w', self._on_search_changed)
        
        # UI elements
        self.main_scroll: Optional[ctk.CTkScrollableFrame] = None
        self.history_container: Optional[ctk.CTkFrame] = None
        self.status_label: Optional[ctk.CTkLabel] = None
        
        # Build UI
        self._create_ui()
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_ui(self):
        """Create the Apple-style user interface"""
        # Main container with background
        self.root.configure(fg_color=self.colors["bg_secondary"])
        
        # Header
        self._create_header()
        
        # Main scrollable content
        self.main_scroll = ctk.CTkScrollableFrame(
            self.root,
            fg_color="transparent",
            scrollbar_button_color=self.colors["text_secondary"],
            scrollbar_button_hover_color=self.colors["text_primary"]
        )
        self.main_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        self.main_scroll.grid_columnconfigure(0, weight=1)
        
        # Search section
        self._create_search_section()
        
        # Transcription history
        self._create_history_section()
        
        # Settings (collapsible)
        self._create_settings_section()
        
        # Footer status
        self._create_footer()
    
    def _create_header(self):
        """Create minimalist header"""
        header = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_primary"],
            height=70,
            corner_radius=0
        )
        header.pack(fill="x", padx=0, pady=0)
        header.pack_propagate(False)
        
        # Content container
        header_content = ctk.CTkFrame(header, fg_color="transparent")
        header_content.pack(fill="both", expand=True, padx=30, pady=15)
        
        # Title with icon
        title_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        title_frame.pack(side="left")
        
        title = ctk.CTkLabel(
            title_frame,
            text="🎤  VoiceSnap",
            font=("SF Pro Display", 24, "bold"),
            text_color=self.colors["text_primary"]
        )
        title.pack(side="left")
        
        # Version badge
        version = ctk.CTkLabel(
            title_frame,
            text="2.1",
            font=("SF Pro Text", 11),
            text_color=self.colors["text_secondary"],
            fg_color=self.colors["bg_tertiary"],
            corner_radius=6,
            padx=8,
            pady=2
        )
        version.pack(side="left", padx=(10, 0))
        
        # Right side buttons
        button_frame = ctk.CTkFrame(header_content, fg_color="transparent")
        button_frame.pack(side="right")
        
        # Theme toggle
        self.theme_btn = AppleButton(
            button_frame,
            text="🌙",
            style="minimal",
            width=36,
            height=36,
            font=("SF Pro Text", 16),
            command=self._toggle_theme
        )
        self.theme_btn.pack(side="right", padx=(8, 0))
    
    def _create_search_section(self):
        """Create search bar"""
        search_frame = ctk.CTkFrame(
            self.main_scroll,
            fg_color=self.colors["bg_primary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        search_frame.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Search input
        search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="🔍 Search transcriptions...",
            font=("SF Pro Text", 14),
            fg_color="transparent",
            border_width=0,
            height=44
        )
        search_entry.grid(row=0, column=0, sticky="ew", padx=16, pady=8)
    
    def _create_history_section(self):
        """Create history section"""
        # Section header
        header_frame = ctk.CTkFrame(self.main_scroll, fg_color="transparent")
        header_frame.grid(row=1, column=0, sticky="ew", pady=(0, 12))
        header_frame.grid_columnconfigure(0, weight=1)
        
        header_label = ctk.CTkLabel(
            header_frame,
            text="Recent Transcriptions",
            font=("SF Pro Display", 18, "bold"),
            text_color=self.colors["text_primary"],
            anchor="w"
        )
        header_label.grid(row=0, column=0, sticky="w")
        
        # History container
        self.history_container = ctk.CTkFrame(
            self.main_scroll,
            fg_color="transparent"
        )
        self.history_container.grid(row=2, column=0, sticky="ew")
        self.history_container.grid_columnconfigure(0, weight=1)
        
        # Placeholder
        self._show_history_placeholder()
    
    def _show_history_placeholder(self):
        """Show placeholder when no transcriptions"""
        placeholder_frame = ctk.CTkFrame(
            self.history_container,
            fg_color=self.colors["bg_primary"],
            corner_radius=12,
            border_width=1,
            border_color=self.colors["border"]
        )
        placeholder_frame.grid(row=0, column=0, sticky="ew", pady=8)
        
        placeholder = ctk.CTkLabel(
            placeholder_frame,
            text="No transcriptions yet\n\nPress Ctrl+Space to start recording",
            font=("SF Pro Text", 14),
            text_color=self.colors["text_secondary"],
            justify="center"
        )
        placeholder.pack(pady=60)
    
    def _create_settings_section(self):
        """Create collapsible settings section"""
        settings_header = ctk.CTkLabel(
            self.main_scroll,
            text="Settings",
            font=("SF Pro Display", 18, "bold"),
            text_color=self.colors["text_primary"],
            anchor="w"
        )
        settings_header.grid(row=3, column=0, sticky="w", pady=(24, 12))
        
        # Audio settings
        audio_section = CollapsibleSection(
            self.main_scroll,
            title="Audio",
            theme=self.theme
        )
        audio_section.grid(row=4, column=0, sticky="ew", pady=4)
        
        audio_content = audio_section.get_content_frame()
        audio_content.grid_columnconfigure(1, weight=1)
        
        # Microphone
        ctk.CTkLabel(
            audio_content,
            text="Microphone",
            font=("SF Pro Text", 13),
            text_color=self.colors["text_secondary"]
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 8))
        
        self.microphone_menu = ctk.CTkOptionMenu(
            audio_content,
            variable=self.microphone_var,
            values=["Default"],
            font=("SF Pro Text", 13),
            fg_color=self.colors["bg_tertiary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["bg_primary"],
            command=self._on_setting_changed
        )
        self.microphone_menu.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))
        
        # Whisper settings
        whisper_section = CollapsibleSection(
            self.main_scroll,
            title="Whisper Model",
            theme=self.theme
        )
        whisper_section.grid(row=5, column=0, sticky="ew", pady=4)
        
        whisper_content = whisper_section.get_content_frame()
        whisper_content.grid_columnconfigure(1, weight=1)
        
        # Model selection
        ctk.CTkLabel(
            whisper_content,
            text="Model Size",
            font=("SF Pro Text", 13),
            text_color=self.colors["text_secondary"]
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 8))
        
        model_menu = ctk.CTkOptionMenu(
            whisper_content,
            variable=self.model_var,
            values=["tiny", "base", "small", "medium", "large"],
            font=("SF Pro Text", 13),
            fg_color=self.colors["bg_tertiary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["bg_primary"],
            command=self._on_setting_changed
        )
        model_menu.grid(row=1, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 8))
        
        # Model info
        model_info = ctk.CTkLabel(
            whisper_content,
            text="• tiny: Fast, simple transcriptions\n"
                 "• base: Balanced (recommended)\n"
                 "• small/medium/large: Higher accuracy, slower",
            font=("SF Pro Text", 11),
            text_color=self.colors["text_secondary"],
            justify="left",
            anchor="w"
        )
        model_info.grid(row=2, column=0, columnspan=2, sticky="w", padx=16, pady=(0, 12))
        
        # Language
        ctk.CTkLabel(
            whisper_content,
            text="Language",
            font=("SF Pro Text", 13),
            text_color=self.colors["text_secondary"]
        ).grid(row=3, column=0, sticky="w", padx=16, pady=(8, 8))
        
        lang_menu = ctk.CTkOptionMenu(
            whisper_content,
            variable=self.language_var,
            values=["Auto-detect", "English", "French", "Spanish", "German", "Italian", "Portuguese"],
            font=("SF Pro Text", 13),
            fg_color=self.colors["bg_tertiary"],
            button_color=self.colors["accent"],
            button_hover_color=self.colors["accent_hover"],
            dropdown_fg_color=self.colors["bg_primary"],
            command=self._on_setting_changed
        )
        lang_menu.grid(row=4, column=0, columnspan=2, sticky="ew", padx=16, pady=(0, 12))
        
        # Hotkey settings
        hotkey_section = CollapsibleSection(
            self.main_scroll,
            title="Hotkey",
            theme=self.theme
        )
        hotkey_section.grid(row=6, column=0, sticky="ew", pady=4)
        
        hotkey_content = hotkey_section.get_content_frame()
        hotkey_content.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(
            hotkey_content,
            text="Current Hotkey",
            font=("SF Pro Text", 13),
            text_color=self.colors["text_secondary"]
        ).grid(row=0, column=0, sticky="w", padx=16, pady=(12, 8))
        
        hotkey_display = ctk.CTkLabel(
            hotkey_content,
            textvariable=self.hotkey_var,
            font=("SF Pro Display", 15, "bold"),
            text_color=self.colors["accent"]
        )
        hotkey_display.grid(row=0, column=1, sticky="e", padx=16, pady=(12, 8))
        
        # Behavior settings
        behavior_section = CollapsibleSection(
            self.main_scroll,
            title="Behavior",
            theme=self.theme
        )
        behavior_section.grid(row=7, column=0, sticky="ew", pady=4)
        
        behavior_content = behavior_section.get_content_frame()
        
        auto_paste_check = ctk.CTkCheckBox(
            behavior_content,
            text="Auto-paste after transcription",
            variable=self.auto_paste_var,
            font=("SF Pro Text", 13),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            border_color=self.colors["border"],
            command=self._on_setting_changed
        )
        auto_paste_check.pack(anchor="w", padx=16, pady=(12, 8))
        
        minimize_check = ctk.CTkCheckBox(
            behavior_content,
            text="Minimize to system tray",
            variable=self.minimize_to_tray_var,
            font=("SF Pro Text", 13),
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            border_color=self.colors["border"],
            command=self._on_setting_changed
        )
        minimize_check.pack(anchor="w", padx=16, pady=(0, 12))
    
    def _create_footer(self):
        """Create footer status bar"""
        footer = ctk.CTkFrame(
            self.root,
            fg_color=self.colors["bg_primary"],
            height=44,
            corner_radius=0
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        footer_content = ctk.CTkFrame(footer, fg_color="transparent")
        footer_content.pack(fill="both", expand=True, padx=30, pady=0)
        
        # Status indicator
        status_dot = ctk.CTkLabel(
            footer_content,
            text="●",
            font=("SF Pro Text", 16),
            text_color=self.colors["success"]
        )
        status_dot.pack(side="left", padx=(0, 8))
        
        self.status_label = ctk.CTkLabel(
            footer_content,
            text="Ready  •  Ctrl+Space to record",
            font=("SF Pro Text", 12),
            text_color=self.colors["text_secondary"],
            anchor="w"
        )
        self.status_label.pack(side="left", fill="x", expand=True)
        
        # Version
        version_label = ctk.CTkLabel(
            footer_content,
            text="v2.1",
            font=("SF Pro Text", 11),
            text_color=self.colors["text_secondary"]
        )
        version_label.pack(side="right")
    
    def _toggle_theme(self):
        """Toggle between light and dark theme"""
        self.theme = "dark" if self.theme == "light" else "light"
        self.colors = COLORS_DARK if self.theme == "dark" else COLORS_LIGHT
        
        # Update appearance
        ctk.set_appearance_mode(self.theme)
        self.theme_btn.configure(text="☀️" if self.theme == "dark" else "🌙")
        
        # Refresh UI (simplified - full implementation would update all widgets)
        self.set_status("Theme updated to " + self.theme.capitalize())
        
        # Note: Full theme refresh would require rebuilding UI or updating each widget's colors
        # For production, consider using CTk's built-in theme system more extensively
    
    def _on_setting_changed(self, *args):
        """Handle settings change"""
        if self.on_settings_changed:
            self.on_settings_changed()
    
    def _on_search_changed(self, *args):
        """Handle search text change"""
        search_term = self.search_var.get().lower()
        
        if search_term:
            filtered = [
                t for t in self.history_items
                if search_term in t.get("text", "").lower()
            ]
            self.update_history(filtered)
        else:
            self.update_history(self.history_items)
    
    def _on_close(self):
        """Handle window close"""
        if self.on_close:
            self.on_close()
        else:
            self.root.quit()
    
    def set_microphones(self, devices: List[Dict]):
        """Set available microphones"""
        if not devices:
            values = ["Default (No devices found)"]
        else:
            values = [f"{d['name']} (#{d['index']})" for d in devices]
        
        self.microphone_menu.configure(values=values)
        if values:
            self.microphone_var.set(values[0])
    
    def update_history(self, transcriptions: List[Dict]):
        """Update history display"""
        # Clear existing
        for widget in self.history_container.winfo_children():
            widget.destroy()
        
        if not transcriptions:
            self._show_history_placeholder()
            return
        
        # Create cards
        for idx, trans in enumerate(transcriptions):
            card = TranscriptionCard(
                self.history_container,
                transcription=trans,
                on_copy=self._copy_text,
                on_paste=self._paste_text,
                on_delete=self._delete_transcription,
                theme=self.theme
            )
            card.grid(row=idx, column=0, sticky="ew", pady=6)
    
    def _copy_text(self, text: str):
        """Copy text to clipboard"""
        pyperclip.copy(text)
        self.set_status("Copied to clipboard")
    
    def _paste_text(self, text: str):
        """Paste text to active window"""
        from pynput.keyboard import Controller, Key
        import sys
        
        pyperclip.copy(text)
        keyboard = Controller()
        
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
        self.set_status(f"Deleting transcription #{transcription_id}")
        # TODO: Implement with callback
    
    def set_status(self, message: str):
        """Set status bar message"""
        if self.status_label:
            self.status_label.configure(text=message)
    
    def get_settings(self) -> Dict:
        """Get current settings"""
        return {
            "microphone": self.microphone_var.get(),
            "model": self.model_var.get(),
            "language": self.language_var.get(),
            "hotkey": self.hotkey_var.get(),
            "auto_paste": self.auto_paste_var.get(),
            "minimize_to_tray": self.minimize_to_tray_var.get()
        }
    
    def set_settings(self, settings: Dict):
        """Set settings values"""
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
