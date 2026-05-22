# Jarvis Enhanced Features

## New Interactive Capabilities

Jarvis has been enhanced with comprehensive app control and system management features. All commands remain **voice-controlled** through your microphone.

### Window Management Commands

Control and manage open application windows:

- **Minimize**: `minimize [app name]`
  - Example: "minimize chrome" → Minimizes the Chrome window
  
- **Maximize**: `maximize [app name]`
  - Example: "maximize visual studio code" → Maximizes VS Code
  
- **Close**: `close [app name]`
  - Example: "close calculator" → Closes Calculator application
  
- **Focus/Bring to Front**: `focus [app name]`
  - Example: "focus spotify" → Brings Spotify to the foreground
  
- **List Open Windows**: `list windows`
  - Shows all currently open application windows
  - Example: "list windows" → "Open windows: Notepad, Chrome, Explorer..."

### System Control Commands

Manage system-level settings:

#### Volume Control

- `volume up` → Increase volume by one step
- `volume down` → Decrease volume by one step
- `set volume to [0-100]` → Set volume to specific percentage
- Example: "volume up", "set volume to 50"

#### Brightness Control

- `brightness up` → Increase screen brightness
- `brightness down` → Decrease screen brightness
- `set brightness to [0-100]` → Set brightness to specific percentage
- Example: "brightness down", "set brightness to 75"

#### Screen & System

- `lock screen` → Lock Windows workstation
- `sleep` → Put system to sleep/hibernation
- `system info` → Display CPU, RAM, and disk usage information

## Architecture Enhancements

### New Classes

1. **WindowManager**
   - Handles all window operations
   - Methods: minimize(), maximize(), close(), focus(), resize(), list_windows()
   - Uses pygetwindow library for cross-platform compatibility

2. **SystemControl**
   - Manages system-level controls
   - Methods: set_volume(), volume_up/down(), set_brightness(), brightness_up/down()
   - Methods: lock_screen(), sleep(), system_info()
   - Uses pyautogui for keyboard shortcuts and psutil for system metrics

### Updated Jarvis Class

- Added 10 new command handlers for window and system control
- Extended command recognition in handle_command()
- Updated help documentation with new features
- All commands integrate seamlessly with existing voice interface

## New Dependencies

Added to requirements.txt:

- **pygetwindow** - Window management and detection
- **pyautogui** - Keyboard and mouse automation
- **psutil** - System performance monitoring

## Usage Examples

```
User: "minimize chrome"
Jarvis: "Minimized chrome."

User: "set volume to 50"
Jarvis: "Volume set to 50 percent."

User: "list windows"
Jarvis: "Open windows: Notepad, Chrome, Calculator, VS Code"

User: "lock screen"
Jarvis: "Locking screen."

User: "system info"
Jarvis: "CPU: 25%, RAM: 40% (8GB/32GB), Disk: 60% used"
```

## Error Handling

- If a window cannot be found, Jarvis provides clear feedback
- System commands fail gracefully if requirements aren't met
- All new features are optional - existing functionality is preserved
- Missing dependencies are handled without breaking the assistant

## Notes

- Window operations require the application name to be partially visible in the window title
- Volume and brightness control use system keyboard shortcuts (may vary by hardware)
- System info requires psutil library
- All commands use voice input - no GUI modifications
- Lock screen and sleep functions work with Windows only
