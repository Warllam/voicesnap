"""Recording overlay window with waveform visualization"""

import tkinter as tk
import threading
import numpy as np
from typing import Optional

class RecordingOverlay:
    """Transparent overlay window showing recording status and waveform"""
    
    def __init__(self, position: str = "top", height: int = 80):
        """Initialize recording overlay
        
        Args:
            position: Window position ('top' or 'bottom')
            height: Window height in pixels
        """
        self.position = position
        self.height = height
        
        self.window: Optional[tk.Toplevel] = None
        self.canvas: Optional[tk.Canvas] = None
        self.is_visible = False
        
        self.waveform_data = np.array([])
        self.animation_running = False
        self.duration = 0.0
        
        # Colors
        self.bg_color = "#1a1a1a"
        self.wave_color = "#00ff00"
        self.text_color = "#ffffff"
    
    def show(self, root: tk.Tk):
        """Show the overlay window
        
        Args:
            root: Parent Tkinter root window
        """
        if self.is_visible:
            return
        
        self.is_visible = True
        
        # Create window
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)  # Remove window decorations
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate window position
        if self.position == "top":
            y_pos = 0
        else:  # bottom
            y_pos = screen_height - self.height
        
        # Set window geometry
        self.window.geometry(f"{screen_width}x{self.height}+0+{y_pos}")
        
        # Make window always on top
        self.window.attributes("-topmost", True)
        
        # Make window transparent
        self.window.attributes("-alpha", 0.9)
        
        # Set background color
        self.window.configure(bg=self.bg_color)
        
        # Create canvas for waveform
        self.canvas = tk.Canvas(
            self.window,
            width=screen_width,
            height=self.height,
            bg=self.bg_color,
            highlightthickness=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Draw initial UI
        self._draw_ui()
        
        # Start animation
        self.animation_running = True
        self._animate()
    
    def hide(self):
        """Hide the overlay window"""
        if not self.is_visible:
            return
        
        self.animation_running = False
        self.is_visible = False
        
        if self.window:
            self.window.destroy()
            self.window = None
            self.canvas = None
    
    def update_waveform(self, audio_data: np.ndarray):
        """Update waveform data
        
        Args:
            audio_data: Audio data as numpy array
        """
        if audio_data is not None and len(audio_data) > 0:
            # Flatten if multi-channel
            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()
            
            # Downsample for visualization
            target_samples = 500
            if len(audio_data) > target_samples:
                step = len(audio_data) // target_samples
                audio_data = audio_data[::step]
            
            self.waveform_data = audio_data
    
    def update_duration(self, duration: float):
        """Update recording duration
        
        Args:
            duration: Duration in seconds
        """
        self.duration = duration
    
    def _draw_ui(self):
        """Draw the UI elements"""
        if not self.canvas:
            return
        
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        if width <= 1:
            width = self.canvas.winfo_reqwidth()
        
        height = self.canvas.winfo_height()
        if height <= 1:
            height = self.canvas.winfo_reqheight()
        
        # Draw recording indicator
        indicator_x = 30
        indicator_y = height // 2
        indicator_radius = 8
        
        self.canvas.create_oval(
            indicator_x - indicator_radius,
            indicator_y - indicator_radius,
            indicator_x + indicator_radius,
            indicator_y + indicator_radius,
            fill="#ff0000",
            outline=""
        )
        
        # Draw "Recording" text
        self.canvas.create_text(
            indicator_x + 25,
            indicator_y,
            text="Recording",
            fill=self.text_color,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        
        # Draw duration
        duration_text = f"{int(self.duration)}s"
        self.canvas.create_text(
            indicator_x + 120,
            indicator_y,
            text=duration_text,
            fill=self.text_color,
            font=("Arial", 11),
            anchor="w"
        )
        
        # Draw waveform
        if len(self.waveform_data) > 0:
            self._draw_waveform(width, height)
        else:
            # Draw empty waveform placeholder
            center_y = height // 2
            self.canvas.create_line(
                200, center_y,
                width - 50, center_y,
                fill=self.wave_color,
                width=1
            )
    
    def _draw_waveform(self, width: int, height: int):
        """Draw the audio waveform
        
        Args:
            width: Canvas width
            height: Canvas height
        """
        if len(self.waveform_data) == 0:
            return
        
        # Waveform area
        wave_start_x = 200
        wave_end_x = width - 50
        wave_width = wave_end_x - wave_start_x
        
        if wave_width <= 0:
            return
        
        center_y = height // 2
        max_amplitude = height // 3
        
        # Normalize waveform data
        data = self.waveform_data
        if len(data) > wave_width:
            # Downsample to fit width
            step = len(data) / wave_width
            indices = np.arange(0, len(data), step).astype(int)
            data = data[indices[:wave_width]]
        
        # Normalize amplitude
        max_val = np.max(np.abs(data)) if len(data) > 0 else 1
        if max_val > 0:
            data = data / max_val * max_amplitude
        
        # Draw waveform
        points = []
        for i, amplitude in enumerate(data):
            x = wave_start_x + (i / len(data)) * wave_width
            y = center_y - amplitude
            points.append((x, y))
        
        # Draw as smooth line
        if len(points) > 1:
            flat_points = []
            for x, y in points:
                flat_points.extend([x, y])
            
            self.canvas.create_line(
                *flat_points,
                fill=self.wave_color,
                width=2,
                smooth=True
            )
    
    def _animate(self):
        """Animation loop"""
        if not self.animation_running or not self.window:
            return
        
        # Redraw UI
        self._draw_ui()
        
        # Schedule next frame
        if self.window:
            self.window.after(50, self._animate)  # ~20 FPS
    
    def set_colors(self, bg_color: str, wave_color: str, text_color: str):
        """Set overlay colors
        
        Args:
            bg_color: Background color (hex)
            wave_color: Waveform color (hex)
            text_color: Text color (hex)
        """
        self.bg_color = bg_color
        self.wave_color = wave_color
        self.text_color = text_color
