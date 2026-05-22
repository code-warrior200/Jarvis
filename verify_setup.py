#!/usr/bin/env python3
"""
Jarvis Setup Verification - Check if everything is ready
"""

import sys
import os
from pathlib import Path

def check_files():
    """Check if all required files exist"""
    print("\n📁 Checking files...")
    required_files = [
        'jarvis.py',
        'jarvis_gui.py',
        'jarvis_main.py',
        'requirements.txt',
        'run.py',
    ]
    
    missing = []
    for file in required_files:
        path = Path(file)
        if path.exists():
            print(f"   ✓ {file}")
        else:
            print(f"   ✗ {file} - MISSING")
            missing.append(file)
    
    return len(missing) == 0

def check_imports():
    """Check if core imports work"""
    print("\n🔧 Checking imports...")
    
    imports = {
        'tkinter': 'GUI Framework',
        'pyttsx3': 'Text-to-Speech',
        'speech_recognition': 'Voice Recognition',
        'pyaudio': 'Audio Input',
        'requests': 'Web Requests',
        'cv2': 'Face Detection (Optional)',
        'pygetwindow': 'Window Management',
        'pyautogui': 'System Automation',
        'psutil': 'System Monitoring',
    }
    
    optional = ['cv2', 'llama_cpp', 'transformers']
    missing = []
    
    for module, description in imports.items():
        try:
            __import__(module)
            is_optional = module in optional
            marker = "○" if is_optional else "✓"
            print(f"   {marker} {module:20} - {description}")
        except ImportError:
            is_optional = module in optional
            marker = "○" if is_optional else "✗"
            print(f"   {marker} {module:20} - {description}")
            if not is_optional:
                missing.append(module)
    
    return len(missing) == 0

def check_jarvis_core():
    """Check if Jarvis core imports work"""
    print("\n🤖 Checking Jarvis core...")
    
    try:
        from jarvis_main import Jarvis, WindowManager, SystemControl
        print("   ✓ jarvis_main imports successful")
        return True
    except Exception as e:
        print(f"   ✗ jarvis_main import failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("🔍 JARVIS SETUP VERIFICATION")
    print("=" * 60)
    
    all_good = True
    
    if not check_files():
        all_good = False
    
    if not check_imports():
        print("\n   ⚠️  Missing required packages!")
        print("   Run: python -m pip install -r requirements.txt")
        all_good = False
    
    if not check_jarvis_core():
        all_good = False
    
    print("\n" + "=" * 60)
    if all_good:
        print("✨ SETUP COMPLETE - Ready to launch Jarvis!")
        print("\nRun this to start:")
        print("   python run.py")
        print("=" * 60)
        return 0
    else:
        print("❌ Setup incomplete - Fix issues above")
        print("=" * 60)
        return 1

if __name__ == '__main__':
    sys.exit(main())
