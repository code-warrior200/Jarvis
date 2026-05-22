import os
import re
import json
import time
import random
import logging
import threading
import webbrowser
import subprocess
import shutil
import platform
from pathlib import Path
from datetime import datetime, timedelta
from urllib.parse import quote_plus

try:
    import pyttsx3  # type: ignore
except ImportError:
    pyttsx3 = None

try:
    import speech_recognition as sr
except ImportError:
    sr = None

try:
    import cv2
except ImportError:
    cv2 = None

try:
    import requests
except ImportError:
    requests = None

try:
    from llama_cpp import Llama # pyright: ignore[reportMissingImports]
except ImportError:
    Llama = None

try:
    from transformers import AutoTokenizer, AutoModelForCausalLM
except ImportError:
    AutoTokenizer = None
    AutoModelForCausalLM = None

try:
    import pygetwindow as gw # type: ignore
except ImportError:
    gw = None

try:
    import pyautogui # pyright: ignore[reportMissingModuleSource]
except ImportError:
    pyautogui = None

try:
    import psutil # pyright: ignore[reportMissingModuleSource]
except ImportError:
    psutil = None

DATA_FILE = Path(__file__).with_name('jarvis_data.json')


class LocalLLM:
    def __init__(self, model_path=None):
        self.model_path = model_path or os.getenv('JARVIS_LOCAL_MODEL_PATH')
        self.engine = None
        self.tokenizer = None
        self.model = None
        self.ready = False

        if Llama and self.model_path:
            try:
                self.engine = Llama(model_path=self.model_path)
                self.ready = True
            except Exception:
                self.engine = None

        if not self.ready and AutoTokenizer and AutoModelForCausalLM and self.model_path:
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(self.model_path, local_files_only=True)
                self.model = AutoModelForCausalLM.from_pretrained(self.model_path, local_files_only=True)
                self.ready = True
            except Exception:
                self.tokenizer = None
                self.model = None

    def generate(self, prompt, max_tokens=200):
        if self.ready and self.engine:
            try:
                response = self.engine.complete(prompt=prompt, max_tokens=max_tokens)
                return response['choices'][0]['text'].strip()
            except Exception:
                return self.fallback(prompt)

        if self.ready and self.tokenizer and self.model:
            try:
                encoded = self.tokenizer(prompt, return_tensors='pt')
                outputs = self.model.generate(**encoded, max_new_tokens=max_tokens)
                return self.tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
            except Exception:
                return self.fallback(prompt)

        return self.fallback(prompt)

    @staticmethod
    def fallback(prompt):
        prompt = prompt.lower()
        if 'weather' in prompt:
            return 'Ask me about weather in a city, for example: "weather in London".'
        if 'calendar' in prompt or 'event' in prompt:
            return 'I can add or list calendar events for you.'
        if 'reminder' in prompt or 'remind' in prompt:
            return 'Tell me what to remind you about and when.'
        if 'open' in prompt or 'launch' in prompt:
            return 'I can open apps like Notepad, Calculator, Chrome, or VS Code.'
        if 'search' in prompt or 'web' in prompt:
            return 'I can search the web and open it in your browser.'
        if 'face' in prompt or 'camera' in prompt:
            return 'I can run face detection if OpenCV is installed.'
        return 'I am ready. Say "help" to see the commands I support.'


