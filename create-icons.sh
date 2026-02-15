#!/bin/bash
# Create placeholder icons for Tauri
# In production, use real icons with proper design

mkdir -p src-tauri/icons

# Create simple placeholder SVG
cat > src-tauri/icons/icon.svg << 'EOF'
<svg width="128" height="128" xmlns="http://www.w3.org/2000/svg">
  <rect width="128" height="128" rx="24" fill="#6366f1"/>
  <circle cx="64" cy="50" r="20" fill="white"/>
  <rect x="54" y="70" width="20" height="30" rx="3" fill="white"/>
  <path d="M 40 100 Q 64 110 88 100" stroke="white" stroke-width="4" fill="none"/>
</svg>
EOF

# Convert to PNG sizes (requires ImageMagick)
if command -v convert &> /dev/null; then
    convert src-tauri/icons/icon.svg -resize 32x32 src-tauri/icons/32x32.png
    convert src-tauri/icons/icon.svg -resize 128x128 src-tauri/icons/128x128.png
    convert src-tauri/icons/icon.svg -resize 256x256 src-tauri/icons/128x128@2x.png
    convert src-tauri/icons/icon.svg -resize 512x512 src-tauri/icons/icon.png
    echo "✅ Icons created successfully"
else
    echo "⚠️  ImageMagick not installed. Placeholder SVG created."
    echo "   Install ImageMagick: sudo apt install imagemagick"
    echo "   Or manually create PNG icons from icon.svg"
fi
