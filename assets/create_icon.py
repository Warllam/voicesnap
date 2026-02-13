#!/usr/bin/env python3
"""Generate VoiceSnap icon"""

from PIL import Image, ImageDraw

# Create a 256x256 image
size = 256
image = Image.new('RGBA', (size, size), color=(0, 0, 0, 0))
dc = ImageDraw.Draw(image)

# Background gradient circle
for i in range(size//2, 0, -1):
    opacity = int((i / (size/2)) * 100)
    color = (66, 135, 245, opacity)
    dc.ellipse([size//2 - i, size//2 - i, size//2 + i, size//2 + i], fill=color)

# Microphone icon (white)
color = (255, 255, 255)

# Microphone body
mic_width = 60
mic_height = 90
mic_x = (size - mic_width) // 2
mic_y = 50

dc.rounded_rectangle(
    [mic_x, mic_y, mic_x + mic_width, mic_y + mic_height],
    radius=30,
    fill=color
)

# Microphone arc (bottom)
arc_y = mic_y + mic_height + 10
arc_size = 40
dc.arc(
    [mic_x - arc_size//2, arc_y - 20, mic_x + mic_width + arc_size//2, arc_y + 40],
    start=180,
    end=0,
    fill=color,
    width=12
)

# Microphone stand
stand_x = size // 2
dc.line([stand_x, arc_y + 20, stand_x, arc_y + 60], fill=color, width=12)

# Stand base
base_width = 80
dc.rounded_rectangle(
    [stand_x - base_width//2, arc_y + 55, stand_x + base_width//2, arc_y + 70],
    radius=8,
    fill=color
)

# Save icon
image.save('icon.png')
print("✓ Icon created: assets/icon.png")
