#!/usr/bin/env python3
"""
JARVIS - Holographic AI Interface v2.0
Futuristic Sci-Fi GUI with Advanced Interactive Elements
Inspired by Tony Stark's JARVIS from Iron Man
"""

import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import sys
from datetime import datetime

from jarvis.core import Jarvis



class FuturisticGUI:
    """Highly interactive futuristic GUI with sci-fi aesthetics"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("⬢ J.A.R.V.I.S - HOLOGRAPHIC INTERFACE ⬢")
        self.root.geometry("1400x900")
        self.root.resizable(True, True)
        
        # === NEON COLOR PALETTE ===
        self.colors = {
            'bg_main': "#0a0e27",          # Deep space
            'bg_secondary': "#0f1435",     # Grid dark
            'bg_panel': "#0d1120",         # Panel dark
            'neon_cyan': "#00ffff",        # Primary cyan
            'neon_magenta': "#ff00ff",     # Magenta
            'neon_green': "#00ff88",       # Success green
            'neon_blue': "#0099ff",        # Electric blue
            'neon_purple': "#aa00ff",      # Purple accent
            'neon_orange': "#ff6600",      # Warning orange
            'neon_pink': "#ff0088",        # Error pink
            'text_bright': "#e0ffff",      # Bright cyan
            'text_dim': "#99ffff",         # Dim cyan
            'grid': "#1a3a5a",             # Grid color
        }
        
        self.root.configure(bg=self.colors['bg_main'])
        
        # Animation state
        self.pulse = 0
        self.pulse_dir = 1
        self.animation_counter = 0
        self.listening = False
        
        # Initialize Jarvis
        self.jarvis = None
        init_thread = threading.Thread(target=self.init_jarvis, daemon=True)
        init_thread.start()
        
        # Build UI
        self.build_ui()
        self.animate_all()
    
    def init_jarvis(self):
        """Initialize Jarvis engine"""
        try:
            self.jarvis = Jarvis(gui_callback=self.display_message)
            self.display_message("⬢ SYSTEM", "█ Core initialization complete\n█ Quantum processors: ACTIVE\n█ Neural networks: ONLINE\n█ Ready for voice input", tag="success")
        except Exception as e:
            self.display_message("⬢ SYSTEM", f"█ Error: {e}", tag="error")
    
    def build_ui(self):
        """Build the complete futuristic interface"""
        
        # === TOP BANNER ===
        banner = tk.Frame(self.root, bg=self.colors['neon_cyan'], height=4)
        banner.pack(fill=tk.X)
        
        # === HEADER ===
        header = tk.Frame(self.root, bg=self.colors['bg_main'], height=120)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        # Title area
        title_frame = tk.Frame(header, bg=self.colors['bg_main'])
        title_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=20)
        
        # Main title with brackets
        title = tk.Label(title_frame, text="╔════ J.A.R.V.I.S ════╗", 
                        font=("Courier New", 24, "bold"),
                        fg=self.colors['neon_cyan'], bg=self.colors['bg_main'])
        title.pack(side=tk.LEFT)
        
        # Subtitle
        subtitle = tk.Label(title_frame, text="[ ADVANCED NEURAL INTERFACE ]",
                           font=("Courier New", 10),
                           fg=self.colors['neon_green'], bg=self.colors['bg_main'])
        subtitle.pack(side=tk.LEFT, padx=30)
        
        # Status indicator (pulsing)
        self.status_light = tk.Canvas(title_frame, width=50, height=50,
                                     bg=self.colors['bg_main'], highlightthickness=0)
        self.status_light.pack(side=tk.RIGHT)
        self.status_indicator = self.status_light.create_oval(10, 10, 40, 40,
                                                              fill=self.colors['neon_magenta'],
                                                              outline=self.colors['neon_cyan'],
                                                              width=3)
        
        # === MAIN CONTENT ===
        main_container = tk.Frame(self.root, bg=self.colors['bg_main'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # LEFT PANEL - Display Matrix
        left_section = tk.Frame(main_container, bg=self.colors['bg_panel'])
        left_section.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 15))
        
        # Neon border
        tk.Canvas(left_section, height=2, bg=self.colors['neon_blue'],
                 highlightthickness=0).pack(fill=tk.X)
        
        # Panel header
        panel_header = tk.Label(left_section, text="▓▓▓ RESPONSE MATRIX ▓▓▓",
                               font=("Courier New", 11, "bold"),
                               fg=self.colors['neon_blue'],
                               bg=self.colors['bg_panel'])
        panel_header.pack(fill=tk.X, padx=15, pady=15)
        
        # Main display
        self.display = scrolledtext.ScrolledText(
            left_section, height=25, width=90,
            bg=self.colors['bg_main'],
            fg=self.colors['text_bright'],
            font=("Courier New", 9),
            insertbackground=self.colors['neon_cyan'],
            relief=tk.FLAT, bd=0
        )
        self.display.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Configure text colors
        tags = {
            "system": (self.colors['neon_magenta'], "bold"),
            "user": (self.colors['neon_cyan'], "normal"),
            "jarvis": (self.colors['neon_green'], "normal"),
            "error": (self.colors['neon_pink'], "normal"),
            "success": (self.colors['neon_green'], "normal"),
            "info": (self.colors['neon_blue'], "normal"),
            "warning": (self.colors['neon_orange'], "normal"),
        }
        for tag, (color, style) in tags.items():
            weight = "bold" if style == "bold" else "normal"
            self.display.tag_config(tag, foreground=color, font=("Courier New", 9, weight))
        
        self.display.insert(tk.END, "» Initializing quantum processors...\n", "info")
        self.display.config(state=tk.DISABLED)
        
        # === RIGHT PANEL - Control Center ===
        right_section = tk.Frame(main_container, bg=self.colors['bg_panel'], width=280)
        right_section.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(15, 0))
        right_section.pack_propagate(False)
        
        # Neon border
        tk.Canvas(right_section, height=2, bg=self.colors['neon_purple'],
                 highlightthickness=0).pack(fill=tk.X)
        
        # Control header
        ctrl_header = tk.Label(right_section, text="▓▓▓ COMMAND CENTER ▓▓▓",
                              font=("Courier New", 10, "bold"),
                              fg=self.colors['neon_purple'],
                              bg=self.colors['bg_panel'])
        ctrl_header.pack(fill=tk.X, padx=15, pady=15)
        
        # Input area
        input_lbl = tk.Label(right_section, text="» Enter Command",
                            font=("Courier New", 8),
                            fg=self.colors['neon_blue'],
                            bg=self.colors['bg_panel'])
        input_lbl.pack(anchor=tk.W, padx=15, pady=(0, 5))
        
        self.input_cmd = tk.Entry(right_section, bg=self.colors['bg_main'],
                                 fg=self.colors['neon_cyan'],
                                 font=("Courier New", 9),
                                 insertbackground=self.colors['neon_cyan'],
                                 relief=tk.FLAT, bd=1)
        self.input_cmd.pack(fill=tk.X, padx=15, pady=(0, 15))
        self.input_cmd.bind("<Return>", lambda e: self.send_command())
        
        # Button grid
        button_frame = tk.Frame(right_section, bg=self.colors['bg_panel'])
        button_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        buttons = [
            ("▶ LISTEN", self.listen_cmd, self.colors['neon_cyan'], "#000000"),
            ("▶ EXECUTE", self.send_command, self.colors['neon_green'], "#000000"),
            ("▶ HELP", self.show_help, self.colors['neon_blue'], "#ffffff"),
            ("▶ CLEAR", self.clear_display, self.colors['neon_purple'], "#ffffff"),
            ("▶ ANALYZE", self.analyze_systems, self.colors['neon_orange'], "#000000"),
            ("▶ SHUTDOWN", self.quit_app, self.colors['neon_pink'], "#ffffff"),
        ]
        
        self.listen_btn = None
        for text, cmd, bg, fg in buttons:
            btn = tk.Button(button_frame, text=text, command=cmd,
                           bg=bg, fg=fg, font=("Courier New", 8, "bold"),
                           relief=tk.FLAT, bd=0, cursor="hand2",
                           padx=8, pady=8, activeforeground=fg)
            btn.pack(fill=tk.X, pady=4)
            if "LISTEN" in text:
                self.listen_btn = btn
        
        # === FOOTER ===
        footer = tk.Frame(self.root, bg=self.colors['bg_main'], height=50)
        footer.pack(fill=tk.X, side=tk.BOTTOM)
        footer.pack_propagate(False)
        
        # Bottom border
        tk.Canvas(footer, height=2, bg=self.colors['neon_magenta'],
                 highlightthickness=0).pack(fill=tk.X)
        
        self.status_text = tk.Label(footer, text="◆ System Ready ◆",
                                   font=("Courier New", 9),
                                   fg=self.colors['neon_green'],
                                   bg=self.colors['bg_main'])
        self.status_text.pack(anchor=tk.W, padx=20, pady=10)
    
    def display_message(self, label, text, tag="jarvis"):
        """Display message with timestamp"""
        self.display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        
        if label:
            self.display.insert(tk.END, f"[{timestamp}] {label}: ", "system")
        self.display.insert(tk.END, text + "\n", tag)
        self.display.see(tk.END)
        self.display.config(state=tk.DISABLED)
    
    def listen_cmd(self):
        """Voice input handler"""
        if not self.jarvis:
            self.display_message("⬢ SYSTEM", "Jarvis core not initialized", tag="error")
            return
        
        if self.listening:
            self.display_message("⬢ SYSTEM", "Already listening...", tag="warning")
            return
        
        self.listening = True
        self.listen_btn.config(bg=self.colors['neon_pink'], text="◆ LISTENING ◆")
        self.status_text.config(text="◆ LISTENING... SPEAK NOW ◆", fg=self.colors['neon_pink'])
        
        listen_thread = threading.Thread(target=self._listen_thread, daemon=True)
        listen_thread.start()
    
    def _listen_thread(self):
        """Background listening thread"""
        try:
            command = self.jarvis.listen()
            if command:
                self.display_message("YOU", command, tag="user")
                self.handle_command(command)
            else:
                self.display_message("⬢ SYSTEM", "No command detected", tag="info")
        except Exception as e:
            self.display_message("⬢ SYSTEM", f"Error: {str(e)}", tag="error")
        finally:
            self.listening = False
            self.listen_btn.config(bg=self.colors['neon_cyan'], text="▶ LISTEN")
            self.status_text.config(text="◆ System Ready ◆", fg=self.colors['neon_green'])
    
    def send_command(self):
        """Execute typed command"""
        cmd = self.input_cmd.get().strip()
        if not cmd:
            return
        
        if not self.jarvis:
            self.display_message("⬢ SYSTEM", "Jarvis core not available", tag="error")
            return
        
        self.display_message("YOU", cmd, tag="user")
        self.input_cmd.delete(0, tk.END)
        
        exec_thread = threading.Thread(target=lambda: self.handle_command(cmd), daemon=True)
        exec_thread.start()
    
    def handle_command(self, text):
        """Process command"""
        try:
            self.jarvis.handle_command(text)
        except SystemExit:
            self.quit_app()
        except Exception as e:
            self.display_message("⬢ SYSTEM", f"Error: {e}", tag="error")
    
    def analyze_systems(self):
        """System analysis"""
        analysis = """