class WindowManager:
    """Manages window operations like minimize, maximize, close, resize, focus."""
    
    @staticmethod
    def find_window(app_name):
        """Find a window by app name (case-insensitive partial match)."""
        if not gw:
            return None
        try:
            windows = gw.getAllWindows()
            app_lower = app_name.lower()
            for window in windows:
                if app_lower in window.title.lower():
                    return window
        except Exception:
            pass
        return None
    
    @staticmethod
    def list_windows():
        """List all open windows."""
        if not gw:
            return []
        try:
            return [w.title for w in gw.getAllWindows() if w.title.strip()]
        except Exception:
            return []
    
    @staticmethod
    def minimize(app_name):
        """Minimize a window by app name."""
        window = WindowManager.find_window(app_name)
        if window:
            try:
                window.minimize()
                return True
            except Exception:
                pass
        return False
    
    @staticmethod
    def maximize(app_name):
        """Maximize a window by app name."""
        window = WindowManager.find_window(app_name)
        if window:
            try:
                window.maximize()
                return True
            except Exception:
                pass
        return False
    
    @staticmethod
    def close(app_name):
        """Close a window by app name."""
        window = WindowManager.find_window(app_name)
        if window:
            try:
                window.close()
                return True
            except Exception:
                pass
        return False
    
    @staticmethod
    def focus(app_name):
        """Bring a window to foreground by app name."""
        window = WindowManager.find_window(app_name)
        if window:
            try:
                window.activate()
                return True
            except Exception:
                pass
        return False
    
    @staticmethod
    def resize(app_name, width, height):
        """Resize a window by app name."""
        window = WindowManager.find_window(app_name)
        if window:
            try:
                window.width = width
                window.height = height
                return True
            except Exception:
                pass
        return False


