from datetime import datetime
from textual.widgets import Static

class ClockPanel(Static):
    can_focus = False
    def on_mount(self):
        self.set_interval(1, self.update_time)

    def update_time(self):
        self.update(self.render_content())

    def render_content(self):
        # Using datetime.now().astimezone() would ensure system local time
        # but datetime.now() already uses system local time by default.
        # To be explicitly sure and safe as per instructions:
        now = datetime.now().astimezone()
        return f"[bold cyan]{now.strftime('%H:%M:%S')}[/]\n[dim]{now.strftime('%Y-%m-%d')}[/]"

    def render(self):
        return self.render_content()
