import json
from datetime import datetime
from pathlib import Path
import platformdirs

APP_NAME = "termflow"

# Data paths following XDG specs
DATA_DIR = Path(platformdirs.user_data_dir(APP_NAME))
CONFIG_DIR = Path(platformdirs.user_config_dir(APP_NAME))

TODO_FILE = DATA_DIR / "todos.json"
CONFIG_FILE = CONFIG_DIR / "config.toml"

DEFAULT_CONFIG = {
    "city": "New York",
    "pomodoro_duration": 25,
    "theme": "dark"
}

def ensure_dirs():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)

def load_todos():
    ensure_dirs()
    if not TODO_FILE.exists():
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_todos(todos):
    ensure_dirs()
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def load_config():
    ensure_dirs()
    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG
    
    try:
        import tomllib as toml # Python 3.11+
    except ImportError:
        try:
            import tomli as toml # type: ignore
        except ImportError:
            return DEFAULT_CONFIG
        
    try:
        with open(CONFIG_FILE, "rb") as f:
            config = toml.load(f)
            # Merge with defaults
            merged = DEFAULT_CONFIG.copy()
            merged.update(config)
            return merged
    except:
        return DEFAULT_CONFIG

def save_config(config):
    ensure_dirs()
    try:
        import tomli_w as tomlw
        with open(CONFIG_FILE, "wb") as f:
            tomlw.dump(config, f)
    except:
        pass

def get_session_data():
    ensure_dirs()
    session_file = DATA_DIR / "sessions.json"
    if not session_file.exists():
        return {"completed": 0, "last_date": ""}
    try:
        with open(session_file, "r") as f:
            return json.load(f)
    except:
        return {"completed": 0, "last_date": ""}

def increment_pomodoro_session():
    data = get_session_data()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if data.get("last_date") != today:
        data["completed"] = 1
        data["last_date"] = today
    else:
        data["completed"] += 1
    
    session_file = DATA_DIR / "sessions.json"
    with open(session_file, "w") as f:
        json.dump(data, f)
    return data["completed"]
