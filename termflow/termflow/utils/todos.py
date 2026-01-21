import json
import os
from typing import List, Dict

TODO_FILE = "todos.json"

def load_todos() -> List[Dict]:
    """Loads todos from the local JSON file."""
    if not os.path.exists(TODO_FILE):
        return []
    
    try:
        with open(TODO_FILE, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos: List[Dict]):
    """Saves todos to the local JSON file."""
    try:
        with open(TODO_FILE, "w") as f:
            json.dump(todos, f, indent=2)
    except IOError as e:
        print(f"Error saving todos: {e}")

def add_todo(text: str) -> List[Dict]:
    """Adds a new todo and returns the updated list."""
    todos = load_todos()
    todos.append({"text": text, "completed": False})
    save_todos(todos)
    return todos

def toggle_todo(index: int) -> List[Dict]:
    """Toggles the completion status of a todo."""
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["completed"] = not todos[index]["completed"]
        save_todos(todos)
    return todos

def delete_todo(index: int) -> List[Dict]:
    """Deletes a todo by index."""
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return todos
