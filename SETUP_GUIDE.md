# Jarvis Setup and Usage Guide

## Installation

### 1. Install Python Dependencies

Open Command Prompt or PowerShell in the Jarvis directory and run:

```bash
python -m pip install -r requirements.txt
```

If you encounter issues with `pyaudio`, use:

```bash
python -m pip install pipwin
python -m pipwin install pyaudio
```

### 2. Install Optional Dependencies

For the new app control features, the following packages are already in requirements.txt:

- **pygetwindow** - Window management
- **pyautogui** - System automation
- **psutil** - System monitoring

## Running Jarvis

```bash
python jarvis.py
```

Jarvis will start with voice recognition enabled. Speak commands into your microphone.

## Quick Command Reference

### App Control

- "minimize chrome"
- "maximize visual studio code"
- "close calculator"
- "focus spotify"
- "list windows"

### System Control

- "volume up" / "volume down" / "set volume to 50"
- "brightness up" / "brightness down" / "set brightness to 75"
- "lock screen"
- "sleep"

### Information

- "system info" - Shows CPU, RAM, and disk usage
- "what time is it"
- "weather in [city]"

### Productivity

- "add calendar event [title] on [date] at [time]"
- "remind me to [task] in [time]"
- "open [app]"
- "search for [query]"

### Help

- "help" - Lists all available commands

## Troubleshooting

### Microphone not detected

- Ensure your microphone is connected and working
- Check Windows Sound settings
- Restart Jarvis

### Window management not working

- Ensure the application window title contains the app name you're saying
- Try using the full app name or partial matches
- Check "list windows" to see exact window titles

### Volume/Brightness control not working

- These commands use system keyboard shortcuts (Fn keys)
- Verify your keyboard supports these shortcuts
- Some laptops may require Fn key to be held

### Speech recognition issues

- Check internet connection (Google Speech API requires it)
- Speak clearly and at normal volume
- Ensure minimal background noise
- Adjust microphone input levels in Windows Sound settings

## Advanced Features

### Local LLM Integration

To use a local language model instead of online APIs:

```bash
$env:JARVIS_LOCAL_MODEL_PATH = 'C:\path\to\model'
python jarvis.py
```

The model should be compatible with:

- llama-cpp-python (GGUF format)
- Hugging Face transformers

### Customization

Edit `jarvis.py` to:

- Add more known apps to the `known_apps` dictionary
- Customize voice parameters (pitch, rate, volume)
- Extend command handling
- Add new system control features

## Voice Commands Tips

1. **Speak naturally** - Jarvis uses Google's Speech-to-Text API
2. **Pause for responses** - Wait for Jarvis to finish speaking before giving the next command
3. **Be specific** - Use full or partial app names that appear in window titles
4. **Clear articulation** - Speak clearly for better recognition
5. **No background noise** - Minimize background sounds for better accuracy

## Known Limitations

- Window management works best with standard Windows applications
- Volume control may not work on all hardware configurations
- Some system commands may require elevated privileges
- Online features (weather, web search) require internet connection
- Speech recognition works best in English

## Permissions

Some features may require elevated privileges:

- Lock screen
- System sleep/hibernation
- Brightness control (on some systems)

Run as Administrator if you experience permission issues.

## File Structure

```
Jarvis/
├── jarvis.py              # Main application
├── requirements.txt       # Python dependencies
├── jarvis_data.json       # Calendar events and reminders (auto-created)
├── README.md              # General information
├── FEATURES.md            # Feature documentation
├── SETUP_GUIDE.md         # This file
└── test_imports.py        # Import verification script
```

## Getting Help

Type or say "help" at any time to see available commands.

For issues or bugs, check the Jarvis console for error messages.
