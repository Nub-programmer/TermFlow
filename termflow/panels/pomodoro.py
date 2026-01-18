from textual.widgets import Static, Button, Label
from textual.reactive import reactive

class PomodoroPanel(Static):
    time_left = reactive(25 * 60)
    is_running = False

    def compose(self):
        yield Label("[bold red]POMODORO[/]")
        yield Label("25:00", id="timer")
        yield Button("Start/Pause", id="toggle")
        yield Button("Reset", id="reset")

    def on_mount(self):
        self.set_interval(1, self.tick)

    def tick(self):
        if self.is_running and self.time_left > 0:
            self.time_left -= 1
            self.update_timer()

    def update_timer(self):
        m, s = divmod(self.time_left, 60)
        self.query_one("#timer").update(f"{m:02}:{s:02}")

    def on_button_pressed(self, event):
        if event.button.id == "toggle":
            self.is_running = not self.is_running
        elif event.button.id == "reset":
            self.is_running = False
            self.time_left = 25 * 60
            self.update_timer()
