from datetime import datetime
from textual.widgets import Static

class ClockPanel(Static):
    def on_mount(self):
        self.set_interval(1, self.update_time)

    def update_time(self):
        self.update(self.render_content())

    def render_content(self):
        now = datetime.now()
        return f"[bold cyan]{now.strftime('%H:%M:%S')}[/]\n[dim]{now.strftime('%Y-%m-%d')}[/]"

    def render(self):
        return self.render_content()
