import os
import json
from pathlib import Path

# Use local data directory for Replit compatibility
DATA_DIR = Path("termflow/termflow/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

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
    return {}
