# Jarvis AI Assistant

Jarvis is a local Python assistant with a Tkinter GUI, terminal fallback, voice input, text-to-speech responses, app/window controls, reminders, weather lookup, web search, and optional local LLM support.

## Quick Start

```powershell
python -m pip install -r requirements.txt
python run.py
```

You can also launch it as a module:

```powershell
python -m jarvis
```

Run the setup check with:

```powershell
python scripts/verify_setup.py
```

## Project Structure

```text
Jarvis/
├── jarvis/
│   ├── core/
│   │   └── assistant.py          # Core assistant engine
│   ├── ui/
│   │   └── futuristic_gui.py     # Tkinter GUI
│   ├── launcher.py               # GUI-first launcher with terminal fallback
│   └── __main__.py               # python -m jarvis entry point
├── scripts/
│   ├── verify_setup.py           # Environment verification
│   ├── run_jarvis.py             # Legacy launcher wrapper
│   └── start_gui.py              # Legacy GUI wrapper
├── tests/
│   └── test_imports.py           # Import smoke tests
├── docs/
│   └── archive/                  # Historical notes and generated docs
├── run.py                        # Source checkout launcher
├── pyproject.toml
├── setup.py
└── requirements.txt
```

## Common Commands

```powershell
python run.py
python -m jarvis
python -m pytest
python scripts/verify_setup.py
```

## Optional Local Model

Set `JARVIS_LOCAL_MODEL_PATH` to a local model path if you want the optional local LLM integration:

```powershell
$env:JARVIS_LOCAL_MODEL_PATH = "C:\models\llama-2-7b"
python run.py
```

## Notes

Runtime data is stored in `jarvis_data.json` at the project root and is ignored by git. Generated caches, virtual environments, build outputs, and local environment files are also ignored.
