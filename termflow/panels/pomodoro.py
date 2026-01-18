from textual.widgets import Static, Button, Label
from textual.reactive import reactive
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from textual.app import ComposeResult

class PomodoroPanel(Static):
    time_left: reactive[int] = reactive(25 * 60)
    is_running: reactive[bool] = reactive(False)

    def compose(self) -> "ComposeResult":
        yield Label("[bold red]POMODORO[/]", classes="panel-header")
        yield Label("25:00", id="timer")
        yield Button("Start/Pause", id="toggle", variant="success")
        yield Button("Reset", id="reset", variant="primary")

    def on_mount(self) -> None:
        self.set_interval(1, self.tick)

    def tick(self) -> None:
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer()

    def update_timer(self) -> None:
        m, s = divmod(self.time_left, 60)
        try:
            # Type hint with casting to satisfy LSP and provide runtime safety
            timer_label = self.query_one("#timer", Label)
            timer_label.update(f"{m:02}:{s:02}")
        except Exception:
            pass

    def on_button_pressed(self, event: Button.Pressed) -> None:
        button_id: Any = event.button.id
        if button_id == "toggle":
            self.is_running = not self.is_running
        elif button_id == "reset":
            self.is_running = False
            self.time_left = 25 * 60
            self.update_timer()
