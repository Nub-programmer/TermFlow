from textual.app import App
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, Container
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

[bold]?[/] - Toggle Help
[bold]q[/] - Quit
[bold]Tab[/] - Cycle Focus
[bold]Enter[/] - Submit Todo / Toggle Task

[bold underline]Todo Tags[/]
Use [bold light_blue][school][/], [bold green][dev][/], or [bold yellow][life][/] in your tasks.
"""

class HelpOverlay(Container):
    def compose(self):
        yield Static(HELP_TEXT, id="help-content")

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        ("q", "quit", "Quit"),
        ("?", "toggle_help", "Help")
    ]

    def compose(self):
        yield Header()
        yield Static(ASCII_LOGO, id="logo")
        yield Grid(
            TodoPanel(id="todo"),
            ClockPanel(id="clock"),
            PomodoroPanel(id="pomodoro"),
            InfoPanel(id="info"),
        )
        yield HelpOverlay(id="help-overlay")
        yield Footer()

    def on_mount(self):
        self.query_one("#help-overlay").styles.display = "none"

    def action_toggle_help(self):
        overlay = self.query_one("#help-overlay")
        if overlay.styles.display == "none":
            overlay.styles.display = "block"
        else:
            overlay.styles.display = "none"

if __name__ == "__main__":
    app = TermFlowApp()
    app.run()
