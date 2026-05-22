# 🚀 Jarvis Quick Reference

## Installation (First Time)

```powershell
# Navigate to Jarvis folder
cd C:\Users\Dell\Desktop\Jarvis

# Install dependencies
python -m pip install -r requirements.txt

# If pyaudio fails
python -m pip install pipwin
python -m pipwin install pyaudio
```

## Launch Jarvis

```powershell
# GUI Mode (Default) - Recommended
python jarvis.py

# Terminal Mode (if GUI unavailable)
python launcher.py
```

## GUI Quick Start

1. **Click 🎤 Listen** → Speak your command
2. **Or type** in the text field → Press Enter
3. **See response** in the display area
4. **Repeat** with new commands

## Common Voice Commands

### Information
- "What time is it?"
- "What is the date?"
- "Weather in [city]"
- "System info"

### Apps
- "Open notepad"
- "Minimize chrome"
- "Maximize [app]"
- "Close calculator"
- "List windows"

### System
- "Volume up" / "Volume down" / "Set volume to 50"
- "Brightness up" / "Brightness down"
- "Lock screen"
- "Sleep"

### Productivity
- "Add calendar event [title] on [date]"
- "Remind me to [task] in [time]"
- "Search for [query]"

### Fun
- "Tell me a joke"
- "Help" - Show all commands

## Text vs Voice

| Method | When to Use | How |
|--------|------------|-----|
| Voice | Hands-free, quiet environment | Click 🎤 Listen button |
| Text | Loud environment, mic broken | Type + press Enter |
| Mixed | Flexible approach | Use both as needed |

## Troubleshooting

### GUI won't start
```powershell
pip install tk
python jarvis.py
```

### Microphone not working
- Check Windows Sound Settings
- Ensure microphone is enabled
- Type commands instead

### Command not recognized
- Speak more clearly
- Check Help for exact syntax
- Try typing instead
- Use partial app names

## File Reference

| File | Purpose |
|------|---------|
| jarvis.py | Main launcher |
| jarvis_gui.py | GUI interface |
| jarvis_main.py | Core engine |
| GUI_GUIDE.md | Detailed GUI guide |
| FEATURES.md | All features |
| README.md | Full documentation |

## GUI Buttons

| Button | Function |
|--------|----------|
| 🎤 Listen | Start voice input |
| 📤 Send | Execute text command |
| ❓ Help | Show command help |
| 🗑️ Clear | Clear display |

## Tips

✨ **Voice Tips**
- Speak clearly
- Use normal pace
- Minimize background noise
- Use keyword commands

🎨 **GUI Tips**
- Resize window for visibility
- Use Clear button to declutter
- Check Help for command syntax
- Keep mic close but not touching

⚡ **Performance Tips**
- Close unused apps
- Keep only needed windows open
- Restart if memory gets high
- Update dependencies regularly

## Command Syntax

### Weather
```
"weather in Seattle"
"weather in London"
"what's the weather"
```

### Calendar
```
"add calendar event Meeting on 2026-05-25 at 15:00"
"list calendar events"
"show calendar"
```

### Reminders
```
"remind me to call mom in 30 minutes"
"remind me to mail check in 2 hours"
"remind me tomorrow at 9 am"
```

### Apps
```
"open notepad"
"launch chrome"
"start calculator"
"minimize firefox"
```

### System
```
"set volume to 75"
"brightness up"
"lock screen"
"sleep"
```

## Environment Variables

```powershell
# Force terminal mode
$env:JARVIS_NO_GUI = 1

# Set local LLM
$env:JARVIS_LOCAL_MODEL_PATH = "C:\path\to\model"

# Enable debug
$env:JARVIS_DEBUG = 1
```

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Enter | Send text command |
| Ctrl+C | Exit |
| Alt+F4 | Close window |

## Status Indicators

| Status | Meaning |
|--------|---------|
| 🟢 Green | Ready and online |
| 🔴 Red | Initializing |
| 🎤 Listening | Voice recording active |
| ⏳ Processing | Command being processed |

## Data Files

- **jarvis_data.json** - Auto-saved user data (events, reminders)
- **jarvis_gui.py** - GUI code
- **jarvis_main.py** - Jarvis engine

## Getting Help

1. Click **❓ Help** button in GUI
2. Say "help" in voice mode
3. Read **GUI_GUIDE.md** for details
4. Check **FEATURES.md** for all capabilities
5. Review **README.md** for setup

## Advanced Usage

### Import as Library
```python
from jarvis_main import Jarvis
jarvis = Jarvis()
jarvis.speak("Hello")
```

### Customize
Edit `jarvis_gui.py` or `jarvis_main.py` to:
- Change colors
- Add commands
- Modify behavior

### Local LLM
```powershell
$env:JARVIS_LOCAL_MODEL_PATH = "C:\models\llama-2"
python jarvis.py
```

## System Requirements

- Python 3.7+
- 4GB RAM (recommended)
- Microphone (optional, can use text)
- Windows 7+ (or Linux/macOS)
- Internet (optional, for weather/web search)

## Files Summary

```
Jarvis/
├── jarvis.py                    ← RUN THIS
├── jarvis_gui.py               ← GUI module
├── jarvis_main.py              ← Core engine
├── launcher.py                 ← Alt launcher
├── requirements.txt            ← Dependencies
├── jarvis_data.json            ← Your data
├── README.md                   ← Main docs
├── GUI_GUIDE.md               ← GUI docs
├── FEATURES.md                ← Features
├── SETUP_GUIDE.md             ← Setup
├── CHANGELOG.md               ← Version info
└── GUI_IMPLEMENTATION.md      ← Implementation details
```

## One-Minute Setup

```powershell
# 1. Install (1 minute)
python -m pip install -r requirements.txt

# 2. Run (instant)
python jarvis.py

# 3. Use (now!)
# Click 🎤 Listen and start talking
```

## Support

- 📖 See **GUI_GUIDE.md**
- 🎤 Say "help" to Jarvis
- 📁 Check **README.md**
- ✨ Review **FEATURES.md**

## Quick Stats

- ⚡ **Startup**: 2-3 seconds
- 💾 **Size**: ~80MB with dependencies
- 🔧 **CPU**: <5% idle
- 📦 **Dependencies**: 10 packages
- 🎨 **Interface**: Modern GUI + Terminal
- 🗣️ **Voice**: Google Speech-to-Text API
- 🤖 **AI**: Offline fallback + optional LLM

---

**Ready?** Run: `python jarvis.py` 🚀
