from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Grid, VerticalScroll, Horizontal, Container
from textual.binding import Binding
from textual.screen import ModalScreen
from textual.reactive import reactive
from textual.command import Hit, Hits, Provider
from rich.text import Text as Art
from termflow.termflow.panels.clock import ClockPanel
from termflow.termflow.panels.todo_list import TodoPanel
from termflow.termflow.panels.pomodoro import PomodoroPanel
from termflow.termflow.panels.info import InfoPanel
from termflow.termflow.utils.storage import load_config, save_config

class TermFlowCommandProvider(Provider):
    """A command provider for TermFlow commands."""
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        
        commands = [
            ("Toggle Focus Buddy", self.app.action_toggle_buddy, "Show/Hide focus buddy"),
            ("Buddy: Position Left", self.app.action_set_buddy_left, "Place buddy on left"),
            ("Buddy: Position Right", self.app.action_set_buddy_right, "Place buddy on right"),
            ("Buddy: Position Inline", self.app.action_set_buddy_inline, "Place buddy inline"),
            ("Buddy: Human", lambda: self.app.set_buddy_type("human"), "Use human buddy"),
            ("Buddy: Cat", lambda: self.app.set_buddy_type("cat"), "Use cat buddy"),
            ("Buddy: Dog", lambda: self.app.set_buddy_type("dog"), "Use dog buddy"),
            ("Theme: Default", lambda: setattr(self.app, "theme", "builtin:dark"), "Switch to dark theme"),
            ("Theme: Light", lambda: setattr(self.app, "theme", "builtin:light"), "Switch to light theme"),
        ]
        
        for name, callback, help_text in commands:
            score = matcher.match(name)
            if score > 0:
                yield Hit(score, matcher.highlight(name), callback, help=help_text)

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
[bold underline]TermFlow Keybindings[/]

[bold]F[/]     - Enter Flow Mode (Deep Work)
[bold]ESC[/]   - Exit Flow Mode / Close Modal
[bold]P[/]     - Pause/Resume Pomodoro
[bold]T[/]     - Add New Todo (Dashboard only)
[bold]B[/]     - Toggle Focus Buddy
[bold]H / ?[/] - Show this Help screen
[bold]I[/]     - Show About Info
[bold]:[/]     - Open Command Palette
[bold]Q[/]     - Quit Application

