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
            buddy_widget = self.query_one("#focus-buddy")
            if self.buddy_enabled:
                buddy_widget.remove_class("hidden")
                self.watch_buddy_state(self.buddy_state)
            else:
                buddy_widget.add_class("hidden")

    def compose(self) -> ComposeResult:
        header = Header()
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
            # Focus Buddy - single instance
            yield Static("", id="focus-buddy", classes="hidden")
            # Flow Mode specific elements
            yield Static("", id="flow-intention", classes="hidden")
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        self.set_class(state == "DEEP", "state-deep")
        is_deep = (state == "DEEP")
        
        # UI Toggling logic (using classes)
        todo = self.query_one("#todo")
        clock = self.query_one("#clock")
        pomodoro = self.query_one("#pomodoro")
        info = self.query_one("#info")
        logo = self.query_one("#logo")
        intention_static = self.query_one("#flow-intention")
        buddy_widget = self.query_one("#focus-buddy")

        if is_deep:
            # Hide non-essential
            todo.add_class("hidden")
            logo.add_class("hidden")
            # Show Flow elements
            intention_static.remove_class("hidden")
            intention_static.update(f"[bold cyan]Intention:[/] {self.intention}")
            
            # Position core panels for Flow Mode (via CSS classes)
            self.query_one("#dashboard-grid").add_class("flow-layout")
            
            # Buddy logic
            self.update_buddy_layout()
            self.buddy_state = "IDLE"
            # Auto-start Pomodoro if not running
            try:
                pomo = self.query_one(PomodoroPanel)
                # Check if pomo has start/active state correctly
                if hasattr(pomo, "active") and not pomo.active:
                    pomo.handle_toggle()
            except:
                pass
        else:
            # Restore Dashboard
            todo.remove_class("hidden")
            logo.remove_class("hidden")
            intention_static.add_class("hidden")
            buddy_widget.add_class("hidden")
            self.query_one("#dashboard-grid").remove_class("flow-layout")
            self.buddy_state = "IDLE"

    def watch_buddy_state(self, state: str) -> None:
        if not self.buddy_enabled or self.flow_state != "DEEP":
            return
            
        buddy_widget = self.query_one("#focus-buddy")
        
        # Simplified Animated Buddy (Human, Cat, Dog)
        BUDDY_TYPES = {
            "human": {
                "IDLE": "  O  \n /|\\ \n / \\ \n[Begin]",
                "FOCUS": " \\O/ \n  |  \n / \\ \n[Focus]",
                "REST": "  O  \n -|- \n / \\ \n[Done]"
            },
            "cat": {
                "IDLE": " |\\__/,|   (`\\\n |_ _  |.--.) )\n ( T   )     /\n(((^_((_(_((_(\n[Meow]",
                "FOCUS": " |\\__/,|   (`\\\n |o o  |.--.) )\n ( T   )     /\n(((^_((_(_((_(\n[Focus]",
                "REST": " |\\__/,|   (`\\\n |u u  |.--.) )\n ( T   )     /\n(((^_((_(_((_(\n[Zzz]"
            },
            "dog": {
                "IDLE": " / \\__\n(    @\\___\n /         O\n/   (_____/\n/_____/   U\n[Woof]",
                "FOCUS": " / \\__\n(    O\\___\n /         O\n/   (_____/\n/_____/   U\n[Focus]",
                "REST": " / \\__\n(    -\\___\n /         O\n/   (_____/\n/_____/   U\n[Done]"
            }
        }
        
        config = load_config()
        # Cast to dict if it's not
        if not isinstance(config, dict):
            config = {}
        b_type = str(config.get("buddy_type", "human"))
        type_data = BUDDY_TYPES.get(b_type, BUDDY_TYPES["human"])
        art = type_data.get(state, "[Buddy]")
        buddy_widget.update(f"[bold yellow]{art}[/]")

    def get_system_commands(self, screen) -> list:
        from textual.command import SystemCommand
        return [
            SystemCommand("Toggle Focus Buddy", "Show/Hide buddy", self.action_toggle_buddy),
            SystemCommand("Buddy: Human", "Set buddy to Human", lambda: self.set_buddy_type("human")),
            SystemCommand("Buddy: Cat", "Set buddy to Cat", lambda: self.set_buddy_type("cat")),
            SystemCommand("Buddy: Dog", "Set buddy to Dog", lambda: self.set_buddy_type("dog")),
            SystemCommand("Buddy Position: Left", "Move buddy left", self.action_set_buddy_left),
            SystemCommand("Buddy Position: Right", "Move buddy right", self.action_set_buddy_right),
        ]
        save_config(config)
        self.notify(f"Buddy set to {b_type.capitalize()}")
        self.watch_buddy_state(self.buddy_state)

    def action_command_palette(self) -> None:
        """Explicitly trigger the command palette."""
        from textual.command import CommandPalette
        self.push_screen(CommandPalette())

    def action_enter_flow(self) -> None:
        if self.flow_state == "IDLE":
            # In a real app we'd prompt, but here we just enter
            if not self.intention:
                self.intention = "Focus Session"
            self.flow_state = "DEEP"

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
