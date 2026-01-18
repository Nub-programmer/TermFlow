from datetime import datetime
from textual.widgets import Static
from textual.reactive import reactive

class Clock(Static):
    """A widget to display the current time and date."""

    time = reactive(datetime.now().strftime("%H:%M:%S"))
    date = reactive(datetime.now().strftime("%A, %d %B %Y"))

    def on_mount(self) -> None:
        """Called when widget is mounted."""
        self.set_interval(1, self.update_time)

    def update_time(self) -> None:
        """Update the time re-render."""
        now = datetime.now()
        self.time = now.strftime("%H:%M:%S")
        self.date = now.strftime("%A, %d %B %Y")

    def render(self) -> str:
        """Render the widget."""
        return f"\n[bold white]{self.time}[/]\n[blue]{self.date}[/]"
