from textual.widgets import Static, ListView, ListItem, Label, Input
from termflow.utils.storage import load_todos, save_todos
import re

class TodoPanel(Static):
    def compose(self):
        yield Label("[bold underline]TODO LIST[/]")
        yield Input(placeholder="New task... (use [tag] for colors)")
        yield ListView(id="todo-list")

    def on_mount(self):
        self.refresh_list()

    def format_todo_text(self, text):
        # Support simple tags like [school], [dev], [life]
        # [school] -> light_blue, [dev] -> green, [life] -> yellow
        text = re.sub(r'\[school\]', '[bold light_blue][school][/]', text, flags=re.IGNORECASE)
        text = re.sub(r'\[dev\]', '[bold green][dev][/]', text, flags=re.IGNORECASE)
        text = re.sub(r'\[life\]', '[bold yellow][life][/]', text, flags=re.IGNORECASE)
        return text

    def refresh_list(self):
        lv = self.query_one(ListView)
        lv.clear()
        for i, t in enumerate(load_todos()):
            icon = "✅" if t['done'] else "⬜"
            formatted_text = self.format_todo_text(t['text'])
            lv.append(ListItem(Label(f"{icon} {formatted_text}")))

    def on_input_submitted(self, event):
        if event.value.strip():
            todos = load_todos()
            todos.append({"text": event.value, "done": False})
            save_todos(todos)
            event.input.value = ""
            self.refresh_list()

    def on_list_view_selected(self, event):
        todos = load_todos()
        idx = event.list_view.index
        if 0 <= idx < len(todos):
            todos[idx]['done'] = not todos[idx]['done']
            save_todos(todos)
            self.refresh_list()
