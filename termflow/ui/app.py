from textual.app import App
from textual.containers import Container, Grid
from textual.widgets import Header, Footer, Static
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
"""

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self):
        yield Header()
        yield Static(ASCII_LOGO, id="logo")
        yield Grid(
            TodoPanel(id="todo"),
            ClockPanel(id="clock"),
            PomodoroPanel(id="pomodoro"),
            InfoPanel(id="info"),
        )
        yield Footer()

if __name__ == "__main__":
    TermFlowApp().run()
