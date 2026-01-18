from textual.widgets import Static, Label
from termflow.utils.weather import get_weather
from termflow.utils.quotes import get_quote

class InfoPanel(Static):
    def compose(self):
        yield Label("[bold green]INFO[/]")
        yield Label("Weather: Loading...", id="weather")
        yield Label("\n[bold yellow]QUOTE[/]")
        yield Label("Loading...", id="quote")

    def on_mount(self):
        self.update_info()

    def update_info(self):
        self.run_worker(self.fetch_data)

    async def fetch_data(self):
        w = get_weather()
        q = get_quote()
        self.query_one("#weather").update(f"Weather: {w}")
        self.query_one("#quote").update(q)
