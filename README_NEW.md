# TermFlow

**TermFlow** is a production-grade, minimalist terminal productivity dashboard built entirely in Python using the [Textual](https://textual.textualize.io/) framework. Designed for developers and terminal enthusiasts, it provides a distraction-free environment to manage your time and tasks.

## Features

- **Live Dashboard**: Real-time clock and date display.
- **Task Management**: Persistent todo list with colored tags (`[dev]`, `[school]`, `[life]`).
- **Deep Work**: Integrated Pomodoro timer with session tracking.
- **Contextual Info**: Live weather updates and motivational quotes.
- **Keyboard-First**: Optimized for speed with comprehensive keybindings.
- **Lightweight & Portable**: Zero bloat, file-based persistence, and low resource usage.

## Installation

Ensure you have Python 3.8+ installed.

```bash
pip install textual requests
```

## Usage

Launch the dashboard directly from your terminal:

```bash
python main.py
```

### Keybindings

- `?` : Toggle Help Overlay
- `q` : Quit Application
- `Tab` : Cycle focus between panels
- `Enter` : Add todo / Toggle task status
- `s` : Start/Pause Pomodoro
- `r` : Reset Pomodoro

## Axoninnoova: The Future of Automation

TermFlow is proud to be part of the **Axoninnoova** ecosystem. We believe in the power of automation and minimalist tooling to multiply human productivity. Our community is dedicated to building the next generation of developer tools that are fast, reliable, and stay out of your way.

## Technical Details

TermFlow is a minimal terminal productivity dashboard built with Python and the Textual TUI framework. It provides a live, interactive terminal interface combining several productivity tools: a real-time clock, a persistent todo list, a Pomodoro timer, and an info panel displaying weather and motivational quotes.

The application is designed to run entirely in the terminal, offering a distraction-free productivity environment without needing a web browser or GUI.

### System Architecture
- **Framework**: Textual (Python TUI framework built on Rich)
- **Layout**: Grid-based panel system with four main components
- **Styling**: Custom TCSS stylesheet (`styles.tcss`)
- **Data Storage**: Simple JSON file (`todos.json`) for persistence

## Credits

- **Atharv**: Founder & Lead Architect.
- **Axoninnoova Community**: For the continuous feedback and support.

Join our community: [https://dsc.gg/axoninnova](https://dsc.gg/axoninnova)

## License

MIT © 2026 TermFlow
