#!/usr/bin/env python3
"""Voice-only eDEX-inspired Jarvis GUI."""

from __future__ import annotations

import platform
import socket
import sys
import threading
import ctypes
import math
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, scrolledtext
import tkinter as tk
from typing import Optional

from jarvis.core import Jarvis

try:
    import psutil  # type: ignore
except ImportError:  # pragma: no cover - optional runtime dependency
    psutil = None


def acquire_instance_mutex():
    """Allow only one Windows Jarvis process to own the speech engine."""
    if sys.platform != "win32":
        return None

    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Local\\JarvisNeuralCommandCore")
    if not mutex or ctypes.get_last_error() == 183:  # ERROR_ALREADY_EXISTS
        if mutex:
            ctypes.windll.kernel32.CloseHandle(mutex)
        return None
    return mutex


class FuturisticGUI:
    """Voice-first assistant UI styled after eDEX-UI."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("JARVIS // NEURAL COMMAND CORE")
        self.root.geometry("720x720")
        self.root.minsize(720, 720)
        self.root.maxsize(720, 720)

        self.colors = {
            "app": "#01050b",
            "surface": "#06131d",
            "surface_alt": "#092331",
            "input": "#00090f",
            "border": "#0d6f87",
            "border_dim": "#123b4a",
            "text": "#e0fbff",
            "muted": "#6f9fac",
            "cyan": "#22f5f2",
            "cyan_dim": "#179eae",
            "green": "#55ff9a",
            "amber": "#ffc247",
            "red": "#ff5274",
            "purple": "#ae8cff",
            "black": "#00060a",
        }

        self.jarvis: Jarvis | None = None
        self.listening = False
        self.executing = False
        self.command_source = "voice"
        self.command_history: list[str] = []
        self.history_index: int | None = None
        self.keep_listening = tk.BooleanVar(value=False)
        self.voice_chat_active = False
        self.listen_after_id = None
        self.stat_labels: dict[str, tk.Label] = {}
        self.pulse = False
        self.animation_phase = 0

        self.root.configure(bg=self.colors["app"])
        self.build_ui()
        self.set_state("BOOTING", "VOICE KERNEL INITIALIZING", "amber")

        threading.Thread(target=self.init_jarvis, daemon=True).start()
        self.refresh_status()
        self.animate()
        self.animate_background()

    def init_jarvis(self):
        """Initialize the assistant engine without blocking the window."""
        try:
            self.jarvis = Jarvis(gui_callback=self.display_message)
            self.respond("Voice command terminal online. Initializing modules.")
            if self.jarvis.llm.backend == "ollama":
                self.respond(f"Ollama connected. Local model {self.jarvis.llm.ollama_model} is ready.")
            if self.jarvis.microphone_available:
                self.respond("Microphone channel ready. Say a command after pressing SPEAK.")
                self.root.after(0, lambda: self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green"))
            else:
                self.add_message("SYSTEM", "No microphone detected. Text commands remain available.", "error")
                self.root.after(0, lambda: self.set_state("TEXT READY", "MICROPHONE UNAVAILABLE", "amber"))
            self.root.after(0, self.update_voice_availability)
            self.respond("All modules are initialized. Jarvis is ready.")
        except Exception as exc:
            self.add_message("SYSTEM", f"Jarvis could not start: {exc}", "error")
            self.root.after(0, lambda: self.set_state("FAULT", "STARTUP FAILED", "red"))

    def build_ui(self):
        """Build a single-surface interface based on the supplied Jarvis artwork."""
        self.surface = tk.Canvas(self.root, bg=self.colors["black"], highlightthickness=0)
        self.surface.pack(fill=tk.BOTH, expand=True)
        asset_path = Path(__file__).resolve().parents[1] / "assets" / "jarvis-surface.png"
        self.surface_image = tk.PhotoImage(file=str(asset_path))
        self.surface.create_image(0, 0, image=self.surface_image, anchor="nw")
        self.build_background_animation()
        self.surface.configure(cursor="hand2")
        self.surface.bind("<Button-1>", self.handle_surface_click)

        self.clock_label = tk.Label(
            self.root, text="--:--:-- WAT", font=("Consolas", 8, "bold"),
            fg=self.colors["cyan"], bg=self.colors["black"],
        )
        self.state_label = tk.Label(
            self.root, text="BOOTING", font=("Consolas", 8, "bold"),
            fg=self.colors["amber"], bg=self.colors["black"],
        )
        self.state_detail = tk.Label(
            self.root, text="INITIALIZING", font=("Consolas", 7),
            fg=self.colors["muted"], bg=self.colors["black"],
        )
        self.surface.create_window(12, 12, window=self.clock_label, anchor="nw")
        self.surface.create_window(708, 12, window=self.state_label, anchor="ne")
        self.surface.create_window(708, 30, window=self.state_detail, anchor="ne")

        self.response_label = tk.Label(
            self.root, text="", font=("Consolas", 9), fg=self.colors["text"],
            bg=self.colors["black"], justify=tk.LEFT, anchor="w", wraplength=650,
        )
        self.surface.create_window(360, 577, window=self.response_label, width=650, anchor="center")

        self.quick_actions = (
            ("SYSTEM", "system info"),
            ("WINDOWS", "list windows"),
            ("WEATHER", "weather in Lagos"),
            ("TEST VOICE", None),
        )
        for index, (label, command) in enumerate(self.quick_actions):
            action = tk.Button(
                self.root,
                text=label,
                command=lambda value=command: self.test_voice() if value is None else self.run_quick_command(value),
                bg=self.colors["black"],
                fg=self.colors["cyan"],
                activebackground=self.colors["cyan_dim"],
                activeforeground=self.colors["black"],
                relief=tk.FLAT,
                highlightthickness=1,
                highlightbackground=self.colors["border_dim"],
                cursor="hand2",
                font=("Consolas", 8, "bold"),
                padx=8,
                pady=3,
            )
            self.surface.create_window(140 + index * 140, 615, window=action, anchor="center")

        self.chat_btn = tk.Button(
            self.root, text="START CHAT", command=self.toggle_voice_chat,
            bg=self.colors["purple"], fg=self.colors["black"], relief=tk.FLAT,
            activebackground=self.colors["amber"], activeforeground=self.colors["black"],
            cursor="hand2", font=("Consolas", 8, "bold"), padx=8, pady=3,
        )
        self.surface.create_window(650, 615, window=self.chat_btn, anchor="center")

        self.text_command = tk.Entry(
            self.root, bg=self.colors["black"], fg=self.colors["cyan"],
            insertbackground=self.colors["cyan"], relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.colors["cyan_dim"],
            font=("Consolas", 10),
        )
        self.text_command.bind("<Return>", self.submit_text_command)
        self.text_command.bind("<Up>", self.show_previous_command)
        self.text_command.bind("<Down>", self.show_next_command)
        self.send_btn = tk.Button(
            self.root, text="SEND", command=self.submit_text_command,
            bg=self.colors["cyan"], fg=self.colors["black"], relief=tk.FLAT,
            font=("Consolas", 9, "bold"), padx=14,
        )
        self.listen_btn = tk.Button(
            self.root, text="VOICE", command=self.listen_cmd,
            bg=self.colors["black"], fg=self.colors["cyan"], relief=tk.FLAT,
            highlightthickness=1, highlightbackground=self.colors["cyan_dim"],
            font=("Consolas", 9, "bold"), padx=14,
        )
        self.surface.create_window(315, 666, window=self.text_command, width=430, height=32, anchor="center")
        self.surface.create_window(564, 666, window=self.send_btn, anchor="center")
        self.surface.create_window(644, 666, window=self.listen_btn, anchor="center")

        self.root.bind_all("<Control-k>", self.focus_command)
        self.root.bind_all("<Control-l>", self.start_voice_shortcut)
        self.root.bind_all("<F1>", lambda _event: self.show_help())

        self.voice_status = self.state_detail
        self.stat_labels = {}

    def build_background_animation(self):
        """Add subtle motion to the background without obscuring controls."""
        self.background_center = (360, 355)
        self.scanner_line = self.surface.create_line(
            360, 355, 360, 125, fill=self.colors["cyan"], width=2,
        )
        self.scanner_echo = self.surface.create_line(
            360, 355, 360, 150, fill=self.colors["cyan_dim"], width=8,
        )
        self.pulse_rings = [
            self.surface.create_oval(360, 355, 360, 355, outline=self.colors["cyan_dim"], width=1)
            for _ in range(3)
        ]
        self.signal_particles = []
        for index in range(18):
            angle = index * (math.tau / 18)
            radius = 150 + (index % 4) * 30
            x = 360 + math.cos(angle) * radius
            y = 355 + math.sin(angle) * radius
            particle = self.surface.create_oval(x - 2, y - 2, x + 2, y + 2, fill=self.colors["cyan"], outline="")
            self.signal_particles.append((particle, angle, radius))

    def handle_surface_click(self, event):
        """Let the central core act as a large, easy-to-find voice control."""
        distance_squared = (event.x - 360) ** 2 + (event.y - 355) ** 2
        if distance_squared <= 165 ** 2:
            self.listen_cmd()

    def toggle_voice_chat(self):
        """Start or stop a continuous, hands-free voice conversation."""
        if self.voice_chat_active:
            self.stop_voice_chat()
            return
        if not self.jarvis or not self.jarvis.microphone_available:
            self.add_message("SYSTEM", "A working microphone is required to start voice chat.", "error")
            return
        self.voice_chat_active = True
        self.keep_listening.set(True)
        self.chat_btn.config(text="END CHAT", bg=self.colors["amber"])
        self.respond("Voice chat started. How can I help?")
        self.root.after(250, self.listen_cmd)

    def stop_voice_chat(self):
        self.voice_chat_active = False
        self.keep_listening.set(False)
        if self.listen_after_id:
            self.root.after_cancel(self.listen_after_id)
            self.listen_after_id = None
        self.chat_btn.config(text="START CHAT", bg=self.colors["purple"])
        self.respond("Voice chat ended.")

    def run_quick_command(self, command: str):
        """Send a common command in one click, while keeping it visible to the user."""
        if self.executing:
            self.add_message("SYSTEM", "Previous command is still executing.", "system")
            return
        self.text_command.delete(0, tk.END)
        self.text_command.insert(0, command)
        self.submit_text_command()

    def test_voice(self):
        """Play a short confirmation through the configured speaker output."""
        if not self.jarvis:
            self.add_message("SYSTEM", "Jarvis is still starting. Try the voice test again in a moment.", "error")
            return
        if not self.jarvis.voice_enabled:
            self.add_message("SYSTEM", "Speech output is unavailable. Install pyttsx3 and restart Jarvis.", "error")
            return
        if self.executing or self.listening:
            self.add_message("SYSTEM", "Wait for the current command before testing the voice.", "system")
            return

        self.set_state("SPEAKING", "TESTING DEFAULT SPEAKER OUTPUT", "green")
        threading.Thread(target=self._test_voice_thread, daemon=True).start()

    def _test_voice_thread(self):
        assert self.jarvis is not None
        self.jarvis.speak("Hello. Jarvis voice output is online and ready.")
        self.root.after(0, lambda: self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green"))

    def focus_command(self, _event=None):
        if str(self.text_command.cget("state")) == tk.NORMAL:
            self.text_command.focus_set()
            self.text_command.selection_range(0, tk.END)
        return "break"

    def start_voice_shortcut(self, _event=None):
        self.listen_cmd()
        return "break"

    def show_previous_command(self, _event=None):
        if not self.command_history:
            return "break"
        if self.history_index is None:
            self.history_index = len(self.command_history) - 1
        else:
            self.history_index = max(0, self.history_index - 1)
        self.replace_command_text(self.command_history[self.history_index])
        return "break"

    def show_next_command(self, _event=None):
        if self.history_index is None:
            return "break"
        self.history_index += 1
        if self.history_index >= len(self.command_history):
            self.history_index = None
            self.replace_command_text("")
        else:
            self.replace_command_text(self.command_history[self.history_index])
        return "break"

    def replace_command_text(self, command: str):
        self.text_command.delete(0, tk.END)
        self.text_command.insert(0, command)

    def build_header(self):
        header = tk.Frame(self.root, bg=self.colors["app"], height=96)
        header.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 10))
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)

        self.orb = tk.Canvas(
            header,
            width=76,
            height=76,
            bg=self.colors["app"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        self.orb.grid(row=0, column=0, sticky="w")
        self.orb.create_oval(3, 3, 73, 73, outline=self.colors["border_dim"], width=1)
        self.orb.create_oval(11, 11, 65, 65, outline=self.colors["cyan_dim"], width=1)
        self.voice_ring = self.orb.create_oval(18, 18, 58, 58, outline=self.colors["cyan"], width=2)
        self.voice_core = self.orb.create_oval(31, 31, 45, 45, fill=self.colors["amber"], width=0)
        self.orb.create_line(38, 4, 38, 72, fill=self.colors["border_dim"])
        self.orb.create_line(4, 38, 72, 38, fill=self.colors["border_dim"])
        self.orb.create_text(38, 7, text="A1", fill=self.colors["muted"], font=("Consolas", 7, "bold"))

        title = tk.Frame(header, bg=self.colors["app"])
        title.grid(row=0, column=1, sticky="ew", padx=16)

        tk.Label(
            title,
            text="JARVIS // AURORA",
            font=("Consolas", 27, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["app"],
        ).pack(anchor="w")
        tk.Label(
            title,
            text="NEURAL COMMAND CORE  •  VOICE + TEXT LOCAL ASSISTANT  •  NODE 01",
            font=("Consolas", 10, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["app"],
        ).pack(anchor="w")

        status = self.panel(header, width=330)
        status.grid(row=0, column=2, sticky="e")
        status.grid_columnconfigure(0, weight=1)

        self.clock_label = tk.Label(
            status,
            text="--:--:--  WAT",
            font=("Consolas", 20, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["surface"],
        )
        self.clock_label.grid(row=0, column=0, sticky="ew", padx=12, pady=(9, 0))

        self.state_label = tk.Label(
            status,
            text="BOOT",
            font=("Consolas", 11, "bold"),
            fg=self.colors["amber"],
            bg=self.colors["surface"],
        )
        self.state_label.grid(row=1, column=0, sticky="ew", padx=12)

        self.state_detail = tk.Label(
            status,
            text="INITIALIZING",
            font=("Consolas", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
        )
        self.state_detail.grid(row=2, column=0, sticky="ew", padx=12, pady=(0, 9))

        tk.Label(
            status,
            text="UPLINK: LOCAL  //  ENCRYPTION: ACTIVE",
            font=("Consolas", 7, "bold"),
            fg=self.colors["cyan_dim"],
            bg=self.colors["surface"],
        ).grid(row=3, column=0, sticky="ew", padx=12, pady=(0, 8))

    def build_command_examples(self, parent: tk.Frame):
        rail = self.panel(parent)
        rail.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        rail.grid_columnconfigure(0, weight=1)

        self.section_title(rail, "COMMAND MATRIX").grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))

        examples = [
            ("SYSTEM", "system info"),
            ("APPS", "open notepad"),
            ("WINDOWS", "list windows"),
            ("FOCUS", "focus chrome"),
            ("WEATHER", "weather in Lagos"),
            ("SEARCH", "search for Python documentation"),
            ("REMINDER", "remind me to stretch in 10 minutes"),
            ("HELP", "help"),
        ]
        for index, (group, phrase) in enumerate(examples, start=1):
            card = tk.Frame(
                rail,
                bg=self.colors["surface_alt"],
                highlightthickness=1,
                highlightbackground=self.colors["border_dim"],
            )
            card.grid(row=index, column=0, sticky="ew", padx=12, pady=4)
            card.grid_columnconfigure(0, weight=1)

            tk.Label(
                card,
                text=group,
                font=("Consolas", 8, "bold"),
                fg=self.colors["amber"],
                bg=self.colors["surface_alt"],
                anchor="w",
            ).grid(row=0, column=0, sticky="ew", padx=10, pady=(7, 0))
            tk.Label(
                card,
                text=f"> {phrase}",
                font=("Consolas", 9),
                fg=self.colors["text"],
                bg=self.colors["surface_alt"],
                anchor="w",
                wraplength=210,
            ).grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 8))

        self.section_title(rail, "MODE").grid(row=10, column=0, sticky="ew", padx=12, pady=(18, 8))
        self.voice_status = tk.Label(
            rail,
            text="VOICE: CHECKING\nTTS: CHECKING\nLINK: LOCAL",
            font=("Consolas", 9, "bold"),
            fg=self.colors["amber"],
            bg=self.colors["surface"],
            justify=tk.LEFT,
            anchor="w",
        )
        self.voice_status.grid(row=11, column=0, sticky="ew", padx=12, pady=(0, 8))

        follow = tk.Checkbutton(
            rail,
            text="CONTINUOUS LISTEN",
            variable=self.keep_listening,
            bg=self.colors["surface"],
            fg=self.colors["text"],
            activebackground=self.colors["surface"],
            activeforeground=self.colors["cyan"],
            selectcolor=self.colors["black"],
            font=("Consolas", 9, "bold"),
            anchor="w",
        )
        follow.grid(row=12, column=0, sticky="ew", padx=8, pady=(0, 8))

    def build_terminal(self, parent: tk.Frame):
        terminal = self.panel(parent)
        terminal.grid(row=0, column=1, sticky="nsew")
        terminal.grid_columnconfigure(0, weight=1)
        terminal.grid_rowconfigure(1, weight=1)
        terminal.grid_rowconfigure(2, weight=1)

        head = tk.Frame(terminal, bg=self.colors["surface"])
        head.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        head.grid_columnconfigure(1, weight=1)

        tk.Label(
            head,
            text="[ JARVIS HOLOGRAPHIC CORE ]",
            font=("Consolas", 11, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["surface"],
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            head,
            text="ARC REACTOR ONLINE // NODE 01",
            font=("Consolas", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
        ).grid(row=0, column=1, sticky="e")

        self.reactor_canvas = tk.Canvas(
            terminal,
            bg=self.colors["black"],
            highlightthickness=1,
            highlightbackground=self.colors["border_dim"],
        )
        self.reactor_canvas.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 8))
        self.reactor_image = None
        asset_path = Path(__file__).resolve().parents[1] / "assets" / "jarvis-core.png"
        try:
            self.reactor_image = tk.PhotoImage(file=str(asset_path))
        except tk.TclError:
            self.reactor_canvas.create_text(
                260,
                180,
                text="JARVIS\nHOLOGRAPHIC CORE",
                fill=self.colors["cyan"],
                font=("Consolas", 24, "bold"),
                justify=tk.CENTER,
            )
        self.reactor_canvas.bind("<Configure>", self.draw_reactor_core)

        self.display = scrolledtext.ScrolledText(
            terminal,
            bg=self.colors["black"],
            fg=self.colors["text"],
            insertbackground=self.colors["cyan"],
            selectbackground=self.colors["border"],
            relief=tk.FLAT,
            bd=0,
            font=("Consolas", 10),
            wrap=tk.WORD,
            padx=12,
            pady=12,
        )
        self.display.grid(row=2, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.display.tag_config("assistant", foreground=self.colors["green"])
        self.display.tag_config("user", foreground=self.colors["cyan"])
        self.display.tag_config("system", foreground=self.colors["muted"])
        self.display.tag_config("error", foreground=self.colors["red"], font=("Consolas", 10, "bold"))
        self.display.tag_config("label", foreground=self.colors["amber"], font=("Consolas", 9, "bold"))
        self.display.config(state=tk.DISABLED)

    def draw_reactor_core(self, event=None):
        """Center the supplied holographic-core artwork within the command view."""
        canvas = self.reactor_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 1)
        height = max(canvas.winfo_height(), 1)
        for x in range(0, width, 32):
            canvas.create_line(x, 0, x, height, fill=self.colors["border_dim"])
        for y in range(0, height, 32):
            canvas.create_line(0, y, width, y, fill=self.colors["border_dim"])

        if self.reactor_image:
            canvas.create_image(width // 2, height // 2, image=self.reactor_image)
        canvas.create_text(
            12,
            12,
            text="SYS//CORE.01",
            fill=self.colors["cyan"],
            font=("Consolas", 8, "bold"),
            anchor="nw",
        )
        canvas.create_text(
            width - 12,
            height - 12,
            text="LINK: STABLE",
            fill=self.colors["green"],
            font=("Consolas", 8, "bold"),
            anchor="se",
        )

    def build_telemetry(self, parent: tk.Frame):
        stack = tk.Frame(parent, bg=self.colors["app"])
        stack.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        stack.grid_columnconfigure(0, weight=1)
        stack.grid_rowconfigure(2, weight=1)

        system = self.panel(stack)
        system.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        self.section_title(system, "SYSTEM").pack(fill=tk.X, padx=12, pady=(12, 8))
        for key in ("HOST", "OS", "CPU", "MEM", "DISK"):
            self.stat_row(system, key)

        audio = self.panel(stack)
        audio.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        self.section_title(audio, "AUDIO").pack(fill=tk.X, padx=12, pady=(12, 8))
        for key in ("MIC", "TTS", "MODE"):
            self.stat_row(audio, key)

        activity = self.panel(stack)
        activity.grid(row=2, column=0, sticky="nsew")
        self.section_title(activity, "NEURAL SIGNAL").pack(fill=tk.X, padx=12, pady=(12, 8))
        self.signal_canvas = tk.Canvas(
            activity,
            height=170,
            bg=self.colors["black"],
            highlightthickness=1,
            highlightbackground=self.colors["border_dim"],
        )
        self.signal_canvas.pack(fill=tk.X, padx=12, pady=(0, 12))
        self.signal_text = tk.Label(
            activity,
            text="SCAN READY  //  Awaiting a voice or text command.",
            font=("Consolas", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
            justify=tk.LEFT,
            anchor="nw",
        )
        self.signal_text.pack(fill=tk.BOTH, expand=True, padx=12, pady=(0, 12))

    def build_voice_deck(self, parent: tk.Frame):
        deck = self.panel(parent)
        deck.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(10, 0))
        deck.grid_columnconfigure(1, weight=1)

        self.listen_btn = tk.Button(
            deck,
            text="INITIATE VOICE",
            command=self.listen_cmd,
            bg=self.colors["cyan"],
            fg=self.colors["black"],
            activebackground=self.colors["green"],
            activeforeground=self.colors["black"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Consolas", 13, "bold"),
            padx=20,
            pady=16,
        )
        self.listen_btn.grid(row=0, column=0, sticky="w", padx=12, pady=12)

        self.deck_label = tk.Label(
            deck,
            text="VOICE COMMAND BUS ARMED  //  PRESS TO OPEN A SECURE AUDIO CHANNEL",
            font=("Consolas", 11, "bold"),
            fg=self.colors["text"],
            bg=self.colors["surface"],
            anchor="w",
        )
        self.deck_label.grid(row=0, column=1, sticky="ew", padx=12, pady=12)

        for column, (label, command) in enumerate((("CLEAR", self.clear_display), ("HELP", self.show_help)), start=2):
            tk.Button(
                deck,
                text=label,
                command=command,
                bg=self.colors["surface_alt"],
                fg=self.colors["cyan"],
                activebackground=self.colors["border"],
                activeforeground=self.colors["text"],
                relief=tk.FLAT,
                bd=0,
                cursor="hand2",
                font=("Consolas", 10, "bold"),
                padx=16,
                pady=16,
                highlightthickness=1,
                highlightbackground=self.colors["border"],
            ).grid(row=0, column=column, sticky="e", padx=(0, 12), pady=12)

        command_row = tk.Frame(deck, bg=self.colors["surface"])
        command_row.grid(row=1, column=0, columnspan=4, sticky="ew", padx=12, pady=(0, 12))
        command_row.grid_columnconfigure(1, weight=1)

        tk.Label(
            command_row,
            text="TEXT >",
            font=("Consolas", 10, "bold"),
            fg=self.colors["green"],
            bg=self.colors["surface"],
        ).grid(row=0, column=0, padx=(0, 10))
        self.text_command = tk.Entry(
            command_row,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["cyan"],
            relief=tk.FLAT,
            font=("Consolas", 11),
        )
        self.text_command.grid(row=0, column=1, sticky="ew", ipady=9)
        self.text_command.bind("<Return>", self.submit_text_command)
        self.send_btn = tk.Button(
            command_row,
            text="TRANSMIT",
            command=self.submit_text_command,
            bg=self.colors["green"],
            fg=self.colors["black"],
            activebackground=self.colors["cyan"],
            activeforeground=self.colors["black"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Consolas", 10, "bold"),
            padx=18,
            pady=9,
        )
        self.send_btn.grid(row=0, column=2, padx=(10, 0))

    def panel(self, parent: tk.Widget, width: Optional[int] = None):
        return tk.Frame(
            parent,
            width=width or 1,
            bg=self.colors["surface"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )

    def section_title(self, parent: tk.Widget, text: str):
        return tk.Label(
            parent,
            text=f"[ {text} ]",
            font=("Consolas", 10, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["surface"],
            anchor="w",
        )

    def stat_row(self, parent: tk.Widget, key: str):
        row = tk.Frame(parent, bg=self.colors["surface"])
        row.pack(fill=tk.X, padx=12, pady=3)
        tk.Label(
            row,
            text=key,
            width=8,
            font=("Consolas", 9, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
            anchor="w",
        ).pack(side=tk.LEFT)
        value = tk.Label(
            row,
            text="--",
            font=("Consolas", 9),
            fg=self.colors["text"],
            bg=self.colors["surface"],
            anchor="e",
        )
        value.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        self.stat_labels[key] = value

    def display_message(self, label, text, tag="assistant"):
        """Callback used by the assistant core."""
        label_text = "JARVIS" if str(label).lower() == "jarvis" else str(label or "SYSTEM").upper()
        message_tag = "assistant" if label_text == "JARVIS" else tag
        self.add_message(label_text, text, message_tag)

    def respond(self, text: str):
        """Deliver a Jarvis response to both the display and speaker output."""
        if not self.jarvis:
            self.add_message("JARVIS", text, "assistant")
            return
        if not self.jarvis.voice_enabled:
            self.add_message("JARVIS", text, "assistant")
            return
        threading.Thread(target=self.jarvis.speak, args=(text,), daemon=True).start()

    def add_message(self, speaker: str, text: str, tag: str = "system"):
        """Thread-safe response text rendered over the holographic surface."""
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self.add_message(speaker, text, tag))
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        color = self.colors["green"] if speaker == "JARVIS" else self.colors["cyan"]
        if tag == "error":
            color = self.colors["red"]
        self.response_label.config(text=f"{timestamp}  {speaker}: {text}", fg=color)

    def listen_cmd(self):
        """Start a voice capture."""
        if not self.jarvis:
            self.add_message("SYSTEM", "Jarvis is still starting. Try again in a moment.", "error")
            return
        if not self.jarvis.microphone_available:
            self.add_message("SYSTEM", "No microphone is available. Connect one to use voice commands.", "error")
            return
        if self.listening:
            self.add_message("SYSTEM", "Voice channel is already open.", "system")
            return

        self.listening = True
        self.set_state("LISTENING", "SPEAK NOW // PROCESSING AFTER PAUSE", "amber")
        self.listen_btn.config(text="LIVE", bg=self.colors["amber"], state=tk.DISABLED)
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def submit_text_command(self, _event=None):
        """Send an entered command without requiring voice input."""
        if not self.jarvis:
            self.add_message("SYSTEM", "Jarvis is still starting. Try again in a moment.", "error")
            return "break"

        command = self.text_command.get().strip()
        if not command:
            self.text_command.focus_set()
            return "break"

        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = None
        self.text_command.delete(0, tk.END)
        self.add_message("YOU", command, "user")
        self.handle_command(command, source="text")
        return "break"

    def _listen_thread(self):
        try:
            assert self.jarvis is not None
            command = self.jarvis.listen()
            if command:
                self.add_message("YOU", command, "user")
                self.root.after(0, lambda: self.handle_command(command, source="voice"))
            else:
                self.respond("No command detected. Press SPEAK and try again.")
        except SystemExit:
            self.add_message("SYSTEM", "Voice recognition is not available in this environment.", "error")
        except Exception as exc:
            self.add_message("SYSTEM", f"Voice input failed: {exc}", "error")
        finally:
            self.root.after(0, self.finish_listening)

    def finish_listening(self):
        """Restore listening state from the Tk event loop."""
        self.listening = False
        self.reset_voice_controls()

    def handle_command(self, command: str, source: str = "voice"):
        if command.lower().strip() in {"stop chat", "end chat", "stop listening"}:
            self.stop_voice_chat()
            return
        if self.executing:
            self.add_message("SYSTEM", "Previous command is still executing.", "system")
            return

        self.executing = True
        self.command_source = source
        channel = "VOICE" if source == "voice" else "TEXT"
        self.set_state("EXECUTING", f"RUNNING {channel} COMMAND", "amber")
        self.listen_btn.config(state=tk.DISABLED)
        self.text_command.config(state=tk.DISABLED)
        self.send_btn.config(state=tk.DISABLED)
        threading.Thread(target=lambda: self._execute_command(command), daemon=True).start()

    def _execute_command(self, command: str):
        try:
            assert self.jarvis is not None
            self.jarvis.handle_command(command)
            self.respond("Standing by for the next command.")
        except SystemExit:
            self.root.after(0, self.quit_app)
        except Exception as exc:
            self.add_message("SYSTEM", f"Command failed: {exc}", "error")
        finally:
            self.root.after(0, self.finish_execution)

    def finish_execution(self):
        """Restore command controls and read Tk variables on the UI thread."""
        self.executing = False
        self.reset_after_command()
        if self.command_source == "voice" and self.voice_chat_active:
            self.listen_after_id = self.root.after(900, self.listen_cmd)

    def reset_after_command(self):
        if self.jarvis and self.jarvis.microphone_available:
            self.listen_btn.config(state=tk.NORMAL)
        if self.jarvis:
            self.text_command.config(state=tk.NORMAL)
            self.send_btn.config(state=tk.NORMAL)
            self.text_command.focus_set()
        if not self.listening:
            self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green")

    def reset_voice_controls(self):
        self.listen_btn.config(text="INITIATE VOICE", bg=self.colors["cyan"])
        if self.jarvis and self.jarvis.microphone_available and not self.executing:
            self.listen_btn.config(state=tk.NORMAL)
        if not self.executing:
            self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green")

    def update_voice_availability(self):
        if not self.jarvis:
            return
        tts = self.jarvis.tts_voice_name or "UNAVAILABLE"
        response_mode = "TEXT + VOICE" if self.jarvis.voice_enabled else "TEXT ONLY"
        if self.jarvis.microphone_available:
            self.voice_status.config(
                text=f"VOICE: READY\nTEXT: READY\nREPLY: {response_mode}\nTTS: {tts}",
                fg=self.colors["green"],
            )
            self.listen_btn.config(state=tk.NORMAL)
            self.set_stat("MIC", "READY")
        else:
            self.voice_status.config(
                text=f"VOICE: UNAVAILABLE\nTEXT: READY\nREPLY: {response_mode}\nTTS: {tts}",
                fg=self.colors["amber"],
            )
            self.listen_btn.config(state=tk.DISABLED, bg=self.colors["surface_alt"], fg=self.colors["muted"])
            self.set_stat("MIC", "MISSING")
        self.set_stat("TTS", tts)
        self.set_stat("MODE", "VOICE + TEXT")
        self.text_command.config(state=tk.NORMAL)
        self.send_btn.config(state=tk.NORMAL)
        self.text_command.focus_set()

    def refresh_status(self):
        """Refresh clock, system status, and activity graph."""
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S  WAT"))
        self.set_stat("HOST", socket.gethostname())
        self.set_stat("OS", f"{platform.system()} {platform.release()}")

        if psutil:
            cpu = psutil.cpu_percent(interval=None)
            mem = psutil.virtual_memory().percent
            disk = psutil.disk_usage("/").percent
            self.set_stat("CPU", f"{cpu:.0f}%")
            self.set_stat("MEM", f"{mem:.0f}%")
            self.set_stat("DISK", f"{disk:.0f}%")
        else:
            cpu = 18
            mem = 36
            self.set_stat("CPU", "--")
            self.set_stat("MEM", "--")
            self.set_stat("DISK", "--")

        self.draw_signal(cpu, mem)
        self.root.after(1200, self.refresh_status)

    def draw_signal(self, cpu: float, mem: float):
        if not hasattr(self, "signal_canvas"):
            return
        canvas = self.signal_canvas
        canvas.delete("all")
        width = max(canvas.winfo_width(), 260)
        height = max(canvas.winfo_height(), 140)
        step = max(width // 28, 8)

        for y in range(28, height - 8, 28):
            canvas.create_line(8, y, width - 8, y, fill=self.colors["border_dim"])
        canvas.create_line(width // 2, 24, width // 2, height - 8, fill=self.colors["border_dim"])

        for index, x in enumerate(range(8, width - 8, step)):
            value = (int(cpu) + int(mem) + index * 9) % 100
            bar = int((value / 100) * (height - 26))
            color = self.colors["amber"] if self.listening else self.colors["purple"] if value > 78 else self.colors["cyan"]
            canvas.create_rectangle(
                x,
                height - bar - 8,
                x + step - 3,
                height - 8,
                outline=color,
                fill=self.colors["surface_alt"],
            )
        canvas.create_text(
            10,
            10,
            text="VOICE / SYSTEM SIGNAL  •  LIVE SPECTRUM",
            fill=self.colors["muted"],
            anchor="nw",
            font=("Consolas", 8, "bold"),
        )

    def set_stat(self, key: str, value: str):
        label = self.stat_labels.get(key)
        if label:
            label.config(text=value)

    def set_state(self, state: str, detail: str, color_key: str):
        color = self.colors[color_key]
        self.state_label.config(text=state, fg=color)
        self.state_detail.config(text=detail)

    def animate(self):
        self.pulse = not self.pulse
        if hasattr(self, "orb"):
            ring = self.colors["cyan"] if self.pulse else self.colors["purple"]
            core = self.colors["amber"] if self.listening else self.colors["purple"] if self.executing else self.colors["green"]
            self.orb.itemconfig(self.voice_ring, outline=ring)
            self.orb.itemconfig(self.voice_core, fill=core)
        self.root.after(700, self.animate)

    def animate_background(self):
        """Update the holographic scanner overlay at a smooth, low-cost frame rate."""
        self.animation_phase = (self.animation_phase + 0.035) % math.tau
        center_x, center_y = self.background_center
        scan_angle = self.animation_phase
        scan_radius = 245
        end_x = center_x + math.cos(scan_angle) * scan_radius
        end_y = center_y + math.sin(scan_angle) * scan_radius
        echo_x = center_x + math.cos(scan_angle - 0.09) * scan_radius
        echo_y = center_y + math.sin(scan_angle - 0.09) * scan_radius
        self.surface.coords(self.scanner_echo, center_x, center_y, echo_x, echo_y)
        self.surface.coords(self.scanner_line, center_x, center_y, end_x, end_y)

        for index, ring in enumerate(self.pulse_rings):
            radius = ((self.animation_phase * 95) + index * 82) % 250
            alpha_color = self.colors["cyan"] if index == 0 else self.colors["cyan_dim"]
            self.surface.coords(ring, center_x - radius, center_y - radius, center_x + radius, center_y + radius)
            self.surface.itemconfig(ring, outline=alpha_color)

        for index, (particle, base_angle, radius) in enumerate(self.signal_particles):
            angle = base_angle + self.animation_phase * (0.55 + (index % 3) * 0.12)
            orbit = radius + math.sin(self.animation_phase * 2 + index) * 12
            x = center_x + math.cos(angle) * orbit
            y = center_y + math.sin(angle) * orbit * 0.82
            size = 2 if index % 3 else 3
            self.surface.coords(particle, x - size, y - size, x + size, y + size)
            self.surface.itemconfig(particle, fill=self.colors["amber"] if index % 5 == 0 else self.colors["cyan"])

        self.root.after(40, self.animate_background)

    def clear_display(self):
        self.response_label.config(text="")
        if self.jarvis:
            self.jarvis.llm.clear_conversation()
        self.respond("Transcript cleared. Voice channel standing by.")

    def show_help(self):
        help_text = (
            "Select START CHAT for a continuous voice conversation. Say \"stop chat\" or select END CHAT when you are finished.\n\n"
            "You can also click the core to speak once, use the quick actions, or type a command.\n\n"
            "Shortcuts: Ctrl+K focuses the command field, Ctrl+L starts voice input, F1 opens this guide, and Up/Down recalls commands.\n\n"
            "Commands to try:\n\n"
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
        messagebox.showinfo("Jarvis Voice Commands", help_text)

    def quit_app(self):
        if messagebox.askokcancel("Shutdown", "Shut down Jarvis?"):
            self.root.destroy()
            sys.exit(0)


def run_gui():
    """Launch the GUI."""
    instance_mutex = acquire_instance_mutex()
    if sys.platform == "win32" and instance_mutex is None:
        duplicate_notice = tk.Tk()
        duplicate_notice.withdraw()
        messagebox.showwarning(
            "Jarvis is already running",
            "Close the existing Jarvis window before launching another one.",
            parent=duplicate_notice,
        )
        duplicate_notice.destroy()
        return

    root = tk.Tk()
    root.jarvis_instance_mutex = instance_mutex
    app = FuturisticGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()


JarvisGUI = FuturisticGUI


if __name__ == "__main__":
    run_gui()
