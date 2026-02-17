# Specification: Architecture Refactoring - Plugin System & App/UI Separation

## Overview
This track focuses on structural refactoring to improve maintainability, testability, and separation of concerns. The goals are twofold:
1.  **Plugin System Refinement:** Decouple the base plugin classes and management logic from specific implementations, centralizing them in `src/plugin/`.
2.  **App/UI Separation:** Extract business logic, global state, and core utilities (DB, File Ops, Logging) from the `MainWindow` logic into a dedicated `src/app/` module, transforming the `MainWindow` into a pure view/controller delegate.

## Functional Requirements

### 1. Plugin System Refactoring (`src/plugin/`)
-   **Structure:** Relocate the existing `PluginBase` and `PluginManager` (or equivalent) to `src/plugin/`.
-   **Separation:** Explicitly separate core management logic from "Statistical Rules" plugins (pHash, Color, File Size, etc.).
-   **Discovery:** Ensure the `PluginManager` can discover and load plugins from the established plugin directory while maintaining the current design of base classes.

### 2. App/UI Separation (`src/app/`)
-   **Global State:** Centralize application-wide state (e.g., current workspace, registered plugins, active analysis) in `src/app/`.
-   **Core Services:** Move the following to `src/app/`:
    -   **Database Operations:** SQLite handling and data access objects.
    -   **File Operations:** Safe "move" logic and SSD wear-leveling management.
    -   **Logging:** Centralized application logging.
-   **Application Entry:** Move the program's main entry point and initialization logic to `src/app/`.

### 3. UI Logic Decoupling (`src/ui/`)
-   **Refactor `src/ui/main_window/logic.py`:** Strip business logic from this file.
-   **View Responsibility:** The `MainWindow` UI class should handle:
    -   Qt signals and widget interactions.
    -   Layout and styling.
    -   UI-specific state (e.g., active tabs, view modes).
-   **Delegation:** Delegate all application-level operations (workspace loading, starting analysis, file manipulation) to the appropriate classes in `src/app/`.

## Non-Functional Requirements
-   **Testability:** Core services in `src/app/` (DB, File Ops) must be unit-testable without requiring a Qt event loop where possible.
-   **Maintainability:** Reduced complexity in `src/ui/` files.
-   **Backward Compatibility:** Maintain current plugin base/manager design patterns to minimize impact on existing plugin implementations.

## Acceptance Criteria
-   [ ] `src/ui/main_window/logic.py` is reduced to UI delegation and event handling.
-   [ ] All statistical plugins are discovered and loaded correctly from the new `src/plugin/` structure.
-   [ ] Application initializes successfully using the new `src/app/` entry point and global state.
-   [ ] Unit tests for `src/app/` components (Database, File Ops) pass independently of the UI.
-   [ ] The application remains fully functional (file operations, analysis, preview) after refactoring.

## Out of Scope
-   Adding new statistical rules or features.
-   Major UI redesign or changing the look and feel.
-   Changing the underlying SQLite schema (unless required for refactoring).
