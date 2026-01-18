from textual.app import ComposeResult
from textual.widgets import Static, Button, Label, ProgressBar
from textual.containers import Horizontal
from textual.reactive import reactive
from time import monotonic

WORK_TIME = 25 * 60  # 25 minutes
BREAK_TIME = 5 * 60  # 5 minutes

class PomodoroPanel(Static):
    """A Pomodoro timer panel."""
    
    time_left = reactive(WORK_TIME)
    total_time = reactive(WORK_TIME)
    is_running = reactive(False)
    is_break = reactive(False)
    
    def on_mount(self) -> None:
        self.timer = self.set_interval(1, self.tick, pause=True)

    def compose(self) -> ComposeResult:
        yield Label("[bold]Pomodoro Timer[/bold]", classes="panel-header")
        yield Label("25:00", id="timer-display")
        yield ProgressBar(total=WORK_TIME, show_eta=False, id="timer-progress")
        with Horizontal(classes="button-container"):
            yield Button("Start", id="start-btn", variant="success")
            yield Button("Stop", id="stop-btn", variant="error")
            yield Button("Reset", id="reset-btn", variant="primary")
        yield Label("Work Mode", id="mode-label")

    def tick(self) -> None:
        if self.time_left > 0:
            self.time_left -= 1
        else:
            self.is_running = False
            self.timer.pause()
            self.query_one("#start-btn", Button).disabled = False
            self.query_one("#stop-btn", Button).disabled = True
            
            # Auto-switch modes (simple version)
            self.is_break = not self.is_break
            self.total_time = BREAK_TIME if self.is_break else WORK_TIME
            self.time_left = self.total_time
            
            mode = "Break Time!" if self.is_break else "Work Time"
            self.query_one("#mode-label", Label).update(mode)
            self.notify(f"Timer finished! Starting {mode}.")

    def watch_time_left(self, time_left: int) -> None:
        minutes, seconds = divmod(time_left, 60)
        self.query_one("#timer-display", Label).update(f"{minutes:02}:{seconds:02}")
        self.query_one("#timer-progress", ProgressBar).update(total=self.total_time, progress=self.total_time - time_left)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "start-btn":
            self.is_running = True
            self.timer.resume()
            event.button.disabled = True
            self.query_one("#stop-btn", Button).disabled = False
            
        elif event.button.id == "stop-btn":
            self.is_running = False
            self.timer.pause()
            event.button.disabled = True
            self.query_one("#start-btn", Button).disabled = False
            
        elif event.button.id == "reset-btn":
            self.is_running = False
            self.timer.pause()
            self.is_break = False
            self.total_time = WORK_TIME
            self.time_left = WORK_TIME
            self.query_one("#start-btn", Button).disabled = False
            self.query_one("#stop-btn", Button).disabled = True
            self.query_one("#mode-label", Label).update("Work Mode")
