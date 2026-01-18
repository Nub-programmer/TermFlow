from textual.app import ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Input, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message
from termflow.utils.todos import load_todos, add_todo, toggle_todo, delete_todo

class TodoItem(ListItem):
    """A single todo item widget."""

    def __init__(self, text: str, completed: bool, index: int) -> None:
        super().__init__()
        self.todo_text = text
        self.completed = completed
        self.index = index

    def compose(self) -> ComposeResult:
        icon = "✅" if self.completed else "⬜"
        style = "strike" if self.completed else ""
        yield Label(f"{icon} {self.todo_text}", classes=style)

class TodoPanel(Static):
    """A panel to manage To-Do items."""

    def compose(self) -> ComposeResult:
        yield Label("[bold]My Tasks[/bold]", classes="panel-header")
        yield Input(placeholder="Add a task...", id="todo-input")
        yield ListView(id="todo-list")
        yield Label("Enter: Add | Space: Toggle | Del: Remove", classes="help-text")

    def on_mount(self) -> None:
        self.refresh_todos()

    def refresh_todos(self) -> None:
        """Reloads todos from file and updates the list."""
        list_view = self.query_one("#todo-list", ListView)
        list_view.clear()
        
        todos = load_todos()
        for idx, todo in enumerate(todos):
            list_view.append(TodoItem(todo["text"], todo["completed"], idx))

    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle adding a new task."""
        if event.value.strip():
            add_todo(event.value.strip())
            event.input.value = ""
            self.refresh_todos()

    # Note: Textual's ListView doesn't inherently support key bindings on items 
    # easily without focus handling. We'll use the ListView's events.
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Toggle todo on selection (Enter key by default in ListView)."""
        # In a real app we might differentiate keys, but for now selection toggles.
        item = event.item
        if isinstance(item, TodoItem):
            toggle_todo(item.index)
            self.refresh_todos()
            
    def key_space(self) -> None:
        """Toggle selected item."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.highlighted_child:
            item = list_view.highlighted_child
            if isinstance(item, TodoItem):
                toggle_todo(item.index)
                self.refresh_todos()

    def key_delete(self) -> None:
        """Delete selected item."""
        list_view = self.query_one("#todo-list", ListView)
        if list_view.highlighted_child:
            item = list_view.highlighted_child
            if isinstance(item, TodoItem):
                delete_todo(item.index)
                self.refresh_todos()
