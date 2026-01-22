from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, VerticalScroll
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.reactive import reactive
from termflow.termflow.panels.clock import ClockPanel
from termflow.termflow.panels.todo_list import TodoPanel
from termflow.termflow.panels.pomodoro import PomodoroPanel
from termflow.termflow.panels.info import InfoPanel

ASCII_LOGO = """
 [bold blue]
  _____                   ______ _                 
 |_   _|                 |  ____| |                
   | | ___ _ __ _ __ ___ | |__  | | _____      __ 
   | |/ _ \ '__| '_ ` _ \|  __| | |/ _ \ \ /\ / / 
   | |  __/ |  | | | | | | |    | | (_) \ V  V /  
   \_/\___|_|  |_| |_| |_|_|    |_|\___/ \_/\_/   
 [/]
[italic dim]your minimalist terminal productivity hub[/]
"""

class HelpScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("h", "dismiss", "Close"),
    ]
    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="modal-panel"):
            yield Static("""
[bold underline]Orientation[/]
[bold]T[/] - Add Intention
[bold]D[/] - Delete
[bold]Space[/] - Toggle
[bold]F[/] - Flow Mode
[bold]P[/] - Pause/Resume
[bold]I[/] - Info
[bold]ESC[/] - Exit Flow
        """)

class InfoScreen(ModalScreen):
    BINDINGS = [
        Binding("escape", "dismiss", "Close"),
        Binding("i", "dismiss", "Close"),
    ]
    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="modal-panel"):
            yield Static("""
[bold]TermFlow[/]
Project: TermFlow
Made by: Axoninova community
Founder: Atharv
Invite: https://dsc.gg/axoninnova

This is a mindset tool designed 
to reduce cognitive load and 
enable deep work.
        """)

