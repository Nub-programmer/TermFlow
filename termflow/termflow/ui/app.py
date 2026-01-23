from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, ListItem, ListView
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

# Cat Buddy Frames
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
       jgs  \_)) |_))
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
      jgs  \__))   \_))
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
        jgs   \  \ \__)   \   //    /
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
          jgs `'-.____;     /'-.___.-'
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
    async def search(self, query: str) -> Hits:
        app = self.app
        if app.flow_state != "DEEP": return
        matcher = self.matcher(query)
        commands = [
            ("Flow: Pomodoro ON/OFF", app.action_toggle_pomo_visibility, "Toggle timer visibility"),
            ("Flow: Reflection ON/OFF", app.action_toggle_reflection_visibility, "Toggle reflection visibility"),
            ("Flow: Focus Buddy ON/OFF", app.action_toggle_buddy, "Toggle buddy visibility"),
            ("Buddy: Motion ON/OFF", app.action_toggle_buddy_motion, "Toggle animation sequence"),
            ("Buddy: Motion Mode (Idle/Full)", app.action_toggle_buddy_anim_mode, "Toggle motion intensity"),
            ("Buddy: Pos Left", app.action_set_buddy_left, "Dock left"),
            ("Buddy: Pos Right", app.action_set_buddy_right, "Dock right"),
            ("Buddy: Pos Inline", app.action_set_buddy_inline, "Dock inline"),
        ]
        for name, callback, help_text in commands:
            score = matcher.match(name)
            if score > 0:
                yield Hit(score, matcher.highlight(name), callback, help=help_text)

class GeneralProvider(Provider):
    async def search(self, query: str) -> Hits:
        matcher = self.matcher(query)
        app = self.app
        commands = [
            ("Theme: Default", lambda: setattr(app, "theme", "builtin:dark"), "Switch to dark"),
            ("Theme: Light", lambda: setattr(app, "theme", "builtin:light"), "Switch to light"),
            ("Keys: Show Help", app.action_toggle_help, "Keyboard reference"),
            ("Info: About", app.action_toggle_info, "App information"),
            ("Quit", app.action_quit, "Exit TermFlow"),
        ]
        for name, callback, help_text in commands:
            score = matcher.match(name)
            if score > 0:
                yield Hit(score, matcher.highlight(name), callback, help=help_text)

class HelpScreen(ModalScreen):
    BINDINGS = [Binding("escape", "dismiss", "Close"), Binding("h", "dismiss", "Close")]
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
    BINDINGS = [Binding("escape", "dismiss", "Close"), Binding("i", "dismiss", "Close")]
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
    COMMANDS = App.COMMANDS | {FlowModeProvider, GeneralProvider}
    BINDINGS = [
        Binding("f", "enter_flow", "Flow", show=True),
        Binding("escape", "exit_flow_safe", "Exit", show=False),
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
    buddy_motion = reactive(True)
    buddy_anim_mode = reactive("IDLE_ACTIVE") # "IDLE_ONLY" or "IDLE_ACTIVE"
    buddy_state = reactive("IDLE")
    buddy_frame = reactive(0)
    buddy_position = reactive("left")
    pomo_visible = reactive(True)
    reflection_visible = reactive(True)
    current_task = reactive(None)

    def on_mount(self) -> None:
        config = load_config()
        self.buddy_enabled = config.get("buddy_enabled", False)
        self.buddy_motion = config.get("buddy_motion", True)
        self.buddy_anim_mode = config.get("buddy_anim_mode", "IDLE_ACTIVE")
        self.buddy_position = config.get("buddy_position", "left")
        self.pomo_visible = config.get("pomo_visible", True)
        self.reflection_visible = config.get("reflection_visible", True)
        self.set_interval(2.5, self.tick_buddy)

    def tick_buddy(self) -> None:
        if self.flow_state == "DEEP" and self.buddy_enabled:
            if self.buddy_motion:
                if self.buddy_anim_mode == "IDLE_ONLY":
                    self.buddy_frame = (self.buddy_frame + 1) % 2
                    self.buddy_state = "IDLE"
                else:
                    self.buddy_frame = (self.buddy_frame + 1) % 10
                    if self.buddy_frame < 2: self.buddy_state = "IDLE"
                    elif self.buddy_frame == 2: self.buddy_state = "STAND"
                    elif self.buddy_frame in [3,4]: self.buddy_state = "WALK"
                    elif self.buddy_frame in [5,6]: self.buddy_state = "PLAY_A"
                    elif self.buddy_frame in [7,8]: self.buddy_state = "PLAY_B"
                    else: self.buddy_state = "IDLE"
            else:
                self.buddy_state = "IDLE"
                self.buddy_frame = 0
            self.update_buddy_art()

    def update_buddy_art(self) -> None:
        if self.flow_state != "DEEP" or not self.buddy_enabled: return
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
            status_text = " [italic]Begin.[/]" if self.buddy_frame == 0 else " [italic]Focus.[/]" if self.buddy_frame > 0 else ""
            buddy_widget.update(Art(art + status_text))
        except: pass

    def action_exit_flow_safe(self) -> None:
        if self.flow_state == "DEEP": self.action_exit_flow()
        elif len(self.screen_stack) > 1: self.pop_screen()

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
        self.query_one("#flow-pomo").set_class(not self.pomo_visible, "hidden")

    def action_toggle_reflection_visibility(self) -> None:
        self.reflection_visible = not self.reflection_visible
        self.save_current_config()
        self.query_one("#flow-reflection").set_class(not self.reflection_visible, "hidden")

    def save_current_config(self) -> None:
        config = load_config()
        config.update({
            "buddy_enabled": self.buddy_enabled,
            "buddy_motion": self.buddy_motion,
            "buddy_anim_mode": self.buddy_anim_mode,
            "buddy_position": self.buddy_position,
            "pomo_visible": self.pomo_visible,
            "reflection_visible": self.reflection_visible
        })
        save_config(config)

    def update_buddy_layout(self) -> None:
        if self.flow_state == "DEEP":
            container = self.query_one("#flow-container", Horizontal)
            buddy_widget = self.query_one("#focus-buddy", Static)
            container.remove_class("pos-left", "pos-right", "pos-inline")
            if self.buddy_enabled:
                container.add_class(f"pos-{self.buddy_position}")
                buddy_widget.remove_class("hidden")
                self.update_buddy_art()
            else:
                buddy_widget.add_class("hidden")

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
        dashboard = self.query_one("#dashboard-view")
        flow_view = self.query_one("#flow-container")
        if state == "DEEP":
            dashboard.add_class("hidden")
            flow_view.remove_class("hidden")
            self.load_next_flow_task()
            self.update_buddy_layout()
            self.query_one("#flow-pomo").set_class(not self.pomo_visible, "hidden")
            self.query_one("#flow-reflection").set_class(not self.reflection_visible, "hidden")
            try:
                pomo = self.query_one("#flow-pomo", PomodoroPanel)
                if not pomo.timer_active: pomo.handle_toggle()
            except: pass
        else:
            dashboard.remove_class("hidden")
            flow_view.add_class("hidden")

    def load_next_flow_task(self) -> None:
        todos = load_todos()
        active = [t for t in todos if not t.get("completed", False)]
        if active:
            self.current_task = active[0]
            self.query_one("#flow-task", Static).update(f"[bold cyan]Task:[/] {active[0]['task']}")
        else:
            self.current_task = None
            self.query_one("#flow-task", Static).update("[italic]All tasks completed. Add more in dashboard.[/]")

    def action_complete_task(self) -> None:
        if self.flow_state == "DEEP" and self.current_task:
            todos = load_todos()
            for t in todos:
                if t['task'] == self.current_task['task']:
                    t['completed'] = True
                    break
            save_todos(todos)
            self.load_next_flow_task()

    def action_command_palette(self) -> None:
        from textual.command import CommandPalette
        self.push_screen(CommandPalette())

    def action_enter_flow(self) -> None:
        if self.flow_state == "IDLE":
            self.flow_state = "DEEP"

    def action_exit_flow(self) -> None:
        self.flow_state = "IDLE"

    def action_pause_timer(self) -> None:
        selector = "#flow-pomo" if self.flow_state == "DEEP" else "#pomodoro"
        try: self.query_one(selector, PomodoroPanel).handle_toggle()
        except: pass

    def action_add_todo(self) -> None:
        if self.flow_state == "IDLE":
            try: self.query_one(TodoPanel).focus_input()
            except: pass

    def action_toggle_help(self) -> None:
        if self.flow_state == "IDLE": self.push_screen(HelpScreen())

    def action_toggle_info(self) -> None:
        if self.flow_state == "IDLE": self.push_screen(InfoScreen())

if __name__ == "__main__":
    TermFlowApp().run()
