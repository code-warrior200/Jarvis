#!/usr/bin/env python3
"""
Jarvis - Modern GUI AI Assistant
Simply run this to launch the beautiful Jarvis interface!
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

def start_gui():
    """Start Jarvis GUI application"""
    try:
        from jarvis.ui import JarvisGUI
        import tkinter as tk
        
        print("🚀 Launching Jarvis GUI...\n")
        
        root = tk.Tk()
        app = JarvisGUI(root)
        
        # Handle window close
        def on_closing():
            if app.jarvis:
                try:
                    root.destroy()
                except:
                    pass
                sys.exit(0)
        
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Error: Missing dependency: {e}")
        print("\n📦 Install dependencies with:")
        print("   python -m pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    try:
        start_gui()
    except KeyboardInterrupt:
        print("\n👋 Jarvis shutting down...")
        sys.exit(0)
