from textual.app import App, ComposeResult
from textual.widgets import Header, Footer
from termflow.panels.clock import Clock
from termflow.panels.todo_list import TodoPanel
from termflow.panels.pomodoro import PomodoroPanel
from termflow.panels.info_panel import InfoPanel

class TermFlowApp(App):
    """A Terminal Productivity Dashboard."""

    CSS_PATH = "styles.tcss"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        # Grid Layout defined in CSS:
        # Col 1: TodoPanel (Spans 2 rows)
        # Col 2, Row 1: Clock & Info (Actually let's split this)
        
        # Adjusting layout strategy:
        # We can yield containers or just widgets if CSS grid handles it.
        # CSS grid: 2 cols. 
        # Item 1: TodoPanel (row-span 2) -> Left side
        # Item 2: Clock -> Top Right
        # Item 3: Pomodoro -> Middle Right (wait, let's reorganize)
        
        # Let's use containers to be explicit if needed, but CSS grid is powerful.
        # Let's try:
        # Left Col: Todo List
        # Right Col: Clock (Top), Pomodoro (Mid), Info (Bottom)
        
        # Updating CSS to match this thought:
        # grid-template-areas: 
        #   "todo clock"
        #   "todo pomodoro"
        #   "todo info";
        
        # But for simplicity with the current CSS (2x2):
        # TodoPanel (Left, Row 1-2)
        # Clock (Right, Row 1)
        # Pomodoro (Right, Row 2)
        # Info (Right, Row 2 - wait, need 3 slots on right?)
        
        # Let's stick to the CSS I wrote: 2 cols, 2 rows.
        # TodoPanel (row-span 2)
        # Clock
        # Pomodoro
        
        # Wait, I forgot InfoPanel in that mental model.
        # Let's put Clock and Info together or adjust grid.
        
        # REVISION:
        # Left: TodoPanel
        # Right Top: Clock
        # Right Middle: Pomodoro
        # Right Bottom: Info
        
        # I'll update styles.tcss in a subsequent step if needed, but let's try to fit them.
        yield TodoPanel()
        yield Clock()
        yield PomodoroPanel()
        yield InfoPanel()
        
        yield Footer()

if __name__ == "__main__":
    app = TermFlowApp()
    app.run()
