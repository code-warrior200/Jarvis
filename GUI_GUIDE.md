# Jarvis GUI Interface Guide

## Overview

Jarvis now runs with a modern graphical user interface (GUI) by default when you run:
```bash
python jarvis.py
```

The GUI provides a better user experience with:
- ✨ Modern dark theme interface
- 🎤 Visual microphone feedback
- 📝 Real-time command history and responses
- 🎨 Color-coded text for different message types
- ⚡ Responsive buttons and controls
- 📊 System status indicator

## Quick Start

### 1. Installation

Install Jarvis with GUI support:

```bash
# Standard install
python -m pip install -r requirements.txt

# GUI requires tkinter (usually included with Python)
# On Ubuntu/Debian:
sudo apt-get install python3-tk

# On Fedora:
sudo dnf install python3-tkinter

# On Windows:
# tkinter comes with Python by default
```

### 2. Run Jarvis

Simply run:
```bash
python jarvis.py
```

The launcher will automatically detect tkinter and launch the GUI if available.

## GUI Features

### Main Window

**Header Section:**
- 🤖 **JARVIS** - Application title
- 🟢 **Status Indicator** - Green when ready, red while initializing
- Status message showing current state

### Response Display

Large scrolled text area showing:
- **Jarvis responses** (Green text)
- **Your commands** (Blue text)
- **System messages** (Orange text)
- **Errors** (Red text)
- **Success messages** (Green text)

Each entry includes a timestamp for easy tracking.

### Input Methods

#### Voice Input
- **🎤 Listen Button** - Click to start listening
- Jarvis will prompt you to speak
- Automatically processes your voice command
- Status changes to "🎤 Listening..." while recording

#### Manual Input
- **Text input field** - Type commands directly
- Press **Enter** or click **📤 Send** to execute
- Useful when microphone isn't available
- Commands are processed same as voice

### Action Buttons

| Button | Function | Shortcut |
|--------|----------|----------|
| 🎤 Listen | Start voice input | N/A |
| 📤 Send | Execute typed command | Enter |
| ❓ Help | Show command reference | N/A |
| 🗑️ Clear | Clear display | N/A |

### Status Area

- **Connection Status** - Shows if Jarvis is online
- **Info Message** - Current status and tips
- **Ready indicator** - When system is ready for commands

## Usage Examples

### Voice Commands in GUI

1. Click the **🎤 Listen** button
2. Wait for "Listening now" prompt
3. Speak your command clearly:
   - "Minimize chrome"
   - "What's the weather in London?"
   - "Set volume to 50"
   - "Open notepad"

4. Jarvis will process and display the response

### Text Commands in GUI

1. Type your command in the input field
2. Press **Enter** or click **📤 Send**
3. Response appears in the display area

### Mixed Usage

- Use voice when hands-free preferred
- Use text when in quiet/loud environments
- Combine both for flexibility

## Terminal Fallback

If tkinter is not available, Jarvis automatically falls back to terminal mode:

```
[*] tkinter not available - using terminal interface...
[*] For GUI support, ensure tkinter is installed

Jarvis: Hello, I am Jarvis. Say help for a list of commands.
Listening now.
```

Terminal mode works exactly like before with voice input.

## Color Guide

| Color | Meaning | Example |
|-------|---------|---------|
| 🟢 Green | Success / Jarvis responses | "Minimized chrome" |
| 🔵 Blue | Your commands | Your spoken/typed input |
| 🟠 Orange | System information | "Initialization messages" |
| 🔴 Red | Errors | "Could not find app" |

## Tips & Tricks

### Better Voice Recognition
1. **Speak clearly** - Enunciate each word
2. **Normal pace** - Don't rush or speak too slow
3. **Reasonable volume** - Not too quiet, not shouting
4. **Minimize background noise** - Quiet environment works best
5. **Use partial names** - "chrome" works for "Google Chrome"

### Window Management
1. Resize the window for better visibility
2. Scroll through history to see past commands
3. Clear display when it gets cluttered
4. Keep window visible for feedback

### Troubleshooting

**GUI won't load:**
```bash
# Check if tkinter is installed
python -m tkinter

# If not, install it (platform-specific instructions above)

# Run terminal version instead
python launcher.py  # Forces terminal mode
```

**Microphone not working:**
1. Check Windows Sound Settings
2. Ensure microphone is selected as default device
3. Test mic with other applications
4. Type commands instead using text input

**Commands not recognized:**
1. Speak more clearly
2. Use keyword-based commands
3. Check "Help" for exact syntax
4. Try text input instead

## File Structure

```
Jarvis/
├── jarvis.py           ← Main launcher (runs GUI or terminal)
├── jarvis_gui.py       ← GUI interface module
├── jarvis_main.py      ← Core Jarvis engine
├── launcher.py         ← Alternative launcher
├── jarvis_data.json    ← User data (auto-created)
├── requirements.txt    ← Dependencies
└── README.md          ← General documentation
```

## Configuration

### Environment Variables

GUI behavior can be controlled via environment variables:

```bash
# Force terminal mode (no GUI)
set JARVIS_NO_GUI=1
python jarvis.py

# Enable debug mode
set JARVIS_DEBUG=1
python jarvis.py
```

### User Data

Jarvis stores user data in `jarvis_data.json`:
- Calendar events
- Reminders
- User preferences (auto-saved)

This file is automatically created and managed.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| **Enter** | Send text command |
| **Ctrl+C** | Exit Jarvis |
| **Alt+F4** | Close window |

## Advanced Usage

### Running Multiple Instances

You can run multiple Jarvis windows:
```bash
# Window 1
python jarvis.py

# Window 2 (in another terminal)
python jarvis.py
```

Each instance is independent.

### Customizing the GUI

Edit `jarvis_gui.py` to:
- Change colors/theme
- Adjust window size
- Modify button layout
- Add new features

### Integrating with Other Tools

The `jarvis_main.py` can be imported into other Python projects:

```python
from jarvis_main import Jarvis, WindowManager, SystemControl

# Use in your own application
jarvis = Jarvis(gui_callback=your_callback_function)
```

## Performance Tips

- **Keep history clean** - Use "Clear" button occasionally
- **Close unused apps** - Reduces command search time
- **Restart if slow** - Clears memory cache
- **Update dependencies** - `pip install --upgrade -r requirements.txt`

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| GUI very slow | Clear display, close other apps |
| Voice not recognized | Speak louder/clearer, check mic |
| Commands not working | Use exact keywords, try text input |
| Window freezes | Wait for current command to finish |
| Memory usage high | Restart Jarvis application |

## Features Summary

✅ Modern GUI interface
✅ Voice and text input
✅ Command history
✅ Color-coded responses
✅ System status indicator
✅ Help reference
✅ Terminal fallback
✅ Cross-platform compatible
✅ Real-time feedback
✅ Multi-command support

## Support

For issues or questions:
1. Check the Help button in the GUI
2. Review command syntax in documentation
3. Try terminal mode if GUI fails
4. Check jarvis_data.json for debug info

## Updates

To get the latest features:
```bash
# Update all dependencies
pip install --upgrade -r requirements.txt

# Re-run Jarvis
python jarvis.py
```
