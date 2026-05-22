# Jarvis AI Assistant

A local Jarvis assistant for Windows with voice control, offline AI fallback, weather, calendar, reminders, app launching, web search, face detection, and advanced window management.

## Install dependencies

Open PowerShell in `C:\Users\Dell\Desktop\Jarvis` and run:

```powershell
python -m pip install -r requirements.txt
```

If `pyaudio` fails, install it with:

```powershell
python -m pip install pipwin
python -m pipwin install pyaudio
```

## Run Jarvis

```powershell
python jarvis.py
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
