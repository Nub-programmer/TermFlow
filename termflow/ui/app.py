from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, Center, Middle, VerticalScroll
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.reactive import reactive
from termflow.panels.clock import ClockPanel
from termflow.panels.todo import TodoPanel
from termflow.panels.pomodoro import PomodoroPanel
from termflow.panels.info import InfoPanel
from termflow.utils.storage import load_config, DATA_DIR, CONFIG_FILE
import random

ASCII_LOGO = """
 [bold blue]
  _____                   ______ _                 
 |_   _|                 |  ____| |                
   | | ___ _ __ _ __ ___ | |__  | | _____      __ 
   | |/ _ \ '__| '_ ` _ \|  __| | |/ _ \ \ /\ / / 
   | |  __/ |  | | | | | | |    | | (_) \ V  V /  
   \_/\___|_|  |_| |_| |_|_|    |_|\___/ \_/\_/   
 [/]
 [dim]your minimalist terminal productivity hub[/]
"""

class HelpScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Orientation"),
        Binding("q", "dismiss", "Orientation"),
        Binding("h", "dismiss", "Orientation"),
    ]
    
    def compose(self) -> ComposeResult:
        help_content = f"""
[bold underline]Orientation[/]

[bold]A[/] - Add Task
[bold]D[/] - Delete Task
[bold]Space[/] - Toggle Task
[bold]P[/] - Start Flow
[bold]R[/] - Reset Flow
[bold]I[/] - Context
[bold]F[/] - Enter Flow
[bold]H / ?[/] - Orientation
[bold]Q[/] - Quit

[bold underline]Paths[/]
Config: {CONFIG_FILE}
Data: {DATA_DIR}

[bold dim]Press ESC, Q, or H to close[/]
"""
        yield Static(help_content, id="help-content", classes="modal-panel")

class InfoScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Context"),
        Binding("q", "dismiss", "Context"),
        Binding("i", "dismiss", "Context"),
    ]
    
    def compose(self) -> ComposeResult:
        info_content = """
[bold]TermFlow[/]
Minimalist focus engine.
Designed to reduce cognitive load.

[bold]Credits[/]
Nub-programmer / Atharv
https://dsc.gg/axoninnova

Explore the interface. 
TermFlow reveals itself gradually.

[bold dim]Press ESC, Q, or I to close[/]
"""
        yield Static(info_content, id="info-content", classes="modal-panel")

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("h", "toggle_help", "orientation", show=True),
        Binding("i", "toggle_info", "context", show=True),
        Binding("p", "toggle_pomodoro", "start flow", show=True),
        Binding("f", "toggle_flow", "enter flow", show=True),
    ]

    flow_state = reactive("IDLE") # IDLE, FLOW, DEEP

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        with VerticalScroll(id="main-scroll"):
            yield Static(ASCII_LOGO, id="logo")
            yield Grid(
                TodoPanel(id="todo"),
                ClockPanel(id="clock"),
                PomodoroPanel(id="pomodoro"),
                InfoPanel(id="info"),
            )
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        self.remove_class("state-idle")
        self.remove_class("state-flow")
        self.remove_class("state-deep")
        self.add_class(f"state-{state.lower()}")
        
    def action_toggle_flow(self) -> None:
        if self.flow_state == "IDLE":
            self.flow_state = "DEEP"
        else:
            self.flow_state = "IDLE"

    def action_toggle_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_toggle_info(self) -> None:
        self.push_screen(InfoScreen())

    def action_toggle_pomodoro(self) -> None:
        try:
            self.query_one(PomodoroPanel).handle_toggle()
            if self.flow_state == "IDLE":
                self.flow_state = "FLOW"
            elif self.flow_state == "FLOW":
                self.flow_state = "IDLE"
        except:
            pass

    def action_reset_pomodoro(self) -> None:
        try:
            self.query_one(PomodoroPanel).handle_reset()
            self.flow_state = "IDLE"
        except:
            pass

    def action_add_task(self) -> None:
        try:
            todo = self.query_one(TodoPanel)
            todo.focus_input()
        except:
            pass

    def on_mount(self) -> None:
        self.add_class("state-idle")

def main():
    app = TermFlowApp()
    app.run()

if __name__ == "__main__":
    main()
