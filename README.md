# Pic-Analyzer

A sophisticated image gallery and analysis tool built with PySide6, featuring a modern refactored UI and an extensible plugin system.

## Features

- **Modern UI**: Clean, responsive interface with a card-based gallery view and integrated image viewer.
- **Plugin System**: Easily extend functionality with custom sorting and grouping algorithms.
- **Database Backed**: Efficiently manage image metadata and metrics using SQLite.
- **Fast Thumbnails**: Optimized thumbnail generation and caching.

## Project Structure

- `src/`: Core application logic and UI components.
  - `ui/`: Refactored UI components using a logic/layout/style separation pattern.
  - `plugin_manager.py`: Dynamic loading and management of plugins.
- `plugins/`: External plugins for sorting and grouping.
  - `sort/`: Sorting plugins (e.g., Ascending, Descending, Normal Distribution).
  - `group/`: Grouping plugins (e.g., Date Grouping).
- `tests/`: Comprehensive test suite including unit and integration tests.

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python run_app.py
   ```

## Development

The project uses the **Conductor** framework for spec-driven development. Project documentation and track plans are located in the `conductor/` directory.

### Testing

Run tests using pytest:
```bash
$env:PYTHONPATH=".;plugins"; pytest
```