from termflow.termflow.utils.storage import load_config, save_config

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("f", "enter_flow", "Flow", show=True),
        Binding("escape", "exit_flow", "Exit", show=False),
        Binding("p", "pause_timer", "Pause", show=True),
        Binding("t", "add_todo", "Add", show=True),
        Binding("h", "toggle_help", "Help", show=True),
        Binding("i", "toggle_info", "Info", show=True),
        Binding("q", "quit", "Quit", show=True),
        Binding("colon", "command_palette", "Command Palette", show=False),
        Binding("b", "toggle_buddy", "Toggle Buddy", show=True),
    ]

    flow_state = reactive("IDLE")
    intention = reactive("")
    buddy_enabled = reactive(False)
    buddy_state = reactive("IDLE")
    buddy_position = reactive("left")

    def on_mount(self) -> None:
        config = load_config()
        self.buddy_enabled = config.get("buddy_enabled", False)
        self.buddy_position = config.get("buddy_position", "left")

    def action_toggle_buddy(self) -> None:
        self.buddy_enabled = not self.buddy_enabled
        self.save_current_config()
        self.notify(f"Buddy: {'ON' if self.buddy_enabled else 'OFF'}")
        self.update_buddy_layout()

    def action_set_buddy_left(self) -> None:
        self.buddy_position = "left"
        self.save_current_config()
        self.notify("Buddy Position: Left")
        self.update_buddy_layout()

    def action_set_buddy_right(self) -> None:
        self.buddy_position = "right"
        self.save_current_config()
        self.notify("Buddy Position: Right")
        self.update_buddy_layout()

    def save_current_config(self) -> None:
        config = load_config()
        config["buddy_enabled"] = self.buddy_enabled
        config["buddy_position"] = self.buddy_position
        save_config(config)

    def update_buddy_layout(self) -> None:
        if self.flow_state == "DEEP":
            container = self.query_one("#flow-container")
            buddy_widget = self.query_one("#focus-buddy")
            
            if self.buddy_enabled:
                container.set_class(self.buddy_position == "left", "buddy-left")
                container.set_class(self.buddy_position == "right", "buddy-right")
                buddy_widget.remove_class("hidden")
                self.watch_buddy_state(self.buddy_state)
            else:
                container.remove_class("buddy-left")
                container.remove_class("buddy-right")
                buddy_widget.add_class("hidden")

    def compose(self) -> ComposeResult:
        header = Header()
        header.show_clock = False
        yield header
        with VerticalScroll(id="main-scroll"):
            yield Static(ASCII_LOGO, id="logo")
            yield Grid(
                TodoPanel(id="todo"),
                ClockPanel(id="clock"),
                PomodoroPanel(id="pomodoro"),
                InfoPanel(id="info"),
                id="dashboard-grid"
            )
            with Grid(id="flow-container", classes="hidden"):
                yield Static("", id="focus-buddy", classes="hidden")
                with VerticalScroll(id="flow-content"):
                    yield Static("[bold cyan]Intention:[/] ", id="flow-intention")
                    with Grid(id="flow-panels"):
                        yield ClockPanel(id="flow-clock")
                        yield PomodoroPanel(id="flow-pomodoro")
                        yield InfoPanel(id="flow-info")
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        self.set_class(state == "DEEP", "state-deep")
        dashboard = self.query_one("#dashboard-grid")
        flow_container = self.query_one("#flow-container")
        
        if state == "DEEP":
            dashboard.add_class("hidden")
            flow_container.remove_class("hidden")
            self.query_one("#flow-intention").update(f"[bold cyan]Intention:[/] {self.intention}")
            self.update_buddy_layout()
            
            # Simulated session progress
            self.set_timer(10, lambda: setattr(self, "buddy_state", "FOCUS"))
        else:
            dashboard.remove_class("hidden")
            flow_container.add_class("hidden")
            self.buddy_state = "IDLE"
            try:
                self.query_one("#todo").remove_class("hidden")
            except:
                pass
            self.refresh()

    def watch_buddy_state(self, state: str) -> None:
        if not self.buddy_enabled or self.flow_state != "DEEP":
            return
            
        buddy_widget = self.query_one("#focus-buddy")
        
        # ANIME ASCII ART (12+ lines each)
        IDLE_ART = """
      .---.
     /     \\
    | () () |
     \\  ^  /
      |||||
      |||||
     /     \\
    /       \\
    |       |
    |       |
    /       \\
   /_/     \\_\\
      [Begin.]
"""
        FOCUS_ART = """
      .---.
     /|   |\\
    | (O) (O) |
     \\  -  /
      |||||
    --|||||--
   /  |||||  \\
  /   |||||   \\
  |   |||||   |
  \\   |||||   /
   \\  |||||  /
    --     --
      [Focus.]
"""
        REST_ART = """
      .---.
     /     \\
    | (-) (-) |
     \\  _  /
      |||||
    __|||||__
   /         \\
  /           \\
  |           |
  |           |
  \\           /
   \\_________/
      [Done.]
"""
        
        arts = {"IDLE": IDLE_ART, "FOCUS": FOCUS_ART, "REST": REST_ART}
        art = arts.get(state, IDLE_ART)
        buddy_widget.update(f"[bold yellow]{art}[/]")

    def get_system_commands(self) -> list:
        from textual.app import SystemCommand
        # Get default system commands and add custom ones
        commands = [
            SystemCommand("Toggle Focus Buddy", "Toggle Focus Buddy", self.action_toggle_buddy),
            SystemCommand("Buddy Position: Left", "Buddy Position: Left", self.action_set_buddy_left),
            SystemCommand("Buddy Position: Right", "Buddy Position: Right", self.action_set_buddy_right),
        ]
        return commands

    def action_command_palette(self) -> None:
        """Explicitly trigger the command palette."""
        from textual.command import CommandPalette
        self.push_screen(CommandPalette())

    def action_enter_flow(self) -> None:
        if self.flow_state == "IDLE":
            # In a real app we'd prompt, but here we just enter
            if not self.intention:
                self.intention = "Deep Work"
            self.flow_state = "DEEP"
            try:
                self.query_one(PomodoroPanel).handle_toggle()
            except:
                pass

    def action_exit_flow(self) -> None:
        self.flow_state = "IDLE"

    def action_pause_timer(self) -> None:
        try:
            self.query_one(PomodoroPanel).handle_toggle()
        except:
            pass

    def action_add_todo(self) -> None:
        if self.flow_state == "IDLE":
            try:
                self.query_one(TodoPanel).focus_input()
            except:
                pass

    def action_toggle_help(self) -> None:
        if self.flow_state == "IDLE":
            self.push_screen(HelpScreen())

    def action_toggle_info(self) -> None:
        if self.flow_state == "IDLE":
            self.push_screen(InfoScreen())

if __name__ == "__main__":
    TermFlowApp().run()
