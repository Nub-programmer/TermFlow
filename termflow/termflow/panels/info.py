from textual.widgets import Static, Label
from termflow.termflow.utils.weather import get_weather
from termflow.termflow.utils.quotes import get_quote

class InfoPanel(Static):
    def compose(self):
        yield Label("[bold yellow]Reflection[/]", classes="panel-header")
        yield Label("Loading...", id="reflection")
        # Removed weather/context section as per philosophy of minimal UI in Flow

    def on_mount(self):
        self.update_info()

    def update_info(self):
        # Pass the coroutine object, not the result of calling it if it expects a coroutine
        # Actually in textual, run_worker can take the coroutine directly
        self.run_worker(self.fetch_data())

    async def fetch_data(self):
        try:
            w = get_weather()
        except:
            w = "Global: 18°C"
        try:
            q = get_quote()
        except:
            q = "Stay focused."
        
        self.query_one("#weather", Label).update(f"Weather: {w}")
        self.query_one("#quote", Label).update(q)
