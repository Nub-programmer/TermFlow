import json
from pathlib import Path
from termflow.utils.resources import get_user_data_dir

# Get user data directory
DATA_DIR = get_user_data_dir()

TODO_FILE = DATA_DIR / "todos.json"
CONFIG_FILE = DATA_DIR / "config.toml"
REFLECTIONS_FILE = DATA_DIR / "reflections.json"


def load_todos():
    if not TODO_FILE.exists():
        return []
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except:
        return []


def save_todos(todos):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f)


def load_config():
    if not CONFIG_FILE.exists():
        return {"pomodoro_duration": 25, "pomodoro_sessions_completed": 0}
    try:
        import tomllib
        with open(CONFIG_FILE, "rb") as f:
            return tomllib.load(f)
    except:
        return {"pomodoro_duration": 25, "pomodoro_sessions_completed": 0}


def save_config(config):
    try:
        import tomli_w
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(config, f)
    except:
        pass


def increment_pomodoro_session():
    config = load_config()
    sessions = config.get("pomodoro_sessions_completed", 0) + 1
    config["pomodoro_sessions_completed"] = sessions
    try:
        import tomli_w
        with open(CONFIG_FILE, "wb") as f:
            tomli_w.dump(config, f)
    except:
        pass
    return sessions
