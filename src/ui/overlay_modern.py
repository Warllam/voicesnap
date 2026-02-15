"""Modern, dynamic recording overlay with stunning visuals"""

import tkinter as tk
import numpy as np
from typing import Optional
import math
import colorsys

class RecordingOverlayModern:
    """Beautiful, modern recording overlay with dynamic animations"""
    
    def __init__(self, position: str = "center", style: str = "floating"):
        """Initialize recording overlay
        
        Args:
            position: Window position ('top', 'center', 'bottom')
            style: Overlay style ('floating', 'bar', 'minimal')
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
        self.wave_offset = 0.0
        
        # Modern Dark Theme Colors
        self.bg_color = "#1E1E2E"  # Rich dark blue-gray
        self.bg_gradient_start = "#1E1E2E"
        self.bg_gradient_end = "#2A2A3E"
        self.bg_alpha = 0.95
        
        self.accent_color = "#8B5CF6"  # Modern purple
        self.accent_glow = "#A78BFA"
        self.text_color = "#E5E7EB"
        self.text_dim = "#9CA3AF"
        
        self.wave_color_primary = "#8B5CF6"  # Purple
        self.wave_color_secondary = "#06B6D4"  # Cyan
        self.recording_color = "#EF4444"  # Modern red
        self.recording_glow = "#FCA5A5"
        
        # Dimensions
        if style == "floating":
            self.width = 400
            self.height = 120
        elif style == "minimal":
            self.width = 300
            self.height = 80
        else:  # bar
            self.width = None  # Full width
            self.height = 80
    
    def show(self, root: tk.Tk):
        """Show the overlay window with stunning entrance animation"""
        if self.is_visible:
            return
        
        self.is_visible = True
        
        # Create window
        self.window = tk.Toplevel(root)
        self.window.overrideredirect(True)
        
        # Get screen dimensions
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # Calculate dimensions and position
        if self.style in ["floating", "minimal"]:
            width = self.width
            height = self.height
            
            if self.position == "center":
                x_pos = (screen_width - width) // 2
                y_pos = (screen_height - height) // 2
            elif self.position == "bottom":
                x_pos = (screen_width - width) // 2
                y_pos = screen_height - height - 60
            else:  # top
                x_pos = (screen_width - width) // 2
                y_pos = 60
        else:  # bar
            width = screen_width
            height = self.height
            x_pos = 0
            
            if self.position == "bottom":
                y_pos = screen_height - height
            elif self.position == "center":
                y_pos = (screen_height - height) // 2
            else:  # top
                y_pos = 0
        
        # Set window geometry
        self.window.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        
        # Window attributes
        self.window.attributes("-topmost", True)
        
        # Try transparency
        try:
            self.window.attributes("-alpha", self.bg_alpha)
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
            
            max_samples = 1500
            if len(self.waveform_data) > 0:
                self.waveform_data = np.concatenate([self.waveform_data, audio_data])
                if len(self.waveform_data) > max_samples:
                    self.waveform_data = self.waveform_data[-max_samples:]
            else:
                self.waveform_data = audio_data
    
    def update_duration(self, duration: float):
        """Update recording duration"""
        self.duration = duration
    
    def _draw_gradient_bg(self, width: int, height: int):
        """Draw modern gradient background"""
        # Create subtle gradient from top to bottom
        steps = 30
        for i in range(steps):
            y1 = int((i / steps) * height)
            y2 = int(((i + 1) / steps) * height)
            
            # Interpolate colors
            ratio = i / steps
            color = self._interpolate_color(self.bg_gradient_start, self.bg_gradient_end, ratio)
            
            self.canvas.create_rectangle(
                0, y1, width, y2,
                fill=color,
                outline=""
            )
    
    def _interpolate_color(self, color1: str, color2: str, ratio: float) -> str:
        """Interpolate between two hex colors"""
        c1 = tuple(int(color1[i:i+2], 16) for i in (1, 3, 5))
        c2 = tuple(int(color2[i:i+2], 16) for i in (1, 3, 5))
        
        r = int(c1[0] + (c2[0] - c1[0]) * ratio)
        g = int(c1[1] + (c2[1] - c1[1]) * ratio)
        b = int(c1[2] + (c2[2] - c1[2]) * ratio)
        
        return f"#{r:02x}{g:02x}{b:02x}"
    
    def _draw_ui(self):
        """Draw the stunning UI"""
        if not self.canvas:
            return
        
        self.canvas.delete("all")
        
        width = self.canvas.winfo_width()
        if width <= 1:
            width = self.canvas.winfo_reqwidth()
        
        height = self.canvas.winfo_height()
        if height <= 1:
            height = self.canvas.winfo_reqheight()
        
        # Draw gradient background
        self._draw_gradient_bg(width, height)
        
        center_y = height // 2
        
        if self.style in ["floating", "minimal"]:
            self._draw_floating_style(width, height, center_y)
        else:
            self._draw_bar_style(width, height, center_y)
    
    def _draw_floating_style(self, width: int, height: int, center_y: int):
        """Draw floating card style with modern design"""
        padding = 24
        
        # Outer glow effect for recording indicator
        dot_x = padding + 12
        dot_y = center_y
        
        # Multi-layer pulse glow
        pulse_scale = 1.0 + 0.3 * math.sin(self.pulse_phase)
        
        # Outer glow (largest)
        glow_radius = 20 * pulse_scale
        self.canvas.create_oval(
            dot_x - glow_radius,
            dot_y - glow_radius,
            dot_x + glow_radius,
            dot_y + glow_radius,
            fill="",
            outline=self.recording_glow,
            width=2
        )
        
        # Mid glow
        mid_radius = 12 * pulse_scale
        self.canvas.create_oval(
            dot_x - mid_radius,
            dot_y - mid_radius,
            dot_x + mid_radius,
            dot_y + mid_radius,
            fill=self.recording_glow,
            outline=""
        )
        
        # Core dot
        core_radius = 6
        self.canvas.create_oval(
            dot_x - core_radius,
            dot_y - core_radius,
            dot_x + core_radius,
            dot_y + core_radius,
            fill=self.recording_color,
            outline=""
        )
        
        # Duration with modern font styling
        duration_text = self._format_duration(self.duration)
        self.canvas.create_text(
            dot_x + 40,
            center_y - 8,
            text=duration_text,
            fill=self.text_color,
            font=("Segoe UI", 18, "bold"),
            anchor="w"
        )
        
        # "Recording" label
        self.canvas.create_text(
            dot_x + 40,
            center_y + 12,
            text="RECORDING",
            fill=self.text_dim,
            font=("Segoe UI", 9, "bold"),
            anchor="w"
        )
        
        # Modern gradient waveform
        wave_start_x = padding + 140
        wave_width = width - wave_start_x - padding
        
        if wave_width > 50:
            self._draw_gradient_waveform(wave_start_x, center_y, wave_width, 30)
    
    def _draw_bar_style(self, width: int, height: int, center_y: int):
        """Draw bar style overlay"""
        left_margin = 40
        
        # Recording indicator with glow
        dot_x = left_margin + 8
        dot_y = center_y
        
        pulse_scale = 1.0 + 0.25 * math.sin(self.pulse_phase)
        
        # Glow
        glow_radius = 15 * pulse_scale
        self.canvas.create_oval(
            dot_x - glow_radius,
            dot_y - glow_radius,
            dot_x + glow_radius,
            dot_y + glow_radius,
            fill="",
            outline=self.recording_glow,
            width=2
        )
        
        # Core
        core_radius = 5
        self.canvas.create_oval(
            dot_x - core_radius,
            dot_y - core_radius,
            dot_x + core_radius,
            dot_y + core_radius,
            fill=self.recording_color,
            outline=""
        )
        
        # Duration
        duration_text = self._format_duration(self.duration)
        self.canvas.create_text(
            dot_x + 30,
            center_y,
            text=duration_text,
            fill=self.text_color,
            font=("Segoe UI", 16, "bold"),
            anchor="w"
        )
        
        # Waveform
        wave_start_x = left_margin + 120
        wave_end_x = width - 40
        wave_width = wave_end_x - wave_start_x
        
        if wave_width > 100:
            self._draw_gradient_waveform(wave_start_x, center_y, wave_width, 24)
    
    def _draw_gradient_waveform(self, start_x: int, center_y: int, width: int, max_height: int):
        """Draw beautiful gradient waveform with smooth bars"""
        if len(self.waveform_data) == 0:
            # Draw subtle baseline
            self.canvas.create_line(
                start_x, center_y,
                start_x + width, center_y,
                fill=self.wave_color_primary,
                width=1
            )
            return
        
        # Sample data
        data = self.waveform_data
        num_bars = min(100, width // 5)
        
        if len(data) > num_bars:
            step = len(data) // num_bars
            indices = np.arange(0, len(data), step)[:num_bars]
            data = data[indices]
        
        # Normalize
        max_val = np.max(np.abs(data)) if len(data) > 0 else 1
        if max_val > 0:
            data = data / max_val
        
        # Draw gradient bars
        bar_width = max(3, width // len(data) - 2)
        
        for i, amplitude in enumerate(data):
            x = start_x + (i * (width / len(data)))
            bar_height = abs(amplitude) * max_height
            bar_height = max(3, bar_height)  # Minimum height
            
            # Calculate gradient color (purple to cyan based on position)
            color_ratio = i / len(data)
            bar_color = self._interpolate_color(
                self.wave_color_primary,
                self.wave_color_secondary,
                color_ratio
            )
            
            # Draw rounded bar
            self._draw_rounded_bar(
                x, center_y - bar_height / 2,
                x + bar_width, center_y + bar_height / 2,
                radius=2,
                fill=bar_color
            )
    
    def _draw_rounded_bar(self, x1: float, y1: float, x2: float, y2: float, radius: int, fill: str):
        """Draw a rounded rectangle bar"""
        # Simplified rounded rect for bars
        self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=fill,
            outline="",
            width=0
        )
    
    def _format_duration(self, seconds: float) -> str:
        """Format duration as MM:SS"""
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:01d}:{secs:02d}"
    
    def _animate(self):
        """Smooth animation loop at 40 FPS"""
        if not self.animation_running or not self.window:
            return
        
        # Update animation phases
        self.pulse_phase += 0.12
        if self.pulse_phase > 2 * math.pi:
            self.pulse_phase = 0
        
        self.wave_offset += 0.05
        if self.wave_offset > 1.0:
            self.wave_offset = 0
        
        # Redraw UI
        self._draw_ui()
        
        # Schedule next frame (40 FPS for smoothness)
        if self.window:
            self.window.after(25, self._animate)
    
    def set_colors(self, bg_color: str, wave_color: str, text_color: str, recording_color: str):
        """Set overlay colors"""
        self.bg_color = bg_color
        self.wave_color_primary = wave_color
        self.text_color = text_color
        self.recording_color = recording_color
    
    def set_theme(self, theme: str):
        """Set theme (light/dark)"""
        if theme == "dark":
            self.bg_color = "#1E1E2E"
            self.bg_gradient_start = "#1E1E2E"
            self.bg_gradient_end = "#2A2A3E"
            self.text_color = "#E5E7EB"
            self.text_dim = "#9CA3AF"
            self.wave_color_primary = "#8B5CF6"
            self.wave_color_secondary = "#06B6D4"
            self.recording_color = "#EF4444"
            self.recording_glow = "#FCA5A5"
            self.accent_color = "#8B5CF6"
            self.accent_glow = "#A78BFA"
            self.bg_alpha = 0.95
        else:  # light
            self.bg_color = "#F9FAFB"
            self.bg_gradient_start = "#F9FAFB"
            self.bg_gradient_end = "#F3F4F6"
            self.text_color = "#1F2937"
            self.text_dim = "#6B7280"
            self.wave_color_primary = "#8B5CF6"
            self.wave_color_secondary = "#06B6D4"
            self.recording_color = "#EF4444"
            self.recording_glow = "#FCA5A5"
            self.accent_color = "#8B5CF6"
            self.accent_glow = "#A78BFA"
            self.bg_alpha = 0.92
