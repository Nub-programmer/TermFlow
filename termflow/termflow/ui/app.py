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
    ]

    flow_state = reactive("IDLE")
    intention = reactive("")

    def action_command_palette(self) -> None:
        """Explicitly trigger the command palette."""
        from textual.command import CommandPalette
        self.push_screen(CommandPalette())

    def action_add_intention(self) -> None:
        if self.flow_state == "IDLE":
            # Simple simulation of adding intention
            self.intention = "Focus" 
            self.action_enter_flow()

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
            yield Static("", id="flow-intention", classes="hidden")
            yield Static("", id="focus-buddy", classes="hidden")
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        self.set_class(state == "DEEP", "state-deep")
        dashboard = self.query_one("#dashboard-grid")
        intention_display = self.query_one("#flow-intention")
        buddy = self.query_one("#focus-buddy")
        
        if state == "DEEP":
            dashboard.add_class("hidden")
            intention_display.remove_class("hidden")
            buddy.remove_class("hidden")
            intention_display.update(f"[bold cyan]Intention:[/] {self.intention}")
            # Ensure essential panels remain visible in Flow Mode
            self.query_one("#pomodoro").remove_class("hidden")
            self.query_one("#clock").remove_class("hidden")
            self.query_one("#info").remove_class("hidden")
            buddy.update("✨ [italic]Begin.[/]")
            
            # Focus buddy subtle reaction mid-session simulation
            self.set_timer(10, lambda: buddy.update("✨ [italic]Stay.[/]"))
        else:
            dashboard.remove_class("hidden")
            intention_display.add_class("hidden")
            buddy.add_class("hidden")
            # Restore visibility of all panels when exiting Flow Mode
            self.query_one("#pomodoro").remove_class("hidden")
            self.query_one("#clock").remove_class("hidden")
            self.query_one("#info").remove_class("hidden")
            try:
                self.query_one("#todo").remove_class("hidden")
            except:
                pass
            try:
                # Refresh layout to fix any visibility issues
                self.refresh()
            except:
                pass

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
