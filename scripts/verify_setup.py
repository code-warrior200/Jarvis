#!/usr/bin/env python3
"""Verify that the source checkout can import and run Jarvis."""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def check_files():
    """Check that the expected project files exist."""
    print("\nChecking files...")
    required_files = [
        "jarvis/__init__.py",
        "jarvis/core/assistant.py",
        "jarvis/ui/futuristic_gui.py",
        "jarvis/launcher.py",
        "requirements.txt",
        "run.py",
    ]

    missing = []
    for file_name in required_files:
        path = Path(file_name)
        if path.exists():
            print(f"   OK  {file_name}")
        else:
            print(f"   ERR {file_name} - MISSING")
            missing.append(file_name)

    return not missing


def check_imports():
    """Check optional and required third-party imports."""
    print("\nChecking imports...")

    imports = {
        "tkinter": "GUI Framework",
        "pyttsx3": "Text-to-Speech",
        "speech_recognition": "Voice Recognition",
        "pyaudio": "Audio Input",
        "requests": "Web Requests",
        "cv2": "Face Detection",
        "pygetwindow": "Window Management",
        "pyautogui": "System Automation",
        "psutil": "System Monitoring",
    }

    optional = {"cv2", "llama_cpp", "transformers"}
    missing = []

    for module, description in imports.items():
        try:
            __import__(module)
            marker = "OPT" if module in optional else "OK "
            print(f"   {marker} {module:20} - {description}")
        except ImportError:
            marker = "OPT" if module in optional else "ERR"
            print(f"   {marker} {module:20} - {description}")
            if module not in optional:
                missing.append(module)

    return not missing


def check_jarvis_core():
    """Check whether the Jarvis package imports."""
    print("\nChecking Jarvis package...")

    try:
        from jarvis import Jarvis, SystemControl, WindowManager

        print("   OK  jarvis package imports successful")
        print(f"   OK  {Jarvis.__name__}, {WindowManager.__name__}, {SystemControl.__name__}")
        return True
    except Exception as exc:
        print(f"   ERR jarvis package import failed: {exc}")
        return False


def check_tts_engine():
    """Check whether the configured text-to-speech engine can initialize."""
    print("\nChecking text-to-speech engine...")

    try:
        from jarvis import Jarvis

        jarvis = Jarvis()
        if jarvis.voice_enabled:
            voice = jarvis.tts_voice_name or "system default"
            print(f"   OK  text-to-speech ready: {voice}")
            return True
        print("   WARN text-to-speech engine unavailable")
        print("        Install/repair Windows speech voices or set JARVIS_VOICE_NAME after installing a voice.")
        return True
    except Exception as exc:
        print(f"   WARN text-to-speech check failed: {exc}")
        return True


def main():
    """Run all checks."""
    print("=" * 60)
    print("JARVIS SETUP VERIFICATION")
    print("=" * 60)

    all_good = check_files()

    if not check_imports():
        print("\nMissing required packages.")
        print("Run: python -m pip install -r requirements.txt")
        all_good = False

    if not check_jarvis_core():
        all_good = False

    check_tts_engine()

    print("\n" + "=" * 60)
    if all_good:
        print("SETUP COMPLETE - Ready to launch Jarvis.")
        print("\nRun one of:")
        print("   python run.py")
        print("   python -m jarvis")
        print("=" * 60)
        return 0

    print("Setup incomplete - fix the issues above.")
    print("=" * 60)
    return 1


if __name__ == "__main__":
    sys.exit(main())
