# Tech Stack - Pic-Analyzer

## Core Technologies
- **Language:** Python 3.10+ (for modern typing and concurrency support)
- **UI Framework:** PySide6 (Qt for Python) - Chosen for its native Windows integration and support for modern Fluent Design styles.
- **Database & ORM:** SQLite with **Peewee ORM** - Provides type-safe, structured access to Workspace, Image, AnalysisResult, and SidebarState models.

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
- **Concurrency:** `QThreadPool` and `QRunnable` for multi-threaded, non-blocking image analysis.
- **Centralized State:** Dedicated `src/app/state.py` for global application state and service management.
- **Logic Engines:** 
    - **FilterEngine:** Dedicated processor for evaluating sequential AND/OR boolean chains for image selection.
- **Plugin System:** 
    - **Core Abstraction:** Base classes located in `src/plugin/` for better separation from UI.
    - **Externalized Discovery:** Plugins reside in the root-level `./plugins` directory and are discovered recursively at runtime.
    - **Categorization:** Automatic categorization of plugins into `sort`, `group`, `filter`, and `general`.
    - **Metadata-Driven UI:** Plugins define a `schema` (parameters, types, defaults) used by the sidebar to automatically generate control widgets.
    - **Logic-UI Decoupling:** Plugins focus exclusively on data processing; presentation is handled centrally by the Sidebar Container.
- **Storage:** Safe file operations using Python's `shutil.move` with manual conflict resolution logic.

## Testing Architecture
- **Framework:** `pytest` - Used for unit and integration testing.
- **Decentralized Testing:** Plugin-specific tests are co-located within their respective packages in `./plugins/` to ensure modularity and autonomy.
- **Mirrored Structure:** Core tests in `./tests/` mirror the `src/` directory structure for high discoverability and maintainability.

## Distribution
- **Packaging:** PyInstaller - To package the application into a standalone Windows executable.
