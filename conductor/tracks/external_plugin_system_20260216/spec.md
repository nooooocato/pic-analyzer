# Track Specification: Externalized Plugin System with Dynamic UI Injection

## Overview
This track involves a significant architectural shift in the plugin system. The goal is to move all plugins (both built-in and third-party) from `src/plugins` to a root-level `plugins` directory. Furthermore, the system will be enhanced to allow plugins to define and inject their own UI components dynamically into the main application.

## Functional Requirements
- **Externalized Storage:** All plugins must reside in the `./plugins` directory relative to the application's execution path.
- **Unified Structure:** Plugins will follow a categorized structure (e.g., `./plugins/sort/`) and package both their algorithm and UI components within the same directory/module (e.g., `algo.py` and `ui.py`).
- **Dynamic UI Injection:** 
    - Plugins will receive a reference to the `MainWindow` or specific container widgets during their initialization.
    - Plugins are responsible for programmatically adding their UI elements (buttons, menus, etc.) to the layout.
- **Conflict Management:** If multiple plugins share the same ID or name, the system must log an error and refuse to load either to prevent unpredictable behavior.
- **Clean Migration:** The existing loading logic in `src/plugins` will be replaced by a new system targeting only the root `./plugins` directory.

## Non-Functional Requirements
- **Robustness:** Failure to load one plugin (e.g., due to a conflict or malformed code) should not prevent other valid plugins from loading.
- **Extensibility:** The dynamic injection mechanism should be generic enough to allow plugins to attach themselves to various parts of the UI (toolbar, sidebar, context menus).

## Acceptance Criteria
- [ ] No plugins remain in `src/plugins`.
- [ ] The application successfully discovers and loads plugins from the root `./plugins` directory.
- [ ] Plugins can successfully add a button or widget to the main UI.
- [ ] An error is logged and loading is halted for plugins with conflicting identifiers.
- [ ] Existing sorting functionality (currently in `src/plugins/sort`) is migrated and working as external plugins.

## Out of Scope
- Automatic download or installation of third-party plugins.
- Advanced sandboxing for third-party plugin code (plugins will have full access to the provided UI references).
