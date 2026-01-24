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
from termflow.termflow.utils.storage import load_config, save_config, load_todos, save_todos

CAT_IDLE_A = r'''
         _     _
        /\`-"-`/\
        )` _ _ `(
    (`\ |=  Y  =|
     ) )_\  ^  /_
    ( (/ ;`-u-`; \
     \| /       \ |
      \ \_ \ / _/ /
 jgs  (,(,,)~(,,),)
'''

CAT_IDLE_B = r'''
         _     _
        /\`-"-`/\
        )` _ _ `(
       {=   Y   =}
        \   ^   /
       /`;'-u-';`\
      | /       \ |
     /\ ;__\ / _/ /
 jgs \___, )~(,,),)
        (_(
'''

CAT_STAND = r'''
                      ,
                    _/((
           _.---. .'   `\
         .'      `     ^ T=
        /     \       .--'
       |      /       )'-.
       ; ,   <__..-(   '-.)
        \ \-.__)    ``--._)
     jgs '.'-.__.-.
           '-...-'
'''

CAT_WALK_A = r'''
        _
       //
      ||              |\_/|
       \\  .-""""-._,' e e(
        \\/         \  =_Y/=
         \    \       /`"`
          \   | /    |
          /  / -\   /
          `\ \\  | ||
            \_)) |_))
'''

CAT_WALK_B = r'''
           _ 
          ((
           \\
            ))       
           //.--.     |\_/|
          |      `'..' a a(
           \  \      \ =_Y/=
           /   |   /  /`"`
           > /` --< <<
           \__))   \_))
'''

CAT_PLAY_A = r'''
                      __     __,
                      \,`~"~` /
      .-=-.           /    . .\
     / .-. \          {  =    Y}=
    (_/   \ \          \      / 
           \ \        _/`'`'`b
            \ `.__.-'`        \-._
             |            '.__ `'-;_
             |            _.' `'-.__)
              \    ;_..--'/     //  \
              |   /  /   |     //    |
              \  \ \__)   \   //    /
               \__)        './/   .'
                             `'-'`
'''

CAT_PLAY_B = r'''
                   .-o=o-.
               ,  /=o=o=o=\ .--.
              _|\|=o=O=o=O=|    \
          __.'  a`\=o=o=o=(`\   /
          '.   a 4/`|.-""'`\ \ ;'`)   .---.
            \   .'  /   .--'  |_.'   / .-._)
             `)  _.'   /     /`-.__.' /
              `'-.____;     /'-.___.-'
                       `"""`
'''

ASCII_LOGO = r'''
 [bold blue]
  _____                   ______ _                 
 |_   _|                 |  ____| |                
   | | ___ _ __ _ __ ___ | |__  | | _____      __ 
   | |/ _ \ '__| '_ ` _ \|  __| | |/ _ \ \ /\ / / 
   | |  __/ |  | | | | | | |    | | (_) \ V  V /  
   \_/\___|_|  |_| |_| |_|_|    |_|\___/ \_/\_/   
 [/]
[italic dim]your minimalist terminal productivity hub[/]
'''


class FlowModeProvider(Provider):
    """Provides Flow Mode commands only when Flow Mode is active."""
    
    @property
    def _app(self):
        return self.app
    
    async def search(self, query: str) -> Hits:
        app = self.app # Use self.app directly
        if not hasattr(app, 'flow_state') or getattr(app, 'flow_state', 'IDLE') != "DEEP":
            return
        
        matcher = self.matcher(query)
        
        pomo_status = "ON" if getattr(app, 'pomo_visible', True) else "OFF"
        reflection_status = "ON" if getattr(app, 'reflection_visible', True) else "OFF"
        buddy_status = "ON" if getattr(app, 'buddy_enabled', False) else "OFF"
        motion_status = "ON" if getattr(app, 'buddy_motion', True) else "OFF"
        anim_mode = getattr(app, 'buddy_anim_mode', 'IDLE_ACTIVE')
        anim_status = "Idle + Active" if anim_mode == "IDLE_ACTIVE" else "Idle Only"
        
        commands = [
            (f"Flow Mode: Pomodoro [{pomo_status}]", getattr(app, 'action_toggle_pomo_visibility', lambda: None), "Toggle timer visibility"),
            (f"Flow Mode: Reflection [{reflection_status}]", getattr(app, 'action_toggle_reflection_visibility', lambda: None), "Toggle reflection panel"),
            (f"Flow Mode: Focus Buddy [{buddy_status}]", getattr(app, 'action_toggle_buddy', lambda: None), "Toggle buddy companion"),
        ]
        
        if getattr(app, 'buddy_enabled', False):
            commands.extend([
                (f"  Buddy Motion [{motion_status}]", getattr(app, 'action_toggle_buddy_motion', lambda: None), "Toggle animation"),
                (f"  Buddy Animation Mode [{anim_status}]", getattr(app, 'action_toggle_buddy_anim_mode', lambda: None), "Switch Idle/Full"),
                (f"  Buddy Position: Left", getattr(app, 'action_set_buddy_left', lambda: None), "Dock left"),
                (f"  Buddy Position: Right", getattr(app, 'action_set_buddy_right', lambda: None), "Dock right"),
                (f"  Buddy Position: Inline", getattr(app, 'action_set_buddy_inline', lambda: None), "Use empty space"),
            ])
        
        for name, callback, help_text in commands:
            score = matcher.match(name)
            if not query or score > 0:
                yield Hit(score if score > 0 else 100, matcher.highlight(name) if query else name, callback, help=help_text)


