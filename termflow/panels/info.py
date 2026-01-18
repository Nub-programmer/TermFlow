from textual.widgets import Static, Label
from termflow.utils.weather import get_weather
from termflow.utils.quotes import get_quote

class InfoPanel(Static):
    def compose(self):
        yield Label("[bold green]INFO[/]", classes="panel-header")
        yield Label("Weather: Loading...", id="weather")
        yield Label("\n[bold yellow]QUOTE[/]", classes="panel-header")
        yield Label("Loading...", id="quote")

    def on_mount(self):
        self.update_info()

    def update_info(self):
        self.run_worker(self.fetch_data)

    async def fetch_data(self):
        from termflow.utils.storage import load_config
        config = load_config()
        city = config.get("city", "New York")
        w = get_weather(city) # Note: Weather utility needs to be updated to accept city
        q = get_quote()
        self.query_one("#weather", Label).update(f"Weather ({city}): {w}")
        self.query_one("#quote", Label).update(q)
