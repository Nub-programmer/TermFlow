from textual.widgets import Static, Label
from termflow.utils.weather import get_weather
from termflow.utils.quotes import get_quote

class InfoPanel(Static):
    can_focus = False
    def compose(self):
        yield Label("[bold yellow]Reflection[/]", classes="panel-header")
        yield Label("Loading...", id="reflection")

    def on_mount(self):
        self.update_info()
        self.set_interval(300, self.update_info)

    def update_info(self):
        # Pass the coroutine object, not the result of calling it if it expects a coroutine
        # Actually in textual, run_worker can take the coroutine directly
        self.run_worker(self.fetch_data())

    async def fetch_data(self):
        try:
            q = get_quote()
        except:
            q = "Stay focused."
        
        try:
            self.query_one("#reflection", Label).update(q)
        except:
            pass