class SystemControl:
    """Controls system-level features like volume, brightness, and system info."""
    
    @staticmethod
    def set_volume(level):
        """Set volume to a percentage (0-100). Windows only."""
        if not pyautogui:
            return False
        try:
            level = max(0, min(100, int(level)))
            steps = level // 10
            pyautogui.press('volumemute')
            time.sleep(0.1)
            for _ in range(steps):
                pyautogui.press('volumeup')
                time.sleep(0.05)
            return True
        except Exception:
            return False
    
    @staticmethod
    def volume_up():
        """Increase volume."""
        if not pyautogui:
            return False
        try:
            pyautogui.press('volumeup')
            return True
        except Exception:
            return False
    
    @staticmethod
    def volume_down():
        """Decrease volume."""
        if not pyautogui:
            return False
        try:
            pyautogui.press('volumedown')
            return True
        except Exception:
            return False
    
    @staticmethod
    def set_brightness(level):
        """Set brightness (0-100). Works on Windows with compatible hardware."""
        if not pyautogui:
            return False
        try:
            level = max(0, min(100, int(level)))
            steps = (level - 50) // 10
            if steps > 0:
                for _ in range(abs(steps)):
                    pyautogui.press('brightnessup')
                    time.sleep(0.05)
            elif steps < 0:
                for _ in range(abs(steps)):
                    pyautogui.press('brightnessdown')
                    time.sleep(0.05)
            return True
        except Exception:
            return False
    
    @staticmethod
    def brightness_up():
        """Increase brightness."""
        if not pyautogui:
            return False
        try:
            pyautogui.press('brightnessup')
            return True
        except Exception:
            return False
    
    @staticmethod
    def brightness_down():
        """Decrease brightness."""
        if not pyautogui:
            return False
        try:
            pyautogui.press('brightnessdown')
            return True
        except Exception:
            return False
    
    @staticmethod
    def lock_screen():
        """Lock the Windows screen."""
        try:
            subprocess.Popen(['rundll32.exe', 'user32.dll,LockWorkStation'])
            return True
        except Exception:
            return False
    
    @staticmethod
    def sleep():
        """Put system to sleep."""
        try:
            os.system('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return True
        except Exception:
            return False
    
    @staticmethod
    def system_info():
        """Get system information."""
        if not psutil:
            return 'System info requires psutil.'
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            ram = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            info = (
                f"CPU: {cpu_percent}%, "
                f"RAM: {ram.percent}% ({ram.used // (1024**3)}GB/{ram.total // (1024**3)}GB), "
                f"Disk: {disk.percent}% used"
            )
            return info
        except Exception:
            return 'Could not retrieve system information.'


class Jarvis:
    def __init__(self):
        self.voice_enabled = bool(pyttsx3)
        self.recognizer = sr.Recognizer() if sr else None
        self.microphone_available = False
        self.user_name = None
        if self.recognizer and sr:
            try:
                with sr.Microphone() as source:
                    pass
                self.microphone_available = True
            except Exception as e:
                logging.warning('Microphone unavailable: %s', e)

        self.llm = LocalLLM()
        self.data = self.load_data()
        self.reminder_thread = threading.Thread(target=self.reminder_worker, daemon=True)
        self.reminder_thread.start()
        self.commands = {
            'help': self.show_help,
            'weather': self.weather_command,
            'calendar': self.calendar_command,
            'reminder': self.reminder_command,
            'open': self.open_app,
            'launch': self.open_app,
            'search': self.search_web,
            'web': self.search_web,
            'face': self.face_command,
            'camera': self.face_command,
            'minimize': self.minimize_app,
            'maximize': self.maximize_app,
            'close': self.close_app,
            'focus': self.focus_app,
            'windows': self.list_open_windows,
            'volume': self.volume_command,
            'brightness': self.brightness_command,
            'lock': self.lock_screen_command,
            'sleep': self.sleep_command,
            'system': self.system_info_command,
        }

    def load_data(self):
        if DATA_FILE.exists():
            try:
                return json.loads(DATA_FILE.read_text())
            except Exception:
                return {'events': [], 'reminders': []}
        return {'events': [], 'reminders': []}

    def save_data(self):
        DATA_FILE.write_text(json.dumps(self.data, indent=2))

    def speak(self, text):
        print('Jarvis:', text)
        if self.voice_enabled:
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
            except Exception:
                pass

    def listen(self):
        if not self.recognizer or not sr:
            self.speak('Voice-only mode requires SpeechRecognition and a microphone. Exiting.')
            raise SystemExit

        try:
            with sr.Microphone() as source:
                self.speak('Listening now.')
                self.recognizer.adjust_for_ambient_noise(source, duration=0.8)
                audio = self.recognizer.listen(source, timeout=8, phrase_time_limit=10)

            if hasattr(self.recognizer, 'recognize_sphinx'):
                try:
                    return self.recognizer.recognize_sphinx(audio)
                except Exception:
                    pass
            return self.recognizer.recognize_google(audio)

        except sr.WaitTimeoutError:
            self.speak('I did not hear anything. Please try again.')
        except sr.UnknownValueError:
            self.speak('I could not understand you. Please try again.')
        except Exception as e:
            self.speak(f'Voice recognition failed: {e}')
        return ''

    def parse_datetime(self, text):
        now = datetime.now()
        text = text.lower().strip()
        if 'in ' in text:
            match = re.search(r'in (\d+) (minute|minutes|hour|hours|day|days)', text)
            if match:
                value = int(match.group(1))
                unit = match.group(2)
                if 'minute' in unit:
                    return now + timedelta(minutes=value)
                if 'hour' in unit:
                    return now + timedelta(hours=value)
                if 'day' in unit:
                    return now + timedelta(days=value)
        if 'tomorrow' in text:
            time_match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
            due = now + timedelta(days=1)
            if time_match:
                hour = int(time_match.group(1))
                minute = int(time_match.group(2) or 0)
                ampm = time_match.group(3)
                if ampm == 'pm' and hour < 12:
                    hour += 12
                if ampm == 'am' and hour == 12:
                    hour = 0
                return due.replace(hour=hour, minute=minute, second=0, microsecond=0)
            return due.replace(hour=9, minute=0, second=0, microsecond=0)
        date_match = re.search(r'(\d{4}-\d{1,2}-\d{1,2})', text)
        time_match = re.search(r'at (\d{1,2})(?::(\d{2}))?\s*(am|pm)?', text)
        if date_match:
            date_str = date_match.group(1)
            try:
                dt = datetime.fromisoformat(date_str)
                if time_match:
                    hour = int(time_match.group(1))
                    minute = int(time_match.group(2) or 0)
                    ampm = time_match.group(3)
                    if ampm == 'pm' and hour < 12:
                        hour += 12
                    if ampm == 'am' and hour == 12:
                        hour = 0
                    dt = dt.replace(hour=hour, minute=minute, second=0, microsecond=0)
                return dt
            except ValueError:
                pass
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2) or 0)
            ampm = time_match.group(3)
            if ampm == 'pm' and hour < 12:
                hour += 12
            if ampm == 'am' and hour == 12:
                hour = 0
            return now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        return None

    def reminder_worker(self):
        while True:
            now = datetime.now()
            changed = False
            for reminder in list(self.data.get('reminders', [])):
                due = datetime.fromisoformat(reminder['time'])
                if now >= due and not reminder.get('shown'):
                    self.speak(f"Reminder: {reminder['text']}")
                    reminder['shown'] = True
                    changed = True
            if changed:
                self.save_data()
            time.sleep(30)

    def show_help(self, _=None):
        message = (
            'I can help with these commands:\n'
            '- weather in <city>\n'
            '- add calendar event <title> on <YYYY-MM-DD> at <HH:MM>\n'
            '- list calendar events\n'
            '- remind me to <task> in <minutes/hours/days>\n'
            '- open notepad / chrome / edge / code / calculator\n'
            '- search for <query>\n'
            '- face recognition\n'
            '- minimize / maximize / close / focus <app name>\n'
            '- list windows\n'
            '- volume up / down / set to <number>\n'
            '- brightness up / down / set to <number>\n'
            '- lock screen\n'
            '- sleep\n'
            '- system info\n'
            '- tell me a joke\n'
            '- what time is it\n'
            '- what is the date\n'
            '- how are you\n'
            '- help\n'
            'You can also speak freely and I will do my best to understand and help.\n'
        )
        self.speak(message)

    def tell_joke(self, _=None):
        jokes = [
            'Why did the computer show up at work late? It had a hard drive.',
            'Why do programmers prefer dark mode? Because light attracts bugs.',
            'Why was the cell phone wearing glasses? Because it lost its contacts.',
        ]
        self.speak(random.choice(jokes))

    def say_time(self, _=None):
        self.speak(f'The time is {datetime.now().strftime("%I:%M %p")}.')

    def say_date(self, _=None):
        self.speak(f'Today is {datetime.now().strftime("%A, %B %d, %Y")}.')

    def small_talk(self, text):
        if 'how are you' in text or 'how do you feel' in text:
            self.speak('I am doing great, thanks for asking. I am ready to help you.')
        elif 'who are you' in text or 'what is your name' in text:
            self.speak('I am Jarvis, your personal assistant.')
        elif 'thank you' in text or 'thanks' in text:
            self.speak('You are welcome. Happy to help.')
        else:
            self.speak('I am here and listening.')

    def geocode_location(self, location):
        if not requests:
            return None
        url = 'https://geocoding-api.open-meteo.com/v1/search'
        params = {'name': location, 'count': 1}
        try:
            response = requests.get(url, params=params, timeout=10)
            result = response.json()
            if result.get('results'):
                return result['results'][0]
        except Exception:
            pass
        return None

    def weather_command(self, text=None):
        if not requests:
            self.speak('Weather requires the requests package. Install it and try again.')
            return
        if not text:
            self.speak('Which city weather do you want?')
            text = self.listen()
        location = text.replace('weather', '').strip() or text.strip()
        place = self.geocode_location(location)
        if not place:
            self.speak('Could not find that location.')
            return
        lat, lon = place['latitude'], place['longitude']
        try:
            url = f'https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true&timezone=auto'
            data = requests.get(url, timeout=10).json()
            current = data.get('current_weather', {})
            if current:
                self.speak(f"Weather in {place['name']}: {current['temperature']} degrees C, wind {current['windspeed']} km/h.")
                return
        except Exception:
            pass
        self.speak('Unable to retrieve weather right now.')

    def calendar_command(self, text=None):
        if not text:
            self.speak('What would you like to do with your calendar?')
            text = self.listen()
        if 'list' in text or 'show' in text:
            events = self.data.get('events', [])
            if not events:
                self.speak('Your calendar is empty.')
                return
            lines = ['Your calendar events:'] + [f"{item['time']} - {item['title']}" for item in events]
            self.speak('\n'.join(lines))
            return
        title_match = re.search(r'add calendar event (.+?) on (\d{4}-\d{1,2}-\d{1,2})(?: at (\d{1,2}(?::\d{2})?\s*(?:am|pm)?))?', text)
        if title_match:
            title = title_match.group(1).strip()
            date_text = title_match.group(2)
            time_text = title_match.group(3) or '09:00'
            dt = self.parse_datetime(f'{date_text} at {time_text}')
            if dt:
                self.data['events'].append({'title': title, 'time': dt.isoformat()})
                self.save_data()
                self.speak(f'Added event {title} on {dt.strftime("%Y-%m-%d %H:%M")}.')
                return
        self.speak('Please say: add calendar event <title> on YYYY-MM-DD at HH:MM.')

    def reminder_command(self, text=None):
        if not text:
            self.speak('What should I remind you about?')
            text = self.listen()
        if 'remind me to' in text:
            parts = text.split('remind me to', 1)[1].strip()
            dt = self.parse_datetime(parts)
            if not dt:
                self.speak('When should I remind you? You can say "in 10 minutes" or "tomorrow at 9am".')
                parts = self.listen()
                dt = self.parse_datetime(parts)
            if dt:
                self.data['reminders'].append({'text': parts, 'time': dt.isoformat(), 'shown': False})
                self.save_data()
                self.speak(f'Reminder set for {dt.strftime("%Y-%m-%d %H:%M")}.')
                return
        self.speak('Please say: remind me to <task> in <minutes/hours/days>.')

    def open_app(self, text=None):
        if not text:
            self.speak('Which app do you want to open?')
            text = self.listen()
        target = text.lower().strip()
        for prefix in ('open ', 'launch ', 'start ', 'run ', 'please open ', 'please launch ', 'please start ', 'please run '):
            if target.startswith(prefix):
                target = target[len(prefix):].strip()
                break

        if not target:
            self.speak('I did not catch the app name. Please say the app you want to open.')
            return

        known_apps = {
            'notepad': ['notepad.exe'],
            'calculator': ['calc.exe'],
            'chrome': ['chrome.exe', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'],
            'edge': ['msedge.exe'],
            'code': ['code.cmd', 'code.exe'],
            'vscode': ['code.cmd', 'code.exe'],
            'word': ['winword.exe'],
            'excel': ['excel.exe'],
            'powerpoint': ['powerpnt.exe'],
            'paint': ['mspaint.exe'],
            'terminal': ['wt.exe'],
            'windows terminal': ['wt.exe'],
        }

        for key, commands in known_apps.items():
            if key in target:
                for cmd in commands:
                    try:
                        subprocess.Popen([cmd])
                        self.speak(f'Opening {key}.')
                        return
                    except Exception:
                        continue

        if os.path.exists(target) or target.endswith('.exe'):
            try:
                if os.path.exists(target):
                    os.startfile(target)
                else:
                    subprocess.Popen([target])
                self.speak(f'Opening {target}.')
                return
            except Exception:
                pass

        candidate = shutil.which(target)
        if not candidate and not target.endswith('.exe'):
            candidate = shutil.which(target + '.exe')
        if candidate:
            try:
                subprocess.Popen([candidate])
                self.speak(f'Opening {target}.')
                return
            except Exception:
                pass

        try:
            subprocess.Popen(f'start "" "{target}"', shell=True)
            self.speak(f'Attempting to open {target}.')
            return
        except Exception:
            pass

        self.speak('I could not open that app. Try using its exact executable name or full path.')
    def search_web(self, text=None):
        if not text:
            self.speak('What should I search for?')
            text = self.listen()
        query = text.replace('search', '').replace('web', '').strip() or text.strip()
        if not query:
            self.speak('Search query is empty.')
            return
        url = f'https://www.google.com/search?q={quote_plus(query)}'
        webbrowser.open(url)
        self.speak(f'Searching the web for {query}.')

    def face_command(self, _=None):
        if not cv2:
            self.speak('Face recognition requires OpenCV. Install opencv-python and try again.')
            return
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            self.speak('Cannot open camera.')
            return
        self.speak('Starting face detection. Press Q to stop.')
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.imshow('Jarvis Face Recognition', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        self.speak(f'Detected {len(faces)} face(s).')

    def minimize_app(self, text=None):
        if not text:
            self.speak('Which app should I minimize?')
            text = self.listen()
        app_name = text.replace('minimize', '').strip()
        if not app_name:
            self.speak('Please specify an app name.')
            return
        if WindowManager.minimize(app_name):
            self.speak(f'Minimized {app_name}.')
        else:
            self.speak(f'Could not find or minimize {app_name}.')

    def maximize_app(self, text=None):
        if not text:
            self.speak('Which app should I maximize?')
            text = self.listen()
        app_name = text.replace('maximize', '').strip()
        if not app_name:
            self.speak('Please specify an app name.')
            return
        if WindowManager.maximize(app_name):
            self.speak(f'Maximized {app_name}.')
        else:
            self.speak(f'Could not find or maximize {app_name}.')

    def close_app(self, text=None):
        if not text:
            self.speak('Which app should I close?')
            text = self.listen()
        app_name = text.replace('close', '').strip()
        if not app_name:
            self.speak('Please specify an app name.')
            return
        if WindowManager.close(app_name):
            self.speak(f'Closed {app_name}.')
        else:
            self.speak(f'Could not find or close {app_name}.')

    def focus_app(self, text=None):
        if not text:
            self.speak('Which app should I focus?')
            text = self.listen()
        app_name = text.replace('focus', '').strip()
        if not app_name:
            self.speak('Please specify an app name.')
            return
        if WindowManager.focus(app_name):
            self.speak(f'Focused {app_name}.')
        else:
            self.speak(f'Could not find or focus {app_name}.')

    def list_open_windows(self, _=None):
        windows = WindowManager.list_windows()
        if not windows:
            self.speak('No windows found.')
            return
        window_list = ', '.join(windows[:10])
        if len(windows) > 10:
            self.speak(f'You have many windows open. Here are the first 10: {window_list}')
        else:
            self.speak(f'Open windows: {window_list}')

    def volume_command(self, text=None):
        if not text:
            self.speak('What would you like to do with volume? Say up, down, or set to a number.')
            text = self.listen()
        text = text.lower()
        if 'up' in text:
            if SystemControl.volume_up():
                self.speak('Volume increased.')
            else:
                self.speak('Could not adjust volume.')
        elif 'down' in text:
            if SystemControl.volume_down():
                self.speak('Volume decreased.')
            else:
                self.speak('Could not adjust volume.')
        else:
            match = re.search(r'(\d+)', text)
            if match:
                level = int(match.group(1))
                if SystemControl.set_volume(level):
                    self.speak(f'Volume set to {level} percent.')
                else:
                    self.speak('Could not set volume.')

    def brightness_command(self, text=None):
        if not text:
            self.speak('What would you like to do with brightness? Say up, down, or set to a number.')
            text = self.listen()
        text = text.lower()
        if 'up' in text:
            if SystemControl.brightness_up():
                self.speak('Brightness increased.')
            else:
                self.speak('Could not adjust brightness.')
        elif 'down' in text:
            if SystemControl.brightness_down():
                self.speak('Brightness decreased.')
            else:
                self.speak('Could not adjust brightness.')
        else:
            match = re.search(r'(\d+)', text)
            if match:
                level = int(match.group(1))
                if SystemControl.set_brightness(level):
                    self.speak(f'Brightness set to {level} percent.')
                else:
                    self.speak('Could not set brightness.')

    def lock_screen_command(self, _=None):
        if SystemControl.lock_screen():
            self.speak('Locking screen.')
        else:
            self.speak('Could not lock screen.')

    def sleep_command(self, _=None):
        self.speak('Putting system to sleep.')
        time.sleep(1)
        SystemControl.sleep()

    def system_info_command(self, _=None):
        info = SystemControl.system_info()
        self.speak(info)

    def handle_command(self, text):
        normalized = text.lower().strip()
        if normalized in ('exit', 'quit', 'stop', 'bye'):
            self.speak('Goodbye.')
            raise SystemExit
        if 'my name is ' in normalized:
            name = normalized.split('my name is ', 1)[1].strip().split()[0]
            self.user_name = name.title()
            return self.speak(f'Nice to meet you, {self.user_name}.')
        if 'what is my name' in normalized or "what's my name" in normalized:
            if self.user_name:
                return self.speak(f'Your name is {self.user_name}.')
            return self.speak('I do not know your name yet. Tell me by saying my name is followed by your name.')
        if 'joke' in normalized:
            return self.tell_joke()
        if 'time' in normalized and 'date' not in normalized:
            return self.say_time()
        if 'date' in normalized:
            return self.say_date()
        if 'how are you' in normalized or 'who are you' in normalized or 'what is your name' in normalized:
            return self.small_talk(normalized)
        if 'thank you' in normalized or 'thanks' in normalized:
            return self.small_talk(normalized)
        if 'what can you do' in normalized or 'what are your capabilities' in normalized:
            return self.show_help()

        if any(keyword in normalized for keyword in ('weather', 'temperature', 'forecast')):
            return self.weather_command(normalized)
        if any(keyword in normalized for keyword in ('calendar', 'event', 'meeting', 'schedule')):
            return self.calendar_command(normalized)
        if any(keyword in normalized for keyword in ('remind', 'reminder', 'remember')):
            return self.reminder_command(normalized)
        if any(keyword in normalized for keyword in ('open', 'launch', 'start', 'run')):
            return self.open_app(normalized)
        if any(keyword in normalized for keyword in ('search', 'google', 'find', 'look up')):
            return self.search_web(normalized)
        if any(keyword in normalized for keyword in ('face', 'camera', 'detect', 'recognition')):
            return self.face_command(normalized)
        if any(keyword in normalized for keyword in ('minimize', 'minify')):
            return self.minimize_app(normalized)
        if any(keyword in normalized for keyword in ('maximize', 'maxify')):
            return self.maximize_app(normalized)
        if any(keyword in normalized for keyword in ('close', 'shut')):
            return self.close_app(normalized)
        if any(keyword in normalized for keyword in ('focus', 'bring', 'switch')):
            return self.focus_app(normalized)
        if any(keyword in normalized for keyword in ('list windows', 'show windows', 'open windows')):
            return self.list_open_windows(normalized)
        if any(keyword in normalized for keyword in ('volume', 'sound')):
            return self.volume_command(normalized)
        if any(keyword in normalized for keyword in ('brightness', 'screen brightness')):
            return self.brightness_command(normalized)
        if any(keyword in normalized for keyword in ('lock', 'lock screen', 'lock computer')):
            return self.lock_screen_command(normalized)
        if any(keyword in normalized for keyword in ('sleep', 'hibernate')):
            return self.sleep_command(normalized)
        if any(keyword in normalized for keyword in ('system info', 'system status', 'system information')):
            return self.system_info_command(normalized)

        return self.handle_generic_request(text)

    def handle_generic_request(self, text):
        if self.llm.ready:
            self.speak('Let me think about that.')
            answer = self.llm.generate(
                f'You are a helpful assistant named Jarvis. The user said: "{text}". Respond as helpfully as possible.'
            )
            self.speak(answer)
            return

        fallback_answer = LocalLLM.fallback(text)
        if fallback_answer:
            self.speak(fallback_answer)
            return

        self.speak('I am not sure how to do exactly that yet, but I can still answer questions or help with weather, calendar, reminders, app launch, and face recognition.')

    def run(self):
        if not self.microphone_available:
            self.speak('Voice-only mode requires a working microphone. Please connect one and restart Jarvis.')
            return

        self.speak('Hello, I am Jarvis. Say help for a list of commands.')
        while True:
            command = self.listen()
            if not command:
                continue
            try:
                self.handle_command(command)
                self.speak('What else can I do for you?')
            except SystemExit:
                break
            except Exception as e:
                logging.exception('Unhandled error in handle_command: %s', e)
                self.speak(f'An error occurred: {e}')


if __name__ == '__main__':
    jarvis = Jarvis()
    jarvis.run()

