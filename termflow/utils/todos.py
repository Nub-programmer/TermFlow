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
            data = json.load(f)
            # Ensure data is a list of dicts
            if not isinstance(data, list):
                return []
            return data
    except (json.JSONDecodeError, IOError):
        return []

def save_todos(todos: List[Dict]):
    """Saves todos to the local JSON file."""
    try:
        # Cleanup before saving to maintain consistency
        clean_todos = []
        for todo in todos:
            if isinstance(todo, dict):
                # Ensure we use 'done' as the standard key
                done = todo.get("done", todo.get("completed", False))
                text = todo.get("text", "Untitled")
                clean_todos.append({"text": text, "done": done})
        
        with open(TODO_FILE, "w") as f:
            json.dump(clean_todos, f, indent=2)
    except IOError as e:
        print(f"Error saving todos: {e}")

def add_todo(text: str) -> List[Dict]:
    """Adds a new todo and returns the updated list."""
    todos = load_todos()
    todos.append({"text": text, "done": False})
    save_todos(todos)
    return todos

def toggle_todo(index: int) -> List[Dict]:
    """Toggles the completion status of a todo."""
    todos = load_todos()
    if 0 <= index < len(todos):
        todo = todos[index]
        # Support both keys during toggle
        current_status = todo.get("done", todo.get("completed", False))
        todo["done"] = not current_status
        # Clean up legacy key if present
        if "completed" in todo:
            del todo["completed"]
        save_todos(todos)
    return todos

def delete_todo(index: int) -> List[Dict]:
    """Deletes a todo by index."""
    todos = load_todos()
    if 0 <= index < len(todos):
        todos.pop(index)
        save_todos(todos)
    return todos