╔════════════════════════════════════════╗
║     SYSTEM ANALYSIS - ALL ONLINE      ║
╚════════════════════════════════════════╝

► CPU Cores:        Optimized
► Memory:           Allocated
► Neural Networks:  Training
► Voice Engine:     Active
► Command Buffer:   Ready
► API Connections:  Stable
► Quantum State:    Coherent
► Status:           OPERATIONAL

[All systems nominal]
        """
        self.display_message("⬢ ANALYSIS", analysis, tag="success")
    
    def clear_display(self):
        """Clear display"""
        self.display.config(state=tk.NORMAL)
        self.display.delete(1.0, tk.END)
        self.display.insert(tk.END, "» Display cleared. Ready for new input.\n", "info")
        self.display.config(state=tk.DISABLED)
    
    def show_help(self):
        """Show help dialog"""
        help_text = """
╔════════════════════════════════════════════════╗
║        J.A.R.V.I.S COMMAND REFERENCE          ║
╚════════════════════════════════════════════════╝

🎤 VOICE COMMANDS:

App Control:
  • minimize [app]       - Hide window
  • maximize [app]       - Fullscreen window
  • close [app]          - Terminate application
  • focus [app]          - Bring to foreground
  • list windows         - Show all open windows

System Control:
  • volume up/down       - Adjust volume
  • set volume to [50]   - Set specific level
  • brightness up/down   - Adjust brightness
  • lock screen          - Secure display
  • sleep                - Suspend system
  • system info          - Hardware details