class GeneralProvider(Provider):
    """Provides general commands available in all modes."""
    
    @property
    def _app(self):
        return self.app
    
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        
        commands = [
            ("Theme: Dark Mode", lambda: setattr(app, 'theme', "builtin:dark"), "Switch to dark theme"),
            ("Theme: Light Mode", lambda: setattr(app, 'theme', "builtin:light"), "Switch to light theme"),
            ("Help: Show Guide", getattr(app, 'action_toggle_help', lambda: None), "View keyboard shortcuts"),
            ("Info: About TermFlow", getattr(app, 'action_toggle_info', lambda: None), "App information"),
            ("Quit Application", getattr(app, 'action_quit', lambda: None), "Exit TermFlow"),
        ]
        
        for name, callback, help_text in commands:
            score = matcher.match(name)
            if not query or score > 0:
                yield Hit(score if score > 0 else 50, matcher.highlight(name) if query else name, callback, help=help_text)


class HelpScreen(ModalScreen):
    BINDINGS = [Binding("escape", "dismiss", "Close")]
    
    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="modal-panel"):
            yield Static("""
[bold underline]TermFlow Keybindings[/]

[bold]GENERAL[/]
[bold]:[/]      - Open Command Palette
[bold]ESC[/]    - Back / Close
[bold]F[/]      - Toggle Flow Mode
[bold]Enter[/]  - Add task
[bold]Space[/]  - Toggle task
[bold]Del[/]    - Remove task

[bold]FLOW MODE[/]
- Single-task focus (read-only)
- Pomodoro auto-start
- Task auto-advance on completion

[bold]FLOW MODE INTERFACE SETTINGS[/]
- Pomodoro ON / OFF
- Reflection ON / OFF
- Focus Buddy ON / OFF
- Focus Buddy Motion ON / OFF
- Focus Buddy Position: Left, Right, Inline
- Buddy Animation Mode: Idle only, Idle + Active Motion
        """)


class InfoScreen(ModalScreen):
    BINDINGS = [Binding("escape", "dismiss", "Close")]
    
    def compose(self) -> ComposeResult:
        with VerticalScroll(classes="modal-panel"):
            yield Static("""
[bold]TermFlow[/]
A terminal-first deep focus system

Author: Atharv
Community: AxonInnova (https://dsc.gg/axoninnova)
        """)


