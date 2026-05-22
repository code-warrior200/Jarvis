#!/usr/bin/env python3
"""Simple interactive Jarvis GUI."""

from __future__ import annotations

import platform
import socket
import sys
import threading
from datetime import datetime
from tkinter import messagebox, scrolledtext
import tkinter as tk

from jarvis.core import Jarvis

try:
    import psutil  # type: ignore
except ImportError:  # pragma: no cover - optional runtime dependency
    psutil = None


class FuturisticGUI:
    """Conversation-first assistant UI with clear voice controls."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Jarvis Assistant")
        self.root.geometry("1180x760")
        self.root.minsize(960, 640)

        self.colors = {
            "app": "#0b1117",
            "surface": "#111a22",
            "surface_alt": "#16232d",
            "border": "#243746",
            "text": "#edf7fa",
            "muted": "#8da3ad",
            "cyan": "#31d7e8",
            "green": "#42d984",
            "amber": "#ffb454",
            "red": "#ff5d73",
            "input": "#071017",
        }

        self.jarvis: Jarvis | None = None
        self.listening = False
        self.executing = False
        self.keep_listening = tk.BooleanVar(value=False)

        self.root.configure(bg=self.colors["app"])
        self.build_ui()
        self.set_state("Starting Jarvis...", "Initializing assistant modules.", "amber")
        self.add_message("Jarvis", "Starting up. You can type a command while voice loads.", "assistant")

        threading.Thread(target=self.init_jarvis, daemon=True).start()
        self.refresh_status()

    def init_jarvis(self):
        """Initialize the assistant engine without blocking the window."""
        try:
            self.jarvis = Jarvis(gui_callback=self.display_message)
            voice_text = "Voice input is ready." if self.jarvis.microphone_available else (
                "Text mode is ready. Connect a microphone to use voice."
            )
            self.add_message("Jarvis", voice_text, "assistant")
            self.root.after(0, lambda: self.set_state("Ready", "Ask me by voice or text.", "green"))
            self.root.after(0, self.update_voice_availability)
        except Exception as exc:
            self.add_message("System", f"Jarvis could not start: {exc}", "error")
            self.root.after(0, lambda: self.set_state("Startup failed", "Check dependencies and logs.", "red"))

    def build_ui(self):
        """Build a simpler assistant layout."""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.build_header()

        content = tk.Frame(self.root, bg=self.colors["app"])
        content.grid(row=1, column=0, sticky="nsew", padx=18, pady=(0, 18))
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, minsize=300)
        content.grid_rowconfigure(0, weight=1)

        self.build_conversation(content)
        self.build_side_panel(content)
        self.build_input_bar()

    def build_header(self):
        header = tk.Frame(self.root, bg=self.colors["app"])
        header.grid(row=0, column=0, sticky="ew", padx=18, pady=18)
        header.grid_columnconfigure(1, weight=1)

        orb = tk.Canvas(
            header,
            width=56,
            height=56,
            bg=self.colors["app"],
            highlightthickness=0,
        )
        orb.grid(row=0, column=0, sticky="w")
        self.voice_ring = orb.create_oval(7, 7, 49, 49, outline=self.colors["cyan"], width=3)
        self.voice_core = orb.create_oval(20, 20, 36, 36, fill=self.colors["amber"], width=0)
        self.orb = orb

        title = tk.Frame(header, bg=self.colors["app"])
        title.grid(row=0, column=1, sticky="ew", padx=14)

        tk.Label(
            title,
            text="Jarvis",
            font=("Segoe UI", 24, "bold"),
            fg=self.colors["text"],
            bg=self.colors["app"],
        ).pack(anchor="w")
        tk.Label(
            title,
            text="Voice assistant for apps, windows, search, reminders, weather, and system tasks",
            font=("Segoe UI", 10),
            fg=self.colors["muted"],
            bg=self.colors["app"],
        ).pack(anchor="w")

        status_box = tk.Frame(
            header,
            bg=self.colors["surface"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        status_box.grid(row=0, column=2, sticky="e")
        status_box.grid_columnconfigure(0, weight=1)

        self.state_label = tk.Label(
            status_box,
            text="Starting",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors["amber"],
            bg=self.colors["surface"],
            width=18,
        )
        self.state_label.grid(row=0, column=0, sticky="ew", padx=14, pady=(8, 0))

        self.state_detail = tk.Label(
            status_box,
            text="Loading...",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
            width=32,
        )
        self.state_detail.grid(row=1, column=0, sticky="ew", padx=14, pady=(0, 8))

    def build_conversation(self, parent: tk.Frame):
        conversation = tk.Frame(
            parent,
            bg=self.colors["surface"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        conversation.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        conversation.grid_columnconfigure(0, weight=1)
        conversation.grid_rowconfigure(1, weight=1)

        tk.Label(
            conversation,
            text="Conversation",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors["text"],
            bg=self.colors["surface"],
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        self.display = scrolledtext.ScrolledText(
            conversation,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["cyan"],
            selectbackground=self.colors["border"],
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 11),
            wrap=tk.WORD,
            padx=14,
            pady=12,
        )
        self.display.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.display.tag_config("assistant", foreground=self.colors["green"])
        self.display.tag_config("user", foreground=self.colors["cyan"])
        self.display.tag_config("system", foreground=self.colors["muted"])
        self.display.tag_config("error", foreground=self.colors["red"])
        self.display.tag_config("label", foreground=self.colors["amber"], font=("Segoe UI", 10, "bold"))
        self.display.config(state=tk.DISABLED)

    def build_side_panel(self, parent: tk.Frame):
        side = tk.Frame(
            parent,
            bg=self.colors["surface"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        side.grid(row=0, column=1, sticky="nsew")
        side.grid_columnconfigure(0, weight=1)

        tk.Label(
            side,
            text="Try saying",
            font=("Segoe UI", 13, "bold"),
            fg=self.colors["text"],
            bg=self.colors["surface"],
            anchor="w",
        ).grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        suggestions = [
            ("System info", "system info"),
            ("Open Notepad", "open notepad"),
            ("List windows", "list windows"),
            ("Weather", "weather in Lagos"),
            ("Search web", "search for Python documentation"),
            ("Reminder", "remind me to stretch in 10 minutes"),
            ("Help", "help"),
        ]
        for row, (label, command) in enumerate(suggestions, start=1):
            button = tk.Button(
                side,
                text=label,
                command=lambda value=command: self.use_suggestion(value),
                bg=self.colors["surface_alt"],
                fg=self.colors["text"],
                activebackground=self.colors["cyan"],
                activeforeground=self.colors["app"],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 10),
                anchor="w",
                padx=12,
                pady=10,
            )
            button.grid(row=row, column=0, sticky="ew", padx=16, pady=4)

        tk.Frame(side, height=1, bg=self.colors["border"]).grid(
            row=8,
            column=0,
            sticky="ew",
            padx=16,
            pady=16,
        )

        self.voice_status = tk.Label(
            side,
            text="Voice: checking...",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors["amber"],
            bg=self.colors["surface"],
            anchor="w",
        )
        self.voice_status.grid(row=9, column=0, sticky="ew", padx=16, pady=(0, 8))

        self.system_status = tk.Label(
            side,
            text="System: --",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
            justify=tk.LEFT,
            anchor="nw",
        )
        self.system_status.grid(row=10, column=0, sticky="ew", padx=16, pady=(0, 12))

        follow = tk.Checkbutton(
            side,
            text="Keep listening after each voice command",
            variable=self.keep_listening,
            bg=self.colors["surface"],
            fg=self.colors["text"],
            activebackground=self.colors["surface"],
            activeforeground=self.colors["text"],
            selectcolor=self.colors["input"],
            font=("Segoe UI", 9),
            anchor="w",
        )
        follow.grid(row=11, column=0, sticky="ew", padx=12, pady=(0, 8))

        tk.Label(
            side,
            text="Tip: use the buttons above to fill the command box, then edit or send.",
            font=("Segoe UI", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
            wraplength=250,
            justify=tk.LEFT,
            anchor="nw",
        ).grid(row=12, column=0, sticky="ew", padx=16, pady=(4, 16))

    def build_input_bar(self):
        bar = tk.Frame(
            self.root,
            bg=self.colors["surface"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        bar.grid(row=2, column=0, sticky="ew", padx=18, pady=(0, 18))
        bar.grid_columnconfigure(1, weight=1)

        self.listen_btn = tk.Button(
            bar,
            text="Speak",
            command=self.listen_cmd,
            bg=self.colors["cyan"],
            fg=self.colors["app"],
            activebackground=self.colors["green"],
            activeforeground=self.colors["app"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=12,
        )
        self.listen_btn.grid(row=0, column=0, sticky="w", padx=(12, 8), pady=12)

        self.input_cmd = tk.Entry(
            bar,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["cyan"],
            relief=tk.FLAT,
            font=("Segoe UI", 12),
        )
        self.input_cmd.grid(row=0, column=1, sticky="ew", padx=8, pady=12, ipady=11)
        self.input_cmd.bind("<Return>", lambda _event: self.send_command())
        self.input_cmd.insert(0, "Type a command...")
        self.input_cmd.bind("<FocusIn>", self.clear_placeholder)
        self.input_cmd.bind("<FocusOut>", self.restore_placeholder)

        self.send_btn = tk.Button(
            bar,
            text="Send",
            command=self.send_command,
            bg=self.colors["green"],
            fg=self.colors["app"],
            activebackground=self.colors["cyan"],
            activeforeground=self.colors["app"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 11, "bold"),
            padx=18,
            pady=12,
        )
        self.send_btn.grid(row=0, column=2, sticky="e", padx=8, pady=12)

        tk.Button(
            bar,
            text="Clear",
            command=self.clear_display,
            bg=self.colors["surface_alt"],
            fg=self.colors["text"],
            activebackground=self.colors["border"],
            activeforeground=self.colors["text"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Segoe UI", 10),
            padx=14,
            pady=12,
        ).grid(row=0, column=3, sticky="e", padx=(8, 12), pady=12)

    def display_message(self, label, text, tag="assistant"):
        """Callback used by the assistant core."""
        label_text = "Jarvis" if str(label).lower() == "jarvis" else str(label or "System")
        message_tag = "assistant" if label_text == "Jarvis" else tag
        self.add_message(label_text, text, message_tag)

    def add_message(self, speaker: str, text: str, tag: str = "system"):
        """Thread-safe conversation append."""
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self.add_message(speaker, text, tag))
            return

        timestamp = datetime.now().strftime("%H:%M")
        self.display.config(state=tk.NORMAL)
        self.display.insert(tk.END, f"{speaker}  {timestamp}\n", "label")
        self.display.insert(tk.END, f"{text}\n\n", tag)
        self.display.see(tk.END)
        self.display.config(state=tk.DISABLED)

    def use_suggestion(self, command: str):
        self.input_cmd.delete(0, tk.END)
        self.input_cmd.insert(0, command)
        self.input_cmd.focus_set()

    def clear_placeholder(self, _event=None):
        if self.input_cmd.get() == "Type a command...":
            self.input_cmd.delete(0, tk.END)

    def restore_placeholder(self, _event=None):
        if not self.input_cmd.get().strip():
            self.input_cmd.insert(0, "Type a command...")

    def current_command(self):
        command = self.input_cmd.get().strip()
        if command == "Type a command...":
            return ""
        return command

    def listen_cmd(self):
        """Start a voice capture."""
        if not self.jarvis:
            self.add_message("System", "Jarvis is still starting. Try again in a moment.", "error")
            return
        if not self.jarvis.microphone_available:
            self.add_message("System", "No microphone is available. You can still type commands.", "error")
            return
        if self.listening:
            self.add_message("System", "I am already listening.", "system")
            return

        self.listening = True
        self.set_state("Listening", "Speak now. I will process your command when you stop.", "amber")
        self.listen_btn.config(text="Listening...", bg=self.colors["amber"])
        self.add_message("Jarvis", "I am listening.", "assistant")
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        try:
            assert self.jarvis is not None
            command = self.jarvis.listen()
            if command:
                self.add_message("You", command, "user")
                self.handle_command(command, source="voice")
            else:
                self.add_message("Jarvis", "I did not catch that. Try speaking closer or type it.", "assistant")
        except SystemExit:
            self.add_message("System", "Voice recognition is not available in this environment.", "error")
        except Exception as exc:
            self.add_message("System", f"Voice input failed: {exc}", "error")
        finally:
            self.listening = False
            self.root.after(0, self.reset_voice_controls)

    def send_command(self):
        """Execute typed command."""
        command = self.current_command()
        if not command:
            self.input_cmd.focus_set()
            return
        if not self.jarvis:
            self.add_message("System", "Jarvis is still starting. Try again in a moment.", "error")
            return

        self.input_cmd.delete(0, tk.END)
        self.add_message("You", command, "user")
        self.handle_command(command, source="text")

    def handle_command(self, command: str, source: str):
        if self.executing:
            self.add_message("System", "I am still working on the previous command.", "system")
            return

        self.executing = True
        self.set_state("Working", "Running your command...", "amber")
        self.send_btn.config(state=tk.DISABLED)
        threading.Thread(target=lambda: self._execute_command(command, source), daemon=True).start()

    def _execute_command(self, command: str, source: str):
        try:
            assert self.jarvis is not None
            self.jarvis.handle_command(command)
            self.add_message("Jarvis", "Anything else?", "assistant")
        except SystemExit:
            self.root.after(0, self.quit_app)
        except Exception as exc:
            self.add_message("System", f"Command failed: {exc}", "error")
        finally:
            self.executing = False
            self.root.after(0, self.reset_after_command)
            if source == "voice" and self.keep_listening.get():
                self.root.after(900, self.listen_cmd)

    def reset_after_command(self):
        self.send_btn.config(state=tk.NORMAL)
        if not self.listening:
            self.set_state("Ready", "Ask me by voice or text.", "green")
        self.restore_placeholder()

    def reset_voice_controls(self):
        self.listen_btn.config(text="Speak", bg=self.colors["cyan"])
        if not self.executing:
            self.set_state("Ready", "Ask me by voice or text.", "green")

    def update_voice_availability(self):
        if not self.jarvis:
            return
        if self.jarvis.microphone_available:
            tts = self.jarvis.tts_voice_name or "system default"
            self.voice_status.config(text=f"Voice: ready\nTTS: {tts}", fg=self.colors["green"])
            self.listen_btn.config(state=tk.NORMAL)
        else:
            tts = self.jarvis.tts_voice_name or "unavailable"
            self.voice_status.config(text=f"Voice: unavailable\nTTS: {tts}", fg=self.colors["red"])
            self.listen_btn.config(state=tk.DISABLED, bg=self.colors["surface_alt"], fg=self.colors["muted"])

    def refresh_status(self):
        """Refresh compact machine status."""
        host = socket.gethostname()
        os_name = f"{platform.system()} {platform.release()}"
        if psutil:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            status = f"{host}\n{os_name}\nCPU {cpu:.0f}%  Memory {mem:.0f}%"
        else:
            status = f"{host}\n{os_name}"
        self.system_status.config(text=status)

        pulse_color = self.colors["amber"] if self.listening else self.colors["cyan"]
        core_color = self.colors["amber"] if self.executing else self.colors["green"]
        self.orb.itemconfig(self.voice_ring, outline=pulse_color)
        self.orb.itemconfig(self.voice_core, fill=core_color)

        self.root.after(1200, self.refresh_status)

    def set_state(self, state: str, detail: str, color_key: str):
        color = self.colors[color_key]
        self.state_label.config(text=state, fg=color)
        self.state_detail.config(text=detail)

    def clear_display(self):
        self.display.config(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.config(state=tk.DISABLED)
        self.add_message("Jarvis", "Conversation cleared. What should we do next?", "assistant")

    def show_help(self):
        help_text = (
            "Useful commands:\n\n"
            "open notepad\n"
            "list windows\n"
            "focus chrome\n"
            "system info\n"
            "set volume to 50\n"
            "weather in Lagos\n"
            "search for Python documentation\n"
            "remind me to stretch in 10 minutes\n"
            "tell me a joke"
        )
        messagebox.showinfo("Jarvis Help", help_text)

    def quit_app(self):
        if messagebox.askokcancel("Shutdown", "Shut down Jarvis?"):
            self.root.destroy()
            sys.exit(0)


def run_gui():
    """Launch the GUI."""
    root = tk.Tk()
    app = FuturisticGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()


JarvisGUI = FuturisticGUI


if __name__ == "__main__":
    run_gui()
