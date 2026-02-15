# Track Specification: UI Refactor - PySide6 Modular Style

## 1.0 Overview
This track involves a comprehensive refactor of the existing Pic-Analyzer UI to adhere to the newly established **"Triple-Python Pattern"**. The goal is to separate concerns into dedicated Style, Layout, and Logic layers, improving maintainability, testability, and adherence to Fluent Design principles. This will be a "Big Bang" refactor, replacing the current UI structure with a component-based folder hierarchy.

## 2.0 Functional Requirements

### 2.1 Triple-Python Pattern Implementation
Every major UI component must be split into:
- **`xxx.style.py`**: Pure styling, colors, and QSS constants.
- **`xxx.layout.py`**: Pure widget hierarchy and initialization (no business logic).
- **`xxx.logic.py`**: The entry point class handling signals, slots, and data flow.

### 2.2 Component Hierarchy & Folders
Existing UI code in `src/ui/` will be moved into component-specific directories:
- `src/ui/common/` (Small reusable widgets)
- `src/ui/overlays/` (SelectionOverlay, SortOverlay)
- `src/ui/image_viewer/`
- `src/ui/gallery/` (GroupedListWidget, GalleryView)
- `src/ui/main_window/`

### 2.3 Global Theme System
- Implement `src/ui/theme.py` to house shared constants (e.g., `#f3f3f3` background, Fluent accent colors, standard spacing/radii).
- All component style files must import from this theme file to ensure application-wide consistency.

### 2.4 Bottom-Up Refactor Strategy
The implementation will proceed from the smallest units to the largest:
1. Reusable components (buttons, labels).
2. Overlays and specialized widgets.
3. Complex views (Gallery, Viewer).
4. Main Window and integration.

## 3.0 Technical Requirements
- **Strict Separation:** No business logic in `.layout.py`; no UI initialization in `.logic.py` beyond calling the layout setup.
- **Dynamic Properties:** Use `setProperty("class", "...")` for CSS-like styling instead of deep object name selectors.
- **Resource Management:** Ensure all icons and assets are handled via strictly relative paths or the Qt Resource system.
- **Type Hinting:** Layout files must provide full type hinting for widgets so Logic files have complete IDE support.

## 4.0 Acceptance Criteria
- [ ] Application launches and all existing features (Gallery, Viewer, Selection, Sorting) function exactly as before.
- [ ] No `.ui` or external `.qss` files exist in the source tree.
- [ ] Every UI component follows the folder-based triplet structure.
- [ ] A new parallel test suite in `tests/ui_refactor/` verifies the logic of the new components.
- [ ] `src/ui/theme.py` is the single source of truth for global styling constants.

## 5.0 Out of Scope
- Introducing new features or changing the existing user workflow.
- Database schema changes or backend logic refactoring.
