#!/usr/bin/env python3
"""Voice-only eDEX-inspired Jarvis GUI."""

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
    """Voice-first assistant UI styled after eDEX-UI."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("JARVIS // VOICE TERMINAL")
        self.root.geometry("1360x820")
        self.root.minsize(1100, 700)

        self.colors = {
            "app": "#02070c",
            "surface": "#06131b",
            "surface_alt": "#081c26",
            "input": "#000b10",
            "border": "#0b5165",
            "border_dim": "#14313d",
            "text": "#d8fbff",
            "muted": "#69919b",
            "cyan": "#19f4f2",
            "cyan_dim": "#32a9b7",
            "green": "#4dff91",
            "amber": "#ffb020",
            "red": "#ff4d6d",
            "black": "#00070b",
        }

        self.jarvis: Jarvis | None = None
        self.listening = False
        self.executing = False
        self.keep_listening = tk.BooleanVar(value=True)
        self.stat_labels: dict[str, tk.Label] = {}
        self.pulse = False

        self.root.configure(bg=self.colors["app"])
        self.build_ui()
        self.set_state("BOOTING", "VOICE KERNEL INITIALIZING", "amber")
        self.add_message("JARVIS", "Voice command terminal online. Initializing modules.", "assistant")

        threading.Thread(target=self.init_jarvis, daemon=True).start()
        self.refresh_status()
        self.animate()

    def init_jarvis(self):
        """Initialize the assistant engine without blocking the window."""
        try:
            self.jarvis = Jarvis(gui_callback=self.display_message)
            if self.jarvis.microphone_available:
                self.add_message("JARVIS", "Microphone channel ready. Say a command after pressing SPEAK.", "assistant")
                self.root.after(0, lambda: self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green"))
            else:
                self.add_message("SYSTEM", "No microphone detected. Voice-only mode requires a microphone.", "error")
                self.root.after(0, lambda: self.set_state("NO MIC", "CONNECT MICROPHONE TO CONTINUE", "red"))
            self.root.after(0, self.update_voice_availability)
        except Exception as exc:
            self.add_message("SYSTEM", f"Jarvis could not start: {exc}", "error")
            self.root.after(0, lambda: self.set_state("FAULT", "STARTUP FAILED", "red"))

    def build_ui(self):
        """Build an eDEX-style voice command cockpit."""
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        self.build_header()

        body = tk.Frame(self.root, bg=self.colors["app"])
        body.grid(row=1, column=0, sticky="nsew", padx=14, pady=(0, 12))
        body.grid_columnconfigure(0, minsize=260)
        body.grid_columnconfigure(1, weight=1)
        body.grid_columnconfigure(2, minsize=330)
        body.grid_rowconfigure(0, weight=1)
        body.grid_rowconfigure(1, minsize=98)

        self.build_command_examples(body)
        self.build_terminal(body)
        self.build_telemetry(body)
        self.build_voice_deck(body)

    def build_header(self):
        header = tk.Frame(self.root, bg=self.colors["app"], height=88)
        header.grid(row=0, column=0, sticky="ew", padx=14, pady=(12, 10))
        header.grid_columnconfigure(1, weight=1)
        header.grid_propagate(False)

        self.orb = tk.Canvas(
            header,
            width=68,
            height=68,
            bg=self.colors["app"],
            highlightthickness=1,
            highlightbackground=self.colors["border"],
        )
        self.orb.grid(row=0, column=0, sticky="w")
        self.voice_ring = self.orb.create_oval(9, 9, 59, 59, outline=self.colors["cyan"], width=2)
        self.voice_core = self.orb.create_oval(26, 26, 42, 42, fill=self.colors["amber"], width=0)
        self.orb.create_line(34, 4, 34, 64, fill=self.colors["border_dim"])
        self.orb.create_line(4, 34, 64, 34, fill=self.colors["border_dim"])

        title = tk.Frame(header, bg=self.colors["app"])
        title.grid(row=0, column=1, sticky="ew", padx=16)

        tk.Label(
            title,
            text="JARVIS",
            font=("Consolas", 30, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["app"],
        ).pack(anchor="w")
        tk.Label(
            title,
            text="VOICE-ONLY EDEX COMMAND INTERFACE // LOCAL ASSISTANT NODE",
            font=("Consolas", 10, "bold"),
            fg=self.colors["muted"],
            bg=self.colors["app"],
        ).pack(anchor="w")

        status = self.panel(header, width=330)
        status.grid(row=0, column=2, sticky="e")
        status.grid_columnconfigure(0, weight=1)

        self.clock_label = tk.Label(
            status,
            text="--:--:--",
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

    def build_command_examples(self, parent: tk.Frame):
        rail = self.panel(parent)
        rail.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        rail.grid_columnconfigure(0, weight=1)

        self.section_title(rail, "VOICE COMMANDS").grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))

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
            text="VOICE: CHECKING\nTTS: CHECKING",
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

        head = tk.Frame(terminal, bg=self.colors["surface"])
        head.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 6))
        head.grid_columnconfigure(1, weight=1)

        tk.Label(
            head,
            text="[ TRANSCRIPT ]",
            font=("Consolas", 11, "bold"),
            fg=self.colors["cyan"],
            bg=self.colors["surface"],
        ).grid(row=0, column=0, sticky="w")
        tk.Label(
            head,
            text="VOICE STREAM // READ ONLY",
            font=("Consolas", 9),
            fg=self.colors["muted"],
            bg=self.colors["surface"],
        ).grid(row=0, column=1, sticky="e")

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
        self.display.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))
        self.display.tag_config("assistant", foreground=self.colors["green"])
        self.display.tag_config("user", foreground=self.colors["cyan"])
        self.display.tag_config("system", foreground=self.colors["muted"])
        self.display.tag_config("error", foreground=self.colors["red"], font=("Consolas", 10, "bold"))
        self.display.tag_config("label", foreground=self.colors["amber"], font=("Consolas", 9, "bold"))
        self.display.config(state=tk.DISABLED)

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
        self.section_title(activity, "SIGNAL").pack(fill=tk.X, padx=12, pady=(12, 8))
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
            text="Awaiting voice input.",
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
            text="SPEAK",
            command=self.listen_cmd,
            bg=self.colors["cyan"],
            fg=self.colors["black"],
            activebackground=self.colors["green"],
            activeforeground=self.colors["black"],
            relief=tk.FLAT,
            bd=0,
            cursor="hand2",
            font=("Consolas", 13, "bold"),
            padx=24,
            pady=16,
        )
        self.listen_btn.grid(row=0, column=0, sticky="w", padx=12, pady=12)

        self.deck_label = tk.Label(
            deck,
            text="VOICE COMMAND MODE ENABLED // KEYBOARD COMMAND INPUT DISABLED",
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

    def panel(self, parent: tk.Widget, width: int | None = None):
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

    def add_message(self, speaker: str, text: str, tag: str = "system"):
        """Thread-safe transcript append."""
        if threading.current_thread() is not threading.main_thread():
            self.root.after(0, lambda: self.add_message(speaker, text, tag))
            return

        timestamp = datetime.now().strftime("%H:%M:%S")
        self.display.config(state=tk.NORMAL)
        self.display.insert(tk.END, f"{timestamp}  {speaker:<8}\n", "label")
        self.display.insert(tk.END, f"{text}\n\n", tag)
        self.display.see(tk.END)
        self.display.config(state=tk.DISABLED)
        if hasattr(self, "signal_text"):
            self.signal_text.config(text=f"Last event: {speaker} @ {timestamp}")

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
        self.add_message("JARVIS", "Listening.", "assistant")
        threading.Thread(target=self._listen_thread, daemon=True).start()

    def _listen_thread(self):
        try:
            assert self.jarvis is not None
            command = self.jarvis.listen()
            if command:
                self.add_message("YOU", command, "user")
                self.handle_command(command)
            else:
                self.add_message("JARVIS", "No command detected. Press SPEAK and try again.", "assistant")
        except SystemExit:
            self.add_message("SYSTEM", "Voice recognition is not available in this environment.", "error")
        except Exception as exc:
            self.add_message("SYSTEM", f"Voice input failed: {exc}", "error")
        finally:
            self.listening = False
            self.root.after(0, self.reset_voice_controls)

    def handle_command(self, command: str):
        if self.executing:
            self.add_message("SYSTEM", "Previous command is still executing.", "system")
            return

        self.executing = True
        self.set_state("EXECUTING", "RUNNING VOICE COMMAND", "amber")
        self.listen_btn.config(state=tk.DISABLED)
        threading.Thread(target=lambda: self._execute_command(command), daemon=True).start()

    def _execute_command(self, command: str):
        try:
            assert self.jarvis is not None
            self.jarvis.handle_command(command)
            self.add_message("JARVIS", "Standing by for the next voice command.", "assistant")
        except SystemExit:
            self.root.after(0, self.quit_app)
        except Exception as exc:
            self.add_message("SYSTEM", f"Command failed: {exc}", "error")
        finally:
            self.executing = False
            self.root.after(0, self.reset_after_command)
            if self.keep_listening.get():
                self.root.after(900, self.listen_cmd)

    def reset_after_command(self):
        if self.jarvis and self.jarvis.microphone_available:
            self.listen_btn.config(state=tk.NORMAL)
        if not self.listening:
            self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green")

    def reset_voice_controls(self):
        self.listen_btn.config(text="SPEAK", bg=self.colors["cyan"])
        if self.jarvis and self.jarvis.microphone_available and not self.executing:
            self.listen_btn.config(state=tk.NORMAL)
        if not self.executing:
            self.set_state("READY", "PRESS SPEAK // ISSUE VOICE COMMAND", "green")

    def update_voice_availability(self):
        if not self.jarvis:
            return
        tts = self.jarvis.tts_voice_name or "UNAVAILABLE"
        if self.jarvis.microphone_available:
            self.voice_status.config(text=f"VOICE: READY\nTTS: {tts}", fg=self.colors["green"])
            self.listen_btn.config(state=tk.NORMAL)
            self.set_stat("MIC", "READY")
        else:
            self.voice_status.config(text=f"VOICE: UNAVAILABLE\nTTS: {tts}", fg=self.colors["red"])
            self.listen_btn.config(state=tk.DISABLED, bg=self.colors["surface_alt"], fg=self.colors["muted"])
            self.set_stat("MIC", "MISSING")
        self.set_stat("TTS", tts)
        self.set_stat("MODE", "VOICE ONLY")

    def refresh_status(self):
        """Refresh clock, system status, and activity graph."""
        self.clock_label.config(text=datetime.now().strftime("%H:%M:%S"))
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

        for index, x in enumerate(range(8, width - 8, step)):
            value = (int(cpu) + int(mem) + index * 9) % 100
            bar = int((value / 100) * (height - 26))
            color = self.colors["amber"] if self.listening or value > 78 else self.colors["cyan"]
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
            text="VOICE/SYSTEM SIGNAL",
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
        ring = self.colors["cyan"] if self.pulse else self.colors["border"]
        core = self.colors["amber"] if self.listening or self.executing else self.colors["green"]
        self.orb.itemconfig(self.voice_ring, outline=ring)
        self.orb.itemconfig(self.voice_core, fill=core)
        self.root.after(700, self.animate)

    def clear_display(self):
        self.display.config(state=tk.NORMAL)
        self.display.delete("1.0", tk.END)
        self.display.config(state=tk.DISABLED)
        self.add_message("JARVIS", "Transcript cleared. Voice channel standing by.", "assistant")

    def show_help(self):
        help_text = (
            "Voice commands to try:\n\n"
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
    root = tk.Tk()
    app = FuturisticGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()


JarvisGUI = FuturisticGUI


if __name__ == "__main__":
    run_gui()
