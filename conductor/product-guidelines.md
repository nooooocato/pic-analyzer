# Product Guidelines - Pic-Analyzer

## Visual Identity & UX
- **Design System:** Windows 11 Modern Fluent Design (via PyQt/PySide styling).
- **Layout Philosophy:** Utility-first, high data density. Prioritize information visibility over white space.
- **Image Display:** Lazy loading for thumbnails. Smooth transitions between tiled and original views.
- **Interactivity:** Distribution charts must be interactive, serving as primary filtering mechanisms.

## Communication & Feedback
- **Tone:** Succinct and action-oriented. Provide clear next steps for the user.
- **Error Handling:** Hide complex technical details behind "Show More" or "View Logs" to maintain a clean UI, while still being precise.
- **Conflict Resolution:** Mandatory interactive prompts for filename conflicts during "Move" operations (Rename, Skip, Overwrite).

## Component Standards
- **Data Inspector:** Hierarchical tree view to organize metrics (pHash, File System, Metadata). Now a standalone, reactive widget.
- **Component Communication:** Strictly use the global `Communicator` signal bus for cross-component notifications and state changes to maintain decoupling.
- **Toolbar:** Dynamic generation of buttons based on available statistical plugins.
- **File Operations:** Strictly use "Move" (atomic if possible) to minimize disk I/O and wear.

## Technical Principles
- **Extensibility:** Every statistical rule must be a self-contained plugin.
- **Performance:** Multi-threaded execution for analysis; main thread remains responsive for UI/Preview.
- **Data Integrity:** Analysis results are auxiliary (stored in SQLite) and must never modify the original image files.
