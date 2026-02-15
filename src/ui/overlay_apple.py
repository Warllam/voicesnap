"""Apple-inspired minimalist recording overlay with glassmorphism"""

import tkinter as tk
import numpy as np
from typing import Optional
from PIL import Image, ImageFilter, ImageDraw, ImageTk
import math

class RecordingOverlayApple:
    """Ultra-minimal recording overlay with Apple-style glassmorphism"""
    
    def __init__(self, position: str = "top", style: str = "bar"):
        """Initialize recording overlay
        
        Args:
            position: Window position ('top', 'center')
            style: Overlay style ('bar', 'floating')
        """
        self.position = position
        self.style = style
        
        self.window: Optional[tk.Toplevel] = None
        self.canvas: Optional[tk.Canvas] = None
        self.is_visible = False
        
        self.waveform_data = np.array([])
        self.animation_running = False
        self.duration = 0.0
        self.pulse_phase = 0.0
        
        # Apple Design Colors
        self.bg_color = "#F5F5F7"
        self.bg_alpha = 0.85
        self.accent_color = "#007AFF"
        self.text_color = "#1D1D1F"
        self.wave_color = "#007AFF"
        self.recording_color = "#FF3B30"
        
        # Dimensions
        if style == "floating":
            self.width = 320
            self.height = 100
        else:  # bar
            self.width = None  # Full width
            self.height = 60
    
    def show(self, root: tk.Tk):
        """Show the overlay window"""
        if self.is_visible:
            return
        
        self.is_visible = True
        
        # Create window
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate dimensions
        if self.style == "floating":
            width = self.width
            height = self.height
            
            if self.position == "center":
                x_pos = (screen_width - width) // 2
                y_pos = (screen_height - height) // 2
            else:  # top
                x_pos = (screen_width - width) // 2
                y_pos = 40
        else:  # bar
            width = screen_width
            height = self.height
            x_pos = 0
            
            if self.position == "top":
                y_pos = 0
            else:  # center
                y_pos = (screen_height - height) // 2
        
        # Set window geometry
        self.window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        
        # Window attributes
        self.window.attributes("-topmost", True)
        self.window.attributes("-alpha", self.bg_alpha)
        
        # Try to enable transparency (platform-specific)
        try:
            self.window.wm_attributes("-transparentcolor", "systemTransparent")
        except:
            pass
        
        # Background
        self.window.configure(bg=self.bg_color)
        
        # Create canvas
        self.canvas = tk.Canvas(
            self.window,
            width=width,
            height=height,
            bg=self.bg_color,
            highlightthickness=0,
            bd=0
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Add subtle border for floating style
        if self.style == "floating":
            self._draw_rounded_rect(
                0, 0, width, height,
                radius=16,
                outline="#D2D2D7",
                width=1
            )
        
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
        """Update waveform data"""
        if audio_data is not None and len(audio_data) > 0:
            if audio_data.ndim > 1:
                audio_data = audio_data.flatten()
            
            max_samples = 1000
            if len(self.waveform_data) > 0:
                self.waveform_data = np.concatenate([self.waveform_data, audio_data])
                if len(self.waveform_data) > max_samples:
                    self.waveform_data = self.waveform_data[-max_samples:]
            else:
                self.waveform_data = audio_data
    
    def update_duration(self, duration: float):
        """Update recording duration"""
        self.duration = duration
    
    def _draw_rounded_rect(self, x1, y1, x2, y2, radius=12, **kwargs):
        """Draw rounded rectangle (helper)"""
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.canvas.create_polygon(points, smooth=True, **kwargs)
    
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
        
        center_y = height // 2
        
        if self.style == "floating":
            # Floating card style
            padding = 20
            
            # Pulsing recording dot
            dot_x = padding + 8
            dot_y = center_y
            dot_radius = 6
            
            # Pulse effect
            pulse_scale = 1.0 + 0.2 * math.sin(self.pulse_phase)
            pulse_radius = dot_radius * pulse_scale
            
            # Outer pulse
            self.canvas.create_oval(
                dot_x - pulse_radius * 1.5,
                dot_y - pulse_radius * 1.5,
                dot_x + pulse_radius * 1.5,
                dot_y + pulse_radius * 1.5,
                fill="",
                outline=self.recording_color,
                width=1
            )
            
            # Recording dot
            self.canvas.create_oval(
                dot_x - dot_radius,
                dot_y - dot_radius,
                dot_x + dot_radius,
                dot_y + dot_radius,
                fill=self.recording_color,
                outline=""
            )
            
            # Duration
            duration_text = self._format_duration(self.duration)
            self.canvas.create_text(
                dot_x + 22,
                center_y,
                text=duration_text,
                fill=self.text_color,
                font=("SF Pro Display", 14, "bold"),
                anchor="w"
            )
            
            # Waveform (compact)
            wave_start_x = padding + 80
            wave_width = width - wave_start_x - padding
            self._draw_minimal_waveform(wave_start_x, center_y, wave_width, 24)
            
        else:
            # Bar style (full width)
            left_margin = 30
            
            # Recording indicator
            dot_x = left_margin + 6
            dot_y = center_y
            dot_radius = 5
            
            # Pulse
            pulse_scale = 1.0 + 0.15 * math.sin(self.pulse_phase)
            pulse_radius = dot_radius * pulse_scale
            
            self.canvas.create_oval(
                dot_x - pulse_radius * 1.3,
                dot_y - pulse_radius * 1.3,
                dot_x + pulse_radius * 1.3,
                dot_y + pulse_radius * 1.3,
                fill="",
                outline=self.recording_color,
                width=1
            )
            
            self.canvas.create_oval(
                dot_x - dot_radius,
                dot_y - dot_radius,
                dot_x + dot_radius,
                dot_y + dot_radius,
                fill=self.recording_color,
                outline=""
            )
            
            # Duration
            duration_text = self._format_duration(self.duration)
            self.canvas.create_text(
                dot_x + 20,
                center_y,
                text=duration_text,
                fill=self.text_color,
                font=("SF Pro Display", 13, "bold"),
                anchor="w"
            )
            
            # Waveform
            wave_start_x = left_margin + 100
            wave_end_x = width - 30
            wave_width = wave_end_x - wave_start_x
            
            if wave_width > 100:
                self._draw_minimal_waveform(wave_start_x, center_y, wave_width, 20)
    
    def _draw_minimal_waveform(self, start_x: int, center_y: int, width: int, max_height: int):
        """Draw subtle, minimalist waveform"""
        if len(self.waveform_data) == 0:
            # Draw flat line when no audio
            self.canvas.create_line(
                start_x, center_y,
                start_x + width, center_y,
                fill=self.wave_color,
                width=1
            )
            return
        
        # Sample data
        data = self.waveform_data
        num_bars = min(80, width // 4)
        
        if len(data) > num_bars:
            step = len(data) // num_bars
            indices = np.arange(0, len(data), step)[:num_bars]
            data = data[indices]
        
        # Normalize
        max_val = np.max(np.abs(data)) if len(data) > 0 else 1
        if max_val > 0:
            data = data / max_val
        
        # Draw as bars (Apple Music style)
        bar_width = max(2, width // len(data) - 1)
        
        for i, amplitude in enumerate(data):
            x = start_x + (i * (width / len(data)))
            bar_height = abs(amplitude) * max_height
            bar_height = max(2, bar_height)  # Minimum height
            
            # Subtle rounded bars
            self.canvas.create_rectangle(
                x, center_y - bar_height / 2,
                x + bar_width, center_y + bar_height / 2,
                fill=self.wave_color,
                outline="",
                width=0
            )
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration as MM:SS"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:01d}:{secs:02d}"
    
    def _animate(self):
        """Animation loop"""
        if not self.animation_running or not self.window:
            return
        
        # Update pulse phase
        self.pulse_phase += 0.15
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase = 0
        
        # Redraw UI
        self._draw_ui()
        
        # Schedule next frame (30 FPS for smoothness)
        if self.window:
            self.window.after(33, self._animate)
    
    def set_colors(self, bg_color: str, wave_color: str, text_color: str, recording_color: str):
        """Set overlay colors"""
        self.bg_color = bg_color
        self.wave_color = wave_color
        self.text_color = text_color
        self.recording_color = recording_color
    
    def set_theme(self, theme: str):
        """Set theme (light/dark)"""
        if theme == "dark":
            self.bg_color = "#1C1C1E"
            self.text_color = "#FFFFFF"
            self.wave_color = "#0A84FF"
            self.recording_color = "#FF453A"
            self.bg_alpha = 0.90
        else:  # light
            self.bg_color = "#F5F5F7"
            self.text_color = "#1D1D1F"
            self.wave_color = "#007AFF"
            self.recording_color = "#FF3B30"
            self.bg_alpha = 0.85
