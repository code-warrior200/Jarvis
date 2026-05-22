#!/usr/bin/env python3
"""
🤖 JARVIS - Modern GUI AI Assistant
Simply run this file to launch the beautiful GUI!

Usage: python run.py
"""

import sys
import os
from pathlib import Path

def check_dependencies():
    """Check if required packages are installed"""
    missing = []
    
    required = {
        'tkinter': 'tk',
        'pyttsx3': 'pyttsx3',
        'speech_recognition': 'SpeechRecognition',
    }
    
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("❌ Missing dependencies:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\n📦 Install with: python -m pip install -r requirements.txt")
        return False
    return True

def main():
    """Main entry point"""
    print("🤖 JARVIS - Modern GUI AI Assistant")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Try GUI first
    try:
        import tkinter as tk
        print("✨ Launching GUI interface...\n")
        
        from jarvis_gui import JarvisGUI
        
        root = tk.Tk()
        app = JarvisGUI(root)
        
        # Handle close
        def on_close():
            try:
                app.quit_app()
            except:
                sys.exit(0)
        
        root.protocol("WM_DELETE_WINDOW", on_close)
        root.mainloop()
        
    except Exception as e:
        print(f"\n⚠️  GUI failed: {e}")
        print("\n💻 Trying terminal mode instead...\n")
        
        try:
            from jarvis_main import Jarvis
            jarvis = Jarvis()
            jarvis.run()
        except Exception as e2:
            print(f"\n❌ Error: {e2}")
            import traceback
            traceback.print_exc()
            sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Jarvis shutting down...")
        sys.exit(0)
