"""Regression tests for command-routing and reminder behavior."""

from datetime import datetime, timedelta

from jarvis.core.assistant import Jarvis


def make_jarvis():
    """Create a lightweight assistant without hardware initialization."""
    jarvis = Jarvis.__new__(Jarvis)
    jarvis.data = {"events": [], "reminders": []}
    jarvis.speak = lambda _text: None
    jarvis.save_data = lambda: None
    return jarvis


def test_list_open_windows_is_not_routed_to_app_launcher():
    jarvis = make_jarvis()
    called = []
    jarvis.list_open_windows = lambda _text: called.append("windows")
    jarvis.open_app = lambda _text: called.append("open")

    jarvis.handle_command("list open windows")

    assert called == ["windows"]


def test_reminder_keeps_task_when_schedule_is_answered_later():
    jarvis = make_jarvis()
    jarvis.listen = lambda: "in 10 minutes"

    jarvis.reminder_command("remind me to stretch")

    reminder = jarvis.data["reminders"][0]
    assert reminder["text"] == "stretch"
    assert datetime.fromisoformat(reminder["time"]) > datetime.now() + timedelta(minutes=9)
