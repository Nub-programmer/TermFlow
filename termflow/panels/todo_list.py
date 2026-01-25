from textual.app import ComposeResult
from textual.widgets import Static, ListView, ListItem, Label, Input, Button
from textual.containers import Vertical, Horizontal
from textual.message import Message
from termflow.utils.todos import add_todo, toggle_todo, delete_todo

class TodoItem(ListItem):
    """A single todo item widget."""

    def __init__(self, text: str, completed: bool, index: int) -> None:
        super().__init__()
        self.todo_text = text
        self.completed = completed
        self.index = index

    def compose(self) -> ComposeResult:
        icon = "✅" if self.completed else "⬜"
        if self.completed:
            yield Label(f"[dim strike]{icon} {self.todo_text}[/]")
        else:
            yield Label(f"[bold]{icon} {self.todo_text}[/]")

class TodoPanel(Static):
    """A panel to manage To-Do items."""
    can_focus = False

    def compose(self) -> ComposeResult:
        yield Label("[bold]My Tasks[/bold]", classes="panel-header")
        yield Input(placeholder="Add a task...", id="todo-input")
        yield ListView(id="todo-list")
        yield Label("Enter: Add | Space: Toggle | Del: Remove", classes="help-text")

    def focus_input(self) -> None:
        """Focus the input field for adding new tasks."""
        try:
            input_widget = self.query_one("#todo-input")
            input_widget.focus()
        except:
            pass

    def on_mount(self) -> None:
        self.refresh_todos()

    def refresh_todos(self) -> None:
        """Reloads todos from file and updates the list."""
        list_view = self.query_one("#todo-list", ListView)
        list_view.clear()
        
        from termflow.utils.todos import load_todos
        todos = load_todos()
        for idx, todo in enumerate(todos):
            # Safe access with multi-key support and graceful fallback
            if not isinstance(todo, dict):
                continue
                
            text = todo.get("text", todo.get("task", "Untitled"))
            # Standardize on 'done' internally while supporting 'completed'
            done = todo.get("done", todo.get("completed", False))
            
            list_view.append(TodoItem(text, done, idx))

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
        if self.app.flow_state == "DEEP":
            return
        item = event.item
        if isinstance(item, TodoItem):
            toggle_todo(item.index)
            self.refresh_todos()
            
    def key_space(self) -> None:
        """Toggle selected item."""
        if self.app.flow_state == "DEEP":
            return
        list_view = self.query_one("#todo-list", ListView)
        if list_view.highlighted_child:
            item = list_view.highlighted_child
            if isinstance(item, TodoItem):
                toggle_todo(item.index)
                self.refresh_todos()

    def key_delete(self) -> None:
        """Delete selected item."""
        if self.app.flow_state == "DEEP":
            return
        list_view = self.query_one("#todo-list", ListView)
        if list_view.highlighted_child:
            item = list_view.highlighted_child
            if isinstance(item, TodoItem):
                delete_todo(item.index)
                self.refresh_todos()
