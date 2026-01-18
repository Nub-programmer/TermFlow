from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, Center, Middle
from textual.binding import Binding
from termflow.panels.clock import ClockPanel
from termflow.panels.todo import TodoPanel
from termflow.panels.pomodoro import PomodoroPanel
from termflow.panels.info import InfoPanel

ASCII_LOGO = """
 [bold blue]
  _____                   ______ _                 
 |_   _|                 |  ____| |                
   | | ___ _ __ _ __ ___ | |__  | | _____      __ 
   | |/ _ \ '__| '_ ` _ \|  __| | |/ _ \ \ /\ / / 
   | |  __/ |  | | | | | | |    | | (_) \ V  V /  
   \_/\___|_|  |_| |_| |_|_|    |_|\___/ \_/\_/   
 [/]
 [italic blue]Your minimalist terminal productivity hub[/]
"""

HELP_TEXT = """
[bold underline]Keyboard Shortcuts[/]

[bold]?[/] - Toggle Help Overlay
[bold]q[/] - Quit TermFlow
[bold]Tab[/] - Cycle Focus
[bold]Enter[/] - Submit Todo / Toggle Task
[bold]s[/] - Start/Pause Pomodoro
[bold]r[/] - Reset Pomodoro

[bold underline]Todo Tags[/]
Use [bold light_blue][school][/], [bold green][dev][/], or [bold yellow][life][/] in your tasks.

[bold dim]Press any key or ? to close[/]
"""

class HelpOverlay(Center):
    def compose(self) -> ComposeResult:
        with Middle():
            yield Static(HELP_TEXT, id="help-content")

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("?", "toggle_help", "Help", show=True),
        Binding("s", "toggle_pomodoro", "Start/Pause", show=True),
        Binding("r", "reset_pomodoro", "Reset", show=True),
    ]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static(ASCII_LOGO, id="logo")
        yield Grid(
            TodoPanel(id="todo"),
            ClockPanel(id="clock"),
            PomodoroPanel(id="pomodoro"),
            InfoPanel(id="info"),
        )
        yield HelpOverlay(id="help-overlay")
        yield Footer()

    def on_mount(self) -> None:
        self.query_one("#help-overlay").display = False

    def action_toggle_help(self) -> None:
        overlay = self.query_one("#help-overlay")
        overlay.display = not overlay.display

    def action_toggle_pomodoro(self) -> None:
        try:
            pomodoro = self.query_one(PomodoroPanel)
            pomodoro.handle_toggle()
        except:
            pass

    def action_reset_pomodoro(self) -> None:
        try:
            pomodoro = self.query_one(PomodoroPanel)
            pomodoro.handle_reset()
        except:
            pass

if __name__ == "__main__":
    app = TermFlowApp()
    app.run()
