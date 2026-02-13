"""System tray icon and menu"""

import pystray
from PIL import Image, ImageDraw
from typing import Optional, Callable

class SystemTray:
    """System tray icon manager"""
    
    def __init__(self, app_name: str = "VoiceSnap"):
        """Initialize system tray
        
        Args:
            app_name: Application name
        """
        self.app_name = app_name
        self.icon: Optional[pystray.Icon] = None
        
        # Callbacks
        self.on_show: Optional[Callable] = None
        self.on_settings: Optional[Callable] = None
        self.on_quit: Optional[Callable] = None
        
        # State
        self.is_recording = False
    
    def create_icon(self, recording: bool = False) -> Image.Image:
        """Create tray icon image
        
        Args:
            recording: Whether to show recording indicator
            
        Returns:
            PIL Image for the icon
        """
        # Create a 64x64 image
        size = 64
        image = Image.new('RGB', (size, size), color=(0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        # Draw microphone icon
        color = (255, 0, 0) if recording else (255, 255, 255)
        
        # Microphone body (vertical rectangle)
        mic_width = 20
        mic_height = 30
        mic_x = (size - mic_width) // 2
        mic_y = 10
        dc.rectangle(
            [mic_x, mic_y, mic_x + mic_width, mic_y + mic_height],
            fill=color
        )
        
        # Microphone arc (bottom)
        arc_y = mic_y + mic_height
        dc.arc(
            [mic_x - 5, arc_y - 5, mic_x + mic_width + 5, arc_y + 15],
            start=180,
            end=0,
            fill=color,
            width=3
        )
        
        # Microphone stand
        stand_x = size // 2
        dc.line([stand_x, arc_y + 5, stand_x, arc_y + 15], fill=color, width=3)
        dc.line([stand_x - 8, arc_y + 15, stand_x + 8, arc_y + 15], fill=color, width=3)
        
        # Recording indicator (red dot)
        if recording:
            dc.ellipse([size - 20, 5, size - 5, 20], fill=(255, 0, 0))
        
        return image
    
    def create_menu(self) -> pystray.Menu:
        """Create tray menu
        
        Returns:
            pystray.Menu object
        """
        return pystray.Menu(
            pystray.MenuItem(
                "Show VoiceSnap",
                self._on_show_clicked,
                default=True
            ),
            pystray.MenuItem(
                "Settings",
                self._on_settings_clicked
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Quit",
                self._on_quit_clicked
            )
        )
    
    def start(self):
        """Start the system tray icon"""
        if self.icon is not None:
            return
        
        icon_image = self.create_icon(recording=False)
        menu = self.create_menu()
        
        self.icon = pystray.Icon(
            self.app_name,
            icon_image,
            self.app_name,
            menu
        )
        
        # Run in a separate thread
        import threading
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def stop(self):
        """Stop the system tray icon"""
        if self.icon:
            self.icon.stop()
            self.icon = None
    
    def update_icon(self, recording: bool):
        """Update icon to show recording status
        
        Args:
            recording: Whether recording is active
        """
        self.is_recording = recording
        
        if self.icon:
            icon_image = self.create_icon(recording=recording)
            self.icon.icon = icon_image
    
    def show_notification(self, title: str, message: str):
        """Show a system notification
        
        Args:
            title: Notification title
            message: Notification message
        """
        if self.icon:
            self.icon.notify(message, title)
    
    def _on_show_clicked(self):
        """Handle show menu item click"""
        if self.on_show:
            self.on_show()
    
    def _on_settings_clicked(self):
        """Handle settings menu item click"""
        if self.on_settings:
            self.on_settings()
    
    def _on_quit_clicked(self):
        """Handle quit menu item click"""
        if self.on_quit:
            self.on_quit()
        else:
            self.stop()
