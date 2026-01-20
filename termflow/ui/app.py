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
 [italic blue]Your minimalist terminal productivity hub[/]
"""

class HelpScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
        Binding("h", "dismiss", "Close"),
    ]
    
    def compose(self) -> ComposeResult:
        help_content = f"""
[bold underline]Keyboard Shortcuts[/]

[bold]A[/] - Add Task
[bold]D[/] - Delete Task
[bold]Space[/] - Toggle Task
[bold]P[/] - Pomodoro Start/Pause
[bold]R[/] - Pomodoro Reset
[bold]I[/] - Info Panel
[bold]F[/] - Flow Mode Toggle
[bold]H / ?[/] - Help Overlay
[bold]Q[/] - Quit

[bold underline]Paths[/]
Config: {CONFIG_FILE}
Data: {DATA_DIR}

[bold dim]Press ESC, Q, or H to close[/]
"""
        yield Static(help_content, id="help-content", classes="modal-panel")

class InfoScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("q", "dismiss", "Close"),
        Binding("i", "dismiss", "Close"),
    ]
    
    def compose(self) -> ComposeResult:
        info_content = """
[bold]TermFlow[/]
Minimalist terminal focus environment.
Designed to reduce cognitive load.

[bold]Credits[/]
Creator: Nub-programmer / Atharv
Community: https://dsc.gg/axoninnova

Explore the interface. 
TermFlow reveals itself gradually.

[bold dim]Press ESC, Q, or I to close[/]
"""
        yield Static(info_content, id="info-content", classes="modal-panel")

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("h", "toggle_help", "Help", show=True),
        Binding("question_mark", "toggle_help", "Help", show=False),
        Binding("i", "toggle_info", "Info", show=True),
        Binding("p", "toggle_pomodoro", "Pomodoro", show=True),
        Binding("r", "reset_pomodoro", "Reset", show=True),
        Binding("a", "add_task", "Add Task", show=True),
        Binding("f", "toggle_flow", "Flow Mode", show=True),
    ]

    flow_mode = reactive(False)

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

    def watch_flow_mode(self, flow_mode: bool) -> None:
        self.set_class(flow_mode, "flow-mode-on")
        if flow_mode:
            self.notify("Flow Mode: Active")
        else:
            self.notify("Flow Mode: Deactivated")

    def action_toggle_flow(self) -> None:
        self.flow_mode = not self.flow_mode

    def action_toggle_help(self) -> None:
        self.push_screen(HelpScreen())

    def action_toggle_info(self) -> None:
        self.push_screen(InfoScreen())

    def action_toggle_pomodoro(self) -> None:
        try:
            self.query_one(PomodoroPanel).handle_toggle()
            if random.random() < 0.2:
                self.notify("Focus session running.")
        except:
            pass

    def action_reset_pomodoro(self) -> None:
        try:
            self.query_one(PomodoroPanel).handle_reset()
        except:
            pass

    def action_add_task(self) -> None:
        try:
            todo = self.query_one(TodoPanel)
            todo.focus_input()
        except:
            pass

    def on_mount(self) -> None:
        self.set_interval(300, self.quiet_message)

    def quiet_message(self) -> None:
        messages = ["Good pace. Keep going.", "You've been here a while.", "Focus is power."]
        if random.random() < 0.05:
            self.notify(random.choice(messages))

def main():
    app = TermFlowApp()
    app.run()

if __name__ == "__main__":
    main()