[bold]Space[/] - Toggle Todo completion
[bold]Del[/]   - Remove Todo item
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
    COMMANDS = App.COMMANDS | {TermFlowCommandProvider}
    BINDINGS = [
        Binding("f", "enter_flow", "Flow", show=True),
        Binding("escape", "exit_flow", "Exit", show=False),
        Binding("p", "pause_timer", "Pause", show=True),
        Binding("t", "add_todo", "Add", show=True),
        Binding("h,question_mark", "toggle_help", "Help", show=True),
        Binding("i", "toggle_info", "Info", show=True),
        Binding("q", "quit", "Quit", show=True),
        Binding("colon", "command_palette", "Command Palette", show=False),
        Binding("b", "toggle_buddy", "Toggle Buddy", show=True),
    ]

    flow_state = reactive("IDLE")
    intention = reactive("")
    buddy_enabled = reactive(False)
    buddy_state = reactive("IDLE")
    buddy_position = reactive("left") # left, right, inline

    def on_mount(self) -> None:
        config = load_config()
        if not isinstance(config, dict):
            config = {}
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

    def action_set_buddy_inline(self) -> None:
        self.buddy_position = "inline"
        self.save_current_config()
        self.notify("Buddy Position: Inline")
        self.update_buddy_layout()

    def save_current_config(self) -> None:
        config = load_config()
        if not isinstance(config, dict):
            config = {}
        config["buddy_enabled"] = self.buddy_enabled
        config["buddy_position"] = self.buddy_position
        save_config(config)

    def update_buddy_layout(self) -> None:
        if self.flow_state == "DEEP":
            container = self.query_one("#flow-container", Horizontal)
            buddy_widget = self.query_one("#focus-buddy")
            
            # Remove all position classes
            container.remove_class("pos-left", "pos-right", "pos-inline")
            
            if self.buddy_enabled:
                container.add_class(f"pos-{self.buddy_position}")
                buddy_widget.remove_class("hidden")
                self.watch_buddy_state(self.buddy_state)
            else:
                buddy_widget.add_class("hidden")

    def compose(self) -> ComposeResult:
        header = Header()
        yield header
        with Container(id="main-container"):
            with VerticalScroll(id="dashboard-view"):
                yield Static(ASCII_LOGO, id="logo")
                yield Grid(
                    TodoPanel(id="todo"),
                    ClockPanel(id="clock"),
                    PomodoroPanel(id="pomodoro"),
                    InfoPanel(id="info"),
                    id="dashboard-grid"
                )
            
            with Horizontal(id="flow-container", classes="hidden"):
                yield Static("", id="focus-buddy", classes="hidden")
                with VerticalScroll(id="flow-content"):
                    yield Static("", id="flow-intention")
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        is_deep = (state == "DEEP")
        dashboard = self.query_one("#dashboard-view")
        flow_view = self.query_one("#flow-container")
        
        if is_deep:
            dashboard.add_class("hidden")
            flow_view.remove_class("hidden")
            
            intention_static = self.query_one("#flow-intention")
            intention_static.update(f"[bold cyan]Intention:[/] {self.intention}")
            
            self.update_buddy_layout()
            self.buddy_state = "IDLE"
            
            # Auto-start Pomodoro
            try:
                pomo = self.query_one(PomodoroPanel)
                if hasattr(pomo, "timer_active") and not pomo.timer_active:
                    pomo.handle_toggle()
            except:
                pass
        else:
            dashboard.remove_class("hidden")
            flow_view.add_class("hidden")
            self.buddy_state = "IDLE"

    def watch_buddy_state(self, state: str) -> None:
        if not self.buddy_enabled or self.flow_state != "DEEP":
            return
            
        buddy_widget = self.query_one("#focus-buddy", Static)
        
        BUDDY_TYPES = {
            "human": {
                "IDLE": "  (｡•̀ᴗ-)✧  \n   /|\\   \n   / \\   \n [Begin]",
                "FOCUS": "  ( •̀ ω •́ ) \n   \\O/   \n    |    \n [Focus]",
                "REST": "  (￣o￣)zz \n   -|-   \n   / \\   \n [Done]"
            },
            "cat": {
                "IDLE": " ／l、\n（ﾟ､ ｡ ７\nl、 ~ヽ\nじしf_, )ノ\n [Meow]",
                "FOCUS": " ／l、\n（o ω o ７\nl、 ~ヽ\nじしf_, )ノ\n [Focus]",
                "REST": " ／l、\n（u _ u ７\nl、 ~ヽ\nじしf_, )ノ\n [Zzz]"
            },
            "dog": {
                "IDLE": "  __      _ \n o'')}____// \n  `_/      ) \n  (_(_/-(_/  \n [Woof]",
                "FOCUS": "  __      _ \n O'')}____// \n  `_/      ) \n  (_(_/-(_/  \n [Focus]",
                "REST": "  __      _ \n -'')}____// \n  `_/      ) \n  (_(_/-(_/  \n [Done]"
            }
        }
        
        config = load_config()
        if not isinstance(config, dict):
            config = {}
        b_type = str(config.get("buddy_type", "human"))
        type_data = BUDDY_TYPES.get(b_type, BUDDY_TYPES["human"])
        art = type_data.get(state, "[Buddy]")
        buddy_widget.update(Art(art))

    def set_buddy_type(self, b_type: str) -> None:
        config = load_config()
        if not isinstance(config, dict):
            config = {}
        config["buddy_type"] = b_type
        save_config(config)
        self.notify(f"Buddy set to {b_type.capitalize()}")
        self.watch_buddy_state(self.buddy_state)

    def action_command_palette(self) -> None:
        """Explicitly trigger the command palette."""
        from textual.command import CommandPalette
        self.push_screen(CommandPalette())

    def action_enter_flow(self) -> None:
        if self.flow_state == "IDLE":
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
