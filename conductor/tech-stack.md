# Tech Stack - Pic-Analyzer

## Core Technologies
- **Language:** Python 3.10+ (for modern typing and concurrency support)
- **UI Framework:** PySide6 (Qt for Python) - Chosen for its native Windows integration and support for modern Fluent Design styles.
- **Database:** SQLite - Used for local, high-performance storage of image analysis results and metadata.

## Image Processing & Media
- **Pillow (PIL):** Primary library for image loading, thumbnail generation, and basic manipulation.
- **Qt Media:** `QMovie` for high-performance playback of animated formats (GIF, WebP).
- **Custom UI Rendering:** `QStyledItemDelegate` for optimized, overlaid UI components (checkboxes, selection states).
- **OpenCV:** Used for advanced analysis like pHash (similarity) and color space calculations.
- **ImageHash:** Specialized library for pHash, dHash, and other perceptual hashing algorithms.

## Data Visualization
- **PyQtGraph:** Selected for high-performance, interactive 2D charts (histograms, scatter plots) that integrate smoothly with the Qt event loop.
- **NumPy:** Used for efficient statistical calculations (Mean, Standard Deviation) in sorting algorithms.

## Architecture & Infrastructure
- **UI Architecture:** "Triple-Python Pattern" - Strict separation of concerns for UI components:
    - `xxx.style.py`: Pure styling, colors, and QSS fragments.
    - `xxx.layout.py`: Pure widget hierarchy and static initialization.
    - `xxx.logic.py`: Component entry point, signal/slot handling, and orchestration.
- **Concurrency:** `QThreadPool` and `QRunnable` for multi-threaded, non-blocking image analysis.
- **Plugin System:** Python's `importlib` and factory pattern for dynamic loading of statistical rules.
- **Storage:** Safe file operations using Python's `shutil.move` with manual conflict resolution logic.

## Distribution
- **Packaging:** PyInstaller - To package the application into a standalone Windows executable.
