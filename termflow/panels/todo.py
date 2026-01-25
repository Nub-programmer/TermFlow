from textual.widgets import Static, ListView, ListItem, Label, Input
from termflow.utils.storage import load_todos, save_todos
import re

class TodoPanel(Static):
    def compose(self):
        yield Label("[bold green]Orientation[/]", classes="panel-header")
        yield Input(placeholder="Add intention...", id="todo-input")
        yield ListView(id="todo-list")

    def on_mount(self):
        self.refresh_list()

    def focus_input(self):
        self.query_one("#todo-input", Input).focus()

    def format_todo_text(self, text, done):
        if done:
            return f"[dim]{text}[/]"
        return text

    def refresh_list(self):
        lv = self.query_one("#todo-list", ListView)
        lv.clear()
        for t in load_todos():
            is_done = t.get('done') or t.get('completed', False)
            icon = "✅" if is_done else "⬜"
            formatted_text = self.format_todo_text(t['text'], is_done)
            item = ListItem(Label(f"{icon} {formatted_text}"))
            if is_done:
                item.add_class("completed")
            lv.append(item)

    def on_input_submitted(self, event):
        if self.app.flow_state == "DEEP":
            return
        if event.value.strip():
            todos = load_todos()
            todos.append({"text": event.value, "done": False})
            save_todos(todos)
            event.input.value = ""
            self.refresh_list()

    def on_list_view_selected(self, event: ListView.Selected):
        if self.app.flow_state == "DEEP":
            return
        todos = load_todos()
        idx = self.query_one("#todo-list", ListView).index
        if idx is not None and 0 <= idx < len(todos):
            todos[idx]['done'] = not todos[idx].get('done', False)
            save_todos(todos)
            self.refresh_list()

    def on_key(self, event):
        if self.app.flow_state == "DEEP":
            return
        if event.key == "space":
            todos = load_todos()
            lv = self.query_one("#todo-list", ListView)
            idx = lv.index
            if idx is not None and 0 <= idx < len(todos):
                todos[idx]['done'] = not todos[idx].get('done', False)
                save_todos(todos)
                self.refresh_list()
                event.stop()
        elif event.key == "d":
            todos = load_todos()
            lv = self.query_one("#todo-list", ListView)
            idx = lv.index
            if idx is not None and 0 <= idx < len(todos):
                todos.pop(idx)
                save_todos(todos)
                self.refresh_list()
                event.stop()
