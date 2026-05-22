#!/usr/bin/env python3
"""
Jarvis Launcher - Automatically launches GUI if available, falls back to terminal
This is the recommended entry point for Jarvis
"""

import sys
import os

def main():
    """Main launcher function"""
    
    # Try to import tkinter for GUI
    try:
        import tkinter as tk
        print("[*] GUI available - launching Jarvis with graphical interface...")
        
        # Import and run GUI
        from jarvis_gui import run_gui
        run_gui()
        
    except ImportError:
        print("[*] tkinter not available - using terminal interface...")
        print("[*] For GUI support, install: python -m pip install tk")
        print()
        
        # Fallback to terminal
        from jarvis_main import Jarvis
        jarvis = Jarvis()
        jarvis.run()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[*] Jarvis shutting down...")
        sys.exit(0)
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
