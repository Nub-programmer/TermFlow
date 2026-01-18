from textual.app import ComposeResult
from textual.widgets import Static, Label
from termflow.utils.weather import get_current_weather
from termflow.utils.quotes import get_random_quote

class InfoPanel(Static):
    """Panel for Weather and Quotes."""

    def compose(self) -> ComposeResult:
        yield Label("[bold]Weather (NYC)[/bold]", classes="panel-header")
        yield Label("Loading...", id="weather-label")
        yield Label("\n[bold]Daily Quote[/bold]", classes="panel-header")
        yield Label("Loading...", id="quote-label")

    def on_mount(self) -> None:
        # Load data in background to not block UI
        self.run_worker(self.load_data)

    async def load_data(self) -> None:
        # Weather
        weather = get_current_weather()
        if "error" in weather:
            w_text = f"Unavailable: {weather['error']}"
        else:
            w_text = f"{weather['temperature']} {weather['units']['temperature']}\nWind: {weather['windspeed']} {weather['units']['windspeed']}"
        
        self.query_one("#weather-label", Label).update(w_text)

        # Quote
        quote = get_random_quote()
        if "error" in quote:
             q_text = "Could not load quote."
        else:
            q_text = f"\"{quote['text']}\"\n— {quote['author']}"
        
        self.query_one("#quote-label", Label).update(q_text)
