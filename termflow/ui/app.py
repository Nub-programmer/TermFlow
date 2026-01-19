from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, Label, ListView, ListItem, Input
from textual.containers import Grid, Center, Middle, Container
from textual.binding import Binding
from termflow.panels.clock import ClockPanel
from termflow.panels.todo import TodoPanel
from termflow.panels.pomodoro import PomodoroPanel
from termflow.panels.info import InfoPanel
from termflow.utils.storage import load_config, DATA_DIR, CONFIG_FILE
import sys

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

HELP_TEXT = f"""
[bold underline]Keyboard Shortcuts[/]

[bold]a[/] - Add Task
[bold]d[/] - Delete Selected Task
[bold]Space[/] - Toggle Task Completion
[bold]p[/] - Start/Pause Pomodoro
[bold]r[/] - Reset Pomodoro
[bold]c[/] - Command Palette (Help/Info)
[bold]?[/][bold]h[/] - Toggle Help Overlay
[bold]q[/] - Quit Safely

[bold underline]App Info[/]
[bold]Version:[/] 1.0.0
[bold]Founder:[/] Atharv
[bold]Community:[/] Axoninnova (https://dsc.gg/axoninnova)

[bold underline]Paths[/]
[bold]Config:[/] {CONFIG_FILE}
[bold]Data:[/] {DATA_DIR}

[bold dim]Press any key to close[/]
"""

class HelpOverlay(Center):
    def compose(self) -> ComposeResult:
        with Middle():
            yield Static(HELP_TEXT, id="help-content")

class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("h,?", "toggle_help", "Help", show=True),
        Binding("p", "toggle_pomodoro", "Pomodoro", show=True),
        Binding("r", "reset_pomodoro", "Reset", show=True),
        Binding("a", "add_task", "Add Task", show=True),
        Binding("c", "show_command_palette", "Commands", show=True),
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
        self.query_one(PomodoroPanel).handle_toggle()

    def action_reset_pomodoro(self) -> None:
        self.query_one(PomodoroPanel).handle_reset()

    def action_add_task(self) -> None:
        self.query_one(TodoPanel).focus_input()

    def action_show_command_palette(self) -> None:
        from textual.widgets import OptionList
        from textual.containers import Container
        from textual.screen import ModalScreen

        class CommandPalette(ModalScreen):
            def compose(self) -> ComposeResult:
                with Container(id="command-palette-container"):
                    yield Label("[bold]TermFlow Command Palette[/]", id="palette-header")
                    yield OptionList(
                        "Help",
                        "Info",
                        id="palette-list"
                    )

            def on_option_list_option_selected(self, event: OptionList.OptionSelected) -> None:
                self.dismiss(event.option.prompt)

        def handle_choice(choice: str | None) -> None:
            if choice == "Help":
                self.action_toggle_help()
            elif choice == "Info":
                self.action_show_info()

        self.push_screen(CommandPalette(), handle_choice)

    def action_show_info(self) -> None:
        from textual.screen import ModalScreen
        
        INFO_TEXT = """
[bold blue]Project name:[/] TermFlow
[bold blue]Made by:[/] Axoninova community
[bold blue]Founder:[/] Atharv
[bold blue]Invite:[/] https://dsc.gg/axoninnova

[bold underline]Description[/]
TermFlow is a minimalist terminal productivity hub designed to keep you focused and efficient. It integrates essential tools directly into your workflow.

[bold underline]Core Features[/]
• [bold]Tasks:[/] Persistent todo management with quick entry.
• [bold]Pomodoro:[/] Integrated focus timer with session tracking.
• [bold]Config:[/] Easy customization via JSON configuration.
• [bold]Keyboard-first:[/] Optimized for speed and mouse-free operation.

[bold dim]Press any key to close[/]
"""
        class InfoScreen(ModalScreen):
            def compose(self) -> ComposeResult:
                with Center():
                    with Middle():
                        yield Static(INFO_TEXT, id="info-overlay-content")
            
            def on_key(self, event) -> None:
                self.dismiss()
            
            def on_click(self, event) -> None:
                self.dismiss()

        self.push_screen(InfoScreen())

def main():
    app = TermFlowApp()
    app.run()

if __name__ == "__main__":
    main()
