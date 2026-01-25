from textual.widgets import Static, Button, Label
from textual.containers import Horizontal
from textual.reactive import reactive
from typing import TYPE_CHECKING, Any
from termflow.utils.storage import load_config, increment_pomodoro_session

if TYPE_CHECKING:
    from textual.app import ComposeResult

class PomodoroPanel(Static):
    can_focus = False
    time_left: reactive[int] = reactive(25 * 60)
    timer_active: reactive[bool] = reactive(False)
    sessions: reactive[int] = reactive(0)

    def compose(self) -> "ComposeResult":
        config = load_config()
        self.time_left = config.get("pomodoro_duration", 25) * 60
        self.sessions = config.get("pomodoro_sessions_completed", 0)
        
        yield Label("[bold red]POMODORO[/]", classes="panel-header")
        yield Label(f"{config.get('pomodoro_duration', 25)}:00", id="timer")
        yield Label(f"Sessions today: {self.sessions}", id="sessions-count")
        with Horizontal(classes="button-row"):
            yield Button("Start/Pause", id="toggle", variant="success")
            yield Button("Reset", id="reset", variant="primary")

    def on_mount(self) -> None:
        self.set_interval(1, self.tick)

    def tick(self) -> None:
        if self.timer_active:
            if self.time_left > 0:
                self.time_left -= 1
                self.update_timer()
            else:
                self.timer_active = False
                self.sessions = increment_pomodoro_session()
                self.query_one("#sessions-count", Label).update(f"Sessions today: {self.sessions}")
                self.update_timer()

    def update_timer(self) -> None:
        m, s = divmod(self.time_left, 60)
        try:
            timer_label = self.query_one("#timer", Label)
            timer_label.update(f"{m:02}:{s:02}")
        except:
            pass

    def handle_toggle(self) -> None:
        self.timer_active = not self.timer_active

    def handle_reset(self) -> None:
        self.timer_active = False
        config = load_config()
        self.time_left = config.get("pomodoro_duration", 25) * 60
        self.update_timer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "toggle":
            self.handle_toggle()
        elif event.button.id == "reset":
            self.handle_reset()
