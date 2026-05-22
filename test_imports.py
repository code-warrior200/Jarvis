#!/usr/bin/env python3
"""Test that all imports and classes are properly defined."""

import sys
import os

# Add the Jarvis directory to path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from jarvis import Jarvis, WindowManager, SystemControl, LocalLLM
    print("✓ All classes imported successfully")
    print("✓ Jarvis:", Jarvis)
    print("✓ WindowManager:", WindowManager)
    print("✓ SystemControl:", SystemControl)
    print("✓ LocalLLM:", LocalLLM)
    print("\nSetup successful! Jarvis enhancements are ready.")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
