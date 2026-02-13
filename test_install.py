#!/usr/bin/env python3
"""Test VoiceSnap installation and dependencies"""

import sys
import importlib
from pathlib import Path

def test_python_version():
    """Test Python version"""
    print("🐍 Testing Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✓ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (need 3.8+)")
        return False

def test_dependency(module_name, display_name=None):
    """Test if a dependency is installed"""
    if display_name is None:
        display_name = module_name
    
    try:
        importlib.import_module(module_name)
        print(f"   ✓ {display_name}")
        return True
    except ImportError:
        print(f"   ❌ {display_name} not installed")
        return False

def test_ffmpeg():
    """Test if ffmpeg is available"""
    print("🎬 Testing ffmpeg...")
    import subprocess
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            version = result.stdout.decode().split('\n')[0]
            print(f"   ✓ {version}")
            return True
        else:
            print("   ❌ ffmpeg found but returned error")
            return False
    except FileNotFoundError:
        print("   ❌ ffmpeg not found in PATH")
        return False
    except Exception as e:
        print(f"   ❌ Error testing ffmpeg: {e}")
        return False

def test_file_structure():
    """Test file structure"""
    print("📁 Testing file structure...")
    
    required_files = [
        'voicesnap_v2.py',
        'requirements_v2.txt',
        'src/__init__.py',
        'src/config.py',
        'src/database.py',
        'src/core/recorder.py',
        'src/core/transcriber.py',
        'src/core/hotkey_manager.py',
        'src/ui/main_window.py',
        'src/ui/overlay.py',
        'src/ui/system_tray.py',
    ]
    
    root = Path(__file__).parent
    all_present = True
    
    for file_path in required_files:
        full_path = root / file_path
        if full_path.exists():
            print(f"   ✓ {file_path}")
        else:
            print(f"   ❌ {file_path} missing")
            all_present = False
    
    return all_present

def test_imports():
    """Test VoiceSnap imports"""
    print("📦 Testing VoiceSnap imports...")
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    imports = [
        ('src.config', 'Config'),
        ('src.database', 'TranscriptionDB'),
        ('src.core.recorder', 'AudioRecorder'),
        ('src.core.transcriber', 'Transcriber'),
        ('src.core.hotkey_manager', 'HotkeyManager'),
        ('src.ui.main_window', 'MainWindow'),
        ('src.ui.overlay', 'RecordingOverlay'),
        ('src.ui.system_tray', 'SystemTray'),
    ]
    
    all_ok = True
    for module_name, class_name in imports:
        try:
            module = importlib.import_module(module_name)
            if hasattr(module, class_name):
                print(f"   ✓ {module_name}.{class_name}")
            else:
                print(f"   ❌ {class_name} not found in {module_name}")
                all_ok = False
        except Exception as e:
            print(f"   ❌ {module_name}: {e}")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 60)
    print("🔍 VoiceSnap Installation Test")
    print("=" * 60)
    print()
    
    results = []
    
    # Test Python
    results.append(("Python version", test_python_version()))
    print()
    
    # Test dependencies
    print("📚 Testing dependencies...")
    deps = [
        ('whisper', 'openai-whisper'),
        ('torch', 'PyTorch'),
        ('numpy', 'NumPy'),
        ('sounddevice', 'sounddevice'),
        ('soundfile', 'soundfile'),
        ('customtkinter', 'CustomTkinter'),
        ('PIL', 'Pillow'),
        ('pynput', 'pynput'),
        ('pyperclip', 'pyperclip'),
        ('pystray', 'pystray'),
    ]
    
    deps_ok = all(test_dependency(module, name) for module, name in deps)
    results.append(("Dependencies", deps_ok))
    print()
    
    # Test ffmpeg
    results.append(("ffmpeg", test_ffmpeg()))
    print()
    
    # Test file structure
    results.append(("File structure", test_file_structure()))
    print()
    
    # Test imports
    results.append(("VoiceSnap imports", test_imports()))
    print()
    
    # Summary
    print("=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status:10} {name}")
    
    print()
    
    if all(result[1] for result in results):
        print("🎉 All tests passed! VoiceSnap is ready to run.")
        print()
        print("Start VoiceSnap with:")
        print("  python3 voicesnap_v2.py")
        print("  or")
        print("  ./run.sh")
        return 0
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
        print()
        print("To install dependencies:")
        print("  pip install -r requirements_v2.txt")
        print()
        print("To install ffmpeg:")
        print("  macOS:   brew install ffmpeg")
        print("  Linux:   sudo apt install ffmpeg")
        print("  Windows: choco install ffmpeg")
        return 1

if __name__ == "__main__":
    sys.exit(main())
