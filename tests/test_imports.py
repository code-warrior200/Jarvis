"""Smoke tests for public package imports."""

from jarvis import Jarvis, LocalLLM, SystemControl, WindowManager
from jarvis.ui import FuturisticGUI, JarvisGUI, run_gui


def test_public_imports():
    assert Jarvis is not None
    assert LocalLLM is not None
    assert SystemControl is not None
    assert WindowManager is not None


def test_gui_alias():
    assert JarvisGUI is FuturisticGUI
    assert callable(run_gui)