class TermFlowApp(App):
    CSS_PATH = "styles.tcss"
    COMMANDS = App.COMMANDS | {FlowModeProvider, GeneralProvider}
    BINDINGS = [
        Binding("f", "enter_flow", "Flow", show=True),
        Binding("escape", "escape_handler", "Exit", show=False, priority=True),
        Binding("p", "pause_timer", "Pause", show=True),
        Binding("t", "add_todo", "Add", show=True),
        Binding("q", "quit", "Quit", show=True),
        Binding("colon", "open_command_palette", "Command Palette", show=False),
        Binding("b", "toggle_buddy", "Toggle Buddy", show=True),
        Binding("question_mark,f1", "toggle_help", "Help", show=True),
    ]

    flow_state = reactive("IDLE")
    intention = reactive("")
    buddy_enabled = reactive(False)
    buddy_motion = reactive(True)
    buddy_anim_mode = reactive("IDLE_ACTIVE")
    buddy_state = reactive("IDLE")
    buddy_frame = reactive(0)
    buddy_position = reactive("left")
    pomo_visible = reactive(True)
    reflection_visible = reactive(True)
    current_task = reactive(None)
    _palette_open = reactive(False)

    def on_mount(self) -> None:
        config = load_config()
        self.buddy_enabled = config.get("buddy_enabled", False)
        self.buddy_motion = config.get("buddy_motion", True)
        self.buddy_anim_mode = config.get("buddy_anim_mode", "IDLE_ACTIVE")
        self.buddy_position = config.get("buddy_position", "left")
        self.pomo_visible = config.get("pomo_visible", True)
        self.reflection_visible = config.get("reflection_visible", True)
        self.set_interval(2.5, self.tick_buddy)

    async def on_key(self, event) -> None:
        pass

    def tick_buddy(self) -> None:
        if self.flow_state == "DEEP" and self.buddy_enabled:
            if self.buddy_motion:
                if self.buddy_anim_mode == "IDLE_ONLY":
                    self.buddy_frame = (self.buddy_frame + 1) % 2
                    self.buddy_state = "IDLE"
                else:
                    self.buddy_frame = (self.buddy_frame + 1) % 10
                    if self.buddy_frame < 2:
                        self.buddy_state = "IDLE"
                    elif self.buddy_frame == 2:
                        self.buddy_state = "STAND"
                    elif self.buddy_frame in [3, 4]:
                        self.buddy_state = "WALK"
                    elif self.buddy_frame in [5, 6]:
                        self.buddy_state = "PLAY_A"
                    elif self.buddy_frame in [7, 8]:
                        self.buddy_state = "PLAY_B"
                    else:
                        self.buddy_state = "IDLE"
            else:
                self.buddy_state = "IDLE"
                self.buddy_frame = 0
            self.update_buddy_art()

    def update_buddy_art(self) -> None:
        if self.flow_state != "DEEP" or not self.buddy_enabled:
            return
        try:
            buddy_widget = self.query_one("#focus-buddy", Static)
            frames = {
                "IDLE": CAT_IDLE_A if self.buddy_frame % 2 == 0 else CAT_IDLE_B,
                "STAND": CAT_STAND,
                "WALK": CAT_WALK_A if self.buddy_frame == 3 else CAT_WALK_B,
                "PLAY_A": CAT_PLAY_A,
                "PLAY_B": CAT_PLAY_B
            }
            art = frames.get(self.buddy_state, CAT_IDLE_A)
            status_text = " [italic]Begin.[/]" if self.buddy_frame == 0 else " [italic]Focus.[/]"
            buddy_widget.update(Art(art + status_text))
        except Exception:
            pass

    def action_escape_handler(self) -> None:
        """Global ESC handler - always works."""
        if len(self.screen_stack) > 1:
            self.pop_screen()
        elif self.flow_state == "DEEP":
            self.action_exit_flow()

    def action_toggle_buddy_anim_mode(self) -> None:
        self.buddy_anim_mode = "IDLE_ONLY" if self.buddy_anim_mode == "IDLE_ACTIVE" else "IDLE_ACTIVE"
        self.save_current_config()

    def action_toggle_buddy(self) -> None:
        self.buddy_enabled = not self.buddy_enabled
        self.save_current_config()
        self.update_buddy_layout()

    def action_toggle_buddy_motion(self) -> None:
        self.buddy_motion = not self.buddy_motion
        self.save_current_config()

    def action_set_buddy_left(self) -> None:
        self.buddy_position = "left"
        self.save_current_config()
        self.update_buddy_layout()

    def action_set_buddy_right(self) -> None:
        self.buddy_position = "right"
        self.save_current_config()
        self.update_buddy_layout()

    def action_set_buddy_inline(self) -> None:
        self.buddy_position = "inline"
        self.save_current_config()
        self.update_buddy_layout()

    def action_toggle_pomo_visibility(self) -> None:
        self.pomo_visible = not self.pomo_visible
        self.save_current_config()
        try:
            self.query_one("#flow-pomo").set_class(not self.pomo_visible, "hidden")
        except Exception:
            pass

    def action_toggle_reflection_visibility(self) -> None:
        self.reflection_visible = not self.reflection_visible
        self.save_current_config()
        try:
            self.query_one("#flow-reflection").set_class(not self.reflection_visible, "hidden")
        except Exception:
            pass

    def save_current_config(self) -> None:
        from typing import Any
        config: dict[str, Any] = load_config()
        config["buddy_enabled"] = bool(self.buddy_enabled)
        config["buddy_motion"] = bool(self.buddy_motion)
        config["buddy_anim_mode"] = str(self.buddy_anim_mode)
        config["buddy_position"] = str(self.buddy_position)
        config["pomo_visible"] = bool(self.pomo_visible)
        config["reflection_visible"] = bool(self.reflection_visible)
        save_config(config)

    def update_buddy_layout(self) -> None:
        if self.flow_state == "DEEP":
            try:
                container = self.query_one("#flow-container", Horizontal)
                buddy_widget = self.query_one("#focus-buddy", Static)
                container.remove_class("pos-left", "pos-right", "pos-inline")
                if self.buddy_enabled:
                    container.add_class(f"pos-{self.buddy_position}")
                    buddy_widget.remove_class("hidden")
                    self.update_buddy_art()
                else:
                    buddy_widget.add_class("hidden")
            except Exception:
                pass

    def compose(self) -> ComposeResult:
        yield Header()
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
                    yield PomodoroPanel(id="flow-pomo")
                    yield Static("", id="flow-task")
                    yield InfoPanel(id="flow-reflection")
        yield Footer()

    def watch_flow_state(self, state: str) -> None:
        try:
            dashboard = self.query_one("#dashboard-view")
            flow_view = self.query_one("#flow-container")
        except Exception:
            return
            
        if state == "DEEP":
            dashboard.add_class("hidden")
            flow_view.remove_class("hidden")
            self.load_next_flow_task()
            self.update_buddy_layout()
            try:
                self.query_one("#flow-pomo").set_class(not self.pomo_visible, "hidden")
                self.query_one("#flow-reflection").set_class(not self.reflection_visible, "hidden")
            except Exception:
                pass
            try:
                pomo = self.query_one("#flow-pomo", PomodoroPanel)
                if not pomo.timer_active:
                    pomo.handle_toggle()
            except Exception:
                pass
        else:
            dashboard.remove_class("hidden")
            flow_view.add_class("hidden")

    def load_next_flow_task(self) -> None:
        todos = load_todos()
        active = [t for t in todos if not t.get("completed", False)]
        try:
            if active:
                self.current_task = active[0]
                self.query_one("#flow-task", Static).update(f"[bold cyan]Task:[/] {active[0]['task']}")
            else:
                self.current_task = None
                self.query_one("#flow-task", Static).update("[italic]All tasks completed. Add more in dashboard.[/]")
        except Exception:
            pass

    def action_complete_task(self) -> None:
        if self.flow_state == "DEEP" and self.current_task:
            todos = load_todos()
            for t in todos:
                if t['task'] == self.current_task['task']:
                    t['completed'] = True
                    break
            save_todos(todos)
            self.load_next_flow_task()

    def action_open_command_palette(self) -> None:
        """Open command palette with proper state management."""
        from textual.command import CommandPalette
        self._palette_open = True
        self.push_screen(CommandPalette())

    def action_enter_flow(self) -> None:
        if self.flow_state == "IDLE":
            self.flow_state = "DEEP"

    def action_exit_flow(self) -> None:
        self.flow_state = "IDLE"

    def action_pause_timer(self) -> None:
        selector = "#flow-pomo" if self.flow_state == "DEEP" else "#pomodoro"
        try:
            self.query_one(selector, PomodoroPanel).handle_toggle()
        except Exception:
            pass

    def action_add_todo(self) -> None:
        if self.flow_state == "IDLE":
            try:
                self.query_one(TodoPanel).focus_input()
            except Exception:
                pass

    def action_toggle_help(self) -> None:
        if self._palette_open:
            self.pop_screen()
            self._palette_open = False
        if isinstance(self.screen, HelpScreen) or isinstance(self.screen, InfoScreen):
            self.pop_screen()
        self.set_focus(None)
        self.push_screen(HelpScreen())

    def action_toggle_info(self) -> None:
        if self._palette_open:
            self.pop_screen()
            self._palette_open = False
        if isinstance(self.screen, HelpScreen) or isinstance(self.screen, InfoScreen):
            self.pop_screen()
        self.set_focus(None)
        self.push_screen(InfoScreen())


def main():
    TermFlowApp().run()


if __name__ == "__main__":
    main()
