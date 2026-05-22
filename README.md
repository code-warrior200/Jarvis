# Jarvis AI Assistant

🤖 A local Jarvis assistant for Windows with **GUI** or terminal interface, voice control, offline AI fallback, weather, calendar, reminders, app launching, web search, face detection, and advanced window management.

## Quick Start

### 1. Install dependencies

Open PowerShell in `C:\Users\Dell\Desktop\Jarvis` and run:

```powershell
python -m pip install -r requirements.txt
```

If `pyaudio` fails, install it with:

```powershell
python -m pip install pipwin
python -m pipwin install pyaudio
```

### 2. Run Jarvis

```powershell
python jarvis.py
```

✨ **GUI will launch automatically!** The modern graphical interface provides voice and text input with visual feedback.

If you prefer terminal mode:
```powershell
python launcher.py  # Uses terminal instead of GUI
```

## Optional local AI model

To enable a local LLM, set `JARVIS_LOCAL_MODEL_PATH` to a downloaded model directory or file. Example:

```powershell
$env:JARVIS_LOCAL_MODEL_PATH = 'C:\models\llama-2-7b'
python jarvis.py
```

## Example commands

### Productivity & Information

- `weather in Seattle`
- `add calendar event Team meeting on 2026-05-25 at 15:00`
- `remind me to call mom in 30 minutes`
- `search for local coffee shops`
- `system info`

### App Management

- `open notepad`
- `minimize chrome`
- `maximize visual studio code`
- `close calculator`
- `focus spotify`
- `list windows`

### System Control

- `volume up` / `volume down` / `set volume to 50`
- `brightness up` / `brightness down` / `set brightness to 75`
- `lock screen`
- `sleep`

### Entertainment & Interaction

- `face recognition`
- `tell me a joke`
- `what time is it`
- `what is the date`
- `help`

## Interfaces

### 🎨 GUI Mode (Default)
- Modern dark theme interface
- Visual microphone feedback
- Real-time command history
- Color-coded responses
- Type or speak commands
- System status indicator

See **[GUI_GUIDE.md](GUI_GUIDE.md)** for detailed GUI documentation.

### 💻 Terminal Mode
- Classic command-line interface
- Voice input with text feedback
- Works without tkinter
- Lightweight and responsive

## File Overview

- **jarvis.py** - Main launcher (GUI or terminal)
- **jarvis_gui.py** - Modern GUI interface
- **jarvis_main.py** - Core Jarvis engine
- **jarvis_data.json** - Auto-saved user data (calendar, reminders)
- **requirements.txt** - Python dependencies
- **GUI_GUIDE.md** - GUI documentation
- **FEATURES.md** - Feature details
- **CHANGELOG.md** - Version history

## Documentation

- 📖 **[README.md](README.md)** - This file
- 🎨 **[GUI_GUIDE.md](GUI_GUIDE.md)** - GUI interface guide
- ✨ **[FEATURES.md](FEATURES.md)** - Complete feature list
- ⚙️ **[SETUP_GUIDE.md](SETUP_GUIDE.md)** - Advanced setup
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history

## System Requirements

- **Python** 3.7+
- **Windows** 7+ (or Linux/macOS with adjustments)
- **Microphone** for voice input
- **Internet** for weather, web search (optional local LLM available)
- **4GB RAM** minimum recommended

## Key Features

✅ **Voice Control** - Hands-free operation  
✅ **GUI Interface** - Modern graphical experience  
✅ **Window Management** - Minimize, maximize, close apps  
✅ **System Control** - Volume, brightness, sleep  
✅ **Productivity** - Calendar, reminders, weather  
✅ **Web Search** - Google search integration  
✅ **Face Recognition** - With OpenCV  
✅ **Offline Support** - Works without internet  
✅ **Local AI** - Optional LLM support  
✅ **Cross-Platform** - Windows/Linux/macOS  

## Troubleshooting

### GUI won't load
```powershell
# Install tkinter
pip install tk

# Or use terminal mode
python launcher.py
```

### Microphone not detected
```powershell
# Check Windows Sound Settings
# Ensure microphone is enabled and selected as default
# Test with: python -c "import speech_recognition; print('OK')"
```

### Commands not working
- Speak clearly and at normal volume
- Use keywords from the command list
- Try typing commands instead of speaking
- Check microphone levels in Windows Settings

## Getting Started Quickly

```powershell
# 1. Install
python -m pip install -r requirements.txt

# 2. Run
python jarvis.py

# 3. Try a command (via GUI or microphone)
# "what time is it"
# "open notepad"
# "set volume to 50"
```

## Advanced

### Using Local LLM
```powershell
$env:JARVIS_LOCAL_MODEL_PATH = 'C:\path\to\model'
python jarvis.py
```

### Custom Configuration
Edit `jarvis_main.py` to:
- Add new known apps
- Customize voice parameters
- Extend command handlers
- Modify UI colors/layout

### Importing as Library
```python
from jarvis_main import Jarvis, WindowManager, SystemControl

jarvis = Jarvis()
WindowManager.minimize("chrome")
SystemControl.set_volume(75)
```

## Performance

- Lightweight (~50MB with dependencies)
- Runs in background threads
- Minimal CPU usage (~2-5%)
- Quick startup (2-3 seconds)

## License

Open source. See repository for details.

## Contributing

Suggestions and improvements welcome!

## Support

- 📖 Check documentation files
- 💬 Type "help" in Jarvis
- 🔧 Review troubleshooting section
- 📝 Check CHANGELOG.md for updates
