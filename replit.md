# TermFlow

## Overview

TermFlow is a minimal terminal productivity dashboard built with Python and the Textual TUI framework. It provides a live, interactive terminal interface combining several productivity tools: a real-time clock, a persistent todo list, a Pomodoro timer, and an info panel displaying weather and motivational quotes.

The application is designed to run entirely in the terminal, offering a distraction-free productivity environment without needing a web browser or GUI.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Textual (Python TUI framework built on Rich)
- **Layout**: Grid-based panel system with four main components
  - ClockPanel: Real-time clock with 1-second update interval
  - TodoPanel: Task management with input and list view
  - PomodoroPanel: 25-minute timer with start/pause/reset controls
  - InfoPanel: Weather and quotes display with async data fetching
- **Styling**: Custom TCSS stylesheet (`styles.tcss`) for terminal UI styling
- **Entry Point**: `main.py` → `TermFlowApp` class

### Panel Components
Each panel is a self-contained `Static` widget that manages its own state and rendering:
- Panels use Textual's reactive system for state updates
- Background workers handle async operations (API calls) to prevent UI blocking
- Rich markup is used for text formatting (colors, bold, etc.)

### Data Storage
- **Todo Persistence**: Simple JSON file (`todos.json`) in the project root
- **Schema**: Array of objects with `text` (string) and `completed`/`done` (boolean) fields
- **No Database**: File-based storage keeps the application simple and portable

### External Data Fetching
- Weather and quotes are fetched asynchronously on panel mount
- Graceful error handling with fallback messages when APIs are unavailable
- Timeout settings (5 seconds) prevent hanging on slow connections

## External Dependencies

### Python Packages
- **Textual**: Terminal UI framework for building the dashboard interface
- **Requests**: HTTP client for fetching weather and quotes from external APIs

### External APIs
- **Open-Meteo Weather API**: Free weather API, hardcoded to NYC coordinates (40.7128, -74.0060)
  - Endpoint: `https://api.open-meteo.com/v1/forecast`
  - Returns current temperature and wind speed
- **DummyJSON Quotes API**: Random motivational quotes
  - Endpoint: `https://dummyjson.com/quotes/random`
  - Returns quote text and author

### File Dependencies
- `todos.json`: Local file for todo persistence (created automatically if missing)
- `termflow/ui/styles.tcss`: Textual CSS stylesheet for UI styling