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

    def on_mount(self) -> None:
        config = load_config()
        self.buddy_enabled = config.get("buddy_enabled", False)

    def action_toggle_buddy(self) -> None:
        self.buddy_enabled = not self.buddy_enabled
        config = load_config()
        config["buddy_enabled"] = self.buddy_enabled
        save_config(config)
        self.notify(f"Buddy: {'ON' if self.buddy_enabled else 'OFF'}")
        
        # Immediate UI update for Flow Mode
        if self.flow_state == "DEEP":
            buddy_widget = self.query_one("#focus-buddy")
            if self.buddy_enabled:
                buddy_widget.remove_class("hidden")
                self.watch_buddy_state(self.buddy_state)
            else:
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
            yield Static("[bold cyan]Intention:[/] ", id="flow-intention", classes="hidden")
            yield Static("", id="focus-buddy", classes="hidden")
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        self.set_class(state == "DEEP", "state-deep")
        dashboard = self.query_one("#dashboard-grid")
        intention_display = self.query_one("#flow-intention")
        buddy_widget = self.query_one("#focus-buddy")
        
        if state == "DEEP":
            dashboard.add_class("hidden")
            intention_display.remove_class("hidden")
            intention_display.update(f"[bold cyan]Intention:[/] {self.intention}")
            
            if self.buddy_enabled:
                buddy_widget.remove_class("hidden")
                self.buddy_state = "IDLE"
                self.watch_buddy_state("IDLE")
                self.set_timer(10, lambda: setattr(self, "buddy_state", "FOCUS"))
            else:
                buddy_widget.add_class("hidden")
            
            self.query_one("#pomodoro").remove_class("hidden")
            self.query_one("#clock").remove_class("hidden")
            self.query_one("#info").remove_class("hidden")
        else:
            dashboard.remove_class("hidden")
            intention_display.add_class("hidden")
            buddy_widget.add_class("hidden")
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
        chars = {"IDLE": "[•]", "FOCUS": "[■]", "REST": "[·]"}
        msgs = {"IDLE": "Begin.", "FOCUS": "Stay.", "REST": "Done."}
        
        char = chars.get(state, "[•]")
        msg = msgs.get(state, "")
        
        buddy_widget.update(f"[bold yellow]{char}[/]\n[dim]{msg}[/]")
        self.set_timer(3, lambda: buddy_widget.update(f"[bold yellow]{char}[/]"))

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
