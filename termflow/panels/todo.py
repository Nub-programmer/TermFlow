from textual.widgets import Static, ListView, ListItem, Label, Input
from termflow.utils.storage import load_todos, save_todos
import re

class TodoPanel(Static):
    def compose(self):
        yield Label("[bold underline]TODO LIST[/]")
        yield Input(placeholder="New task... (use [tag] for colors)", id="todo-input")
        yield ListView(id="todo-list")

    def on_mount(self):
        self.refresh_list()

    def focus_input(self):
        self.query_one("#todo-input", Input).focus()

    def format_todo_text(self, text, done):
        # Color tags
        text = re.sub(r'\[school\]', '[bold light_blue][school][/]', text, flags=re.IGNORECASE)
        text = re.sub(r'\[dev\]', '[bold green][dev][/]', text, flags=re.IGNORECASE)
        text = re.sub(r'\[life\]', '[bold yellow][life][/]', text, flags=re.IGNORECASE)
        
        if done:
            # Dimmed text for completed items
            return f"[dim]{text}[/]"
        return text

    def refresh_list(self):
        lv = self.query_one(ListView)
        lv.clear()
        for t in load_todos():
            icon = "✅" if t['done'] else "⬜"
            formatted_text = self.format_todo_text(t['text'], t['done'])
            lv.append(ListItem(Label(f"{icon} {formatted_text}")))

    def on_input_submitted(self, event):
        if event.value.strip():
            todos = load_todos()
            todos.append({"text": event.value, "done": False})
            save_todos(todos)
            event.input.value = ""
            self.refresh_list()

    def on_list_view_selected(self, event: ListView.Selected):
        # Toggles completion on Enter or Click
        todos = load_todos()
        idx = self.query_one(ListView).index
        if idx is not None and 0 <= idx < len(todos):
            todos[idx]['done'] = not todos[idx]['done']
            save_todos(todos)
            self.refresh_list()

    def on_key(self, event):
        if event.key == "space":
            # Toggles completion on Space
            todos = load_todos()
            lv = self.query_one(ListView)
            idx = lv.index
            if idx is not None and 0 <= idx < len(todos):
                todos[idx]['done'] = not todos[idx]['done']
                save_todos(todos)
                self.refresh_list()
        elif event.key == "d":
            # Delete task
            todos = load_todos()
            lv = self.query_one(ListView)
            idx = lv.index
            if idx is not None and 0 <= idx < len(todos):
                todos.pop(idx)
                save_todos(todos)
                self.refresh_list()
