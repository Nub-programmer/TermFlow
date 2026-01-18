import json
import os
from datetime import datetime

TODO_FILE = "todos.json"
CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "city": "New York",
    "pomodoro_duration": 25,
    "pomodoro_sessions_completed": 0,
    "last_session_date": ""
}

def load_todos():
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=2)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return DEFAULT_CONFIG
    try:
        with open(CONFIG_FILE, "r") as f:
            config = json.load(f)
            # Ensure all keys exist
            for key, value in DEFAULT_CONFIG.items():
                if key not in config:
                    config[key] = value
            return config
    except:
        return DEFAULT_CONFIG

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def increment_pomodoro_session():
    config = load_config()
    today = datetime.now().strftime("%Y-%m-%d")
    
    if config.get("last_session_date") != today:
        config["pomodoro_sessions_completed"] = 1
        config["last_session_date"] = today
    else:
        config["pomodoro_sessions_completed"] = config.get("pomodoro_sessions_completed", 0) + 1
    
    save_config(config)
    return config["pomodoro_sessions_completed"]