Productivity:
  • weather in [city]    - Get forecast
  • open [app]           - Launch application
  • search for [query]   - Web search
  • what time is it      - Tell time
  • add event [details]  - Calendar entry
  • remind me [task]     - Set reminder

Advanced:
  • help                 - Show all commands
  • how are you          - Small talk
  • tell me a joke       - Random joke
  • my name is [name]    - Set user name

═══════════════════════════════════════════════

💡 TIPS:
  • Speak clearly for best recognition
  • Use partial app names (chrome = Google Chrome)
  • Commands are case-insensitive
  • Type commands if voice unavailable
        """
        messagebox.showinfo("JARVIS Help System", help_text)
    
    def animate_all(self):
        """Master animation loop"""
        self.animation_counter = getattr(self, 'animation_counter', 0) + 1
        
        # Pulse effect on status light
        self.pulse += self.pulse_dir * 0.08
        if self.pulse > 1:
            self.pulse_dir = -1
        elif self.pulse < 0:
            self.pulse_dir = 1
        
        # Color pulse
        if self.listening:
            color = self.colors['neon_pink']
        else:
            if self.pulse > 0.5:
                color = self.colors['neon_magenta']
            else:
                color = self.colors['neon_cyan']
        
        try:
            self.status_light.itemconfig(self.status_indicator, fill=color)
        except:
            pass
        
        self.root.after(50, self.animate_all)
    
    def quit_app(self):
        """Graceful shutdown"""
        if messagebox.askokcancel("SHUTDOWN", "Shut down J.A.R.V.I.S system?"):
            self.root.destroy()
            sys.exit(0)


def run_gui():
    """Launch the futuristic GUI"""
    root = tk.Tk()
    app = FuturisticGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.quit_app)
    root.mainloop()


JarvisGUI = FuturisticGUI


if __name__ == "__main__":
    run_gui()
