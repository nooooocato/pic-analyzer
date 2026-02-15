# Implementation Plan - Fluent Design Migration

## Phase 1: Foundation & Main Window
- [x] Task: Install `PySide6-Fluent-Widgets` and update `requirements.txt`. [a3d8224]
- [ ] Task: Refactor `src/ui/theme.py` to integrate with `qfluentwidgets` theme system.
- [ ] Task: Migrate `MainWindow` to `FluentWindow`.
    - Replace `QMainWindow` with `FluentWindow`.
    - Setup `NavigationInterface` (Sidebar) if applicable, or keep current Toolbar structure using Fluent equivalent.

## Phase 2: Common Components Replacement
- [ ] Task: Replace `IconButton` with `TransparentToolButton` / `tool_button`.
    - Update `src/ui/common/icon_button/`.
- [ ] Task: Replace `Card` with `SimpleCardWidget` or `CardWidget`.
    - Update `src/ui/common/card/`.
- [ ] Task: Replace `Toast` with `InfoBar`.
    - Refactor `src/ui/common/toast/` to wrap `InfoBar.success/warning/error`.

## Phase 3: Overlays & Specialized UI
- [ ] Task: Refactor `SelectionOverlay` to use `Flyout` or `TeachingTip`.
- [ ] Task: Refactor `SortOverlay` to use `CommandBar` or `DropDownMenu`.
    - Ensure sorting logic connected in previous track is preserved.

## Phase 4: Gallery & Complex Views
- [ ] Task: Update `GalleryView` styling.
    - Apply Fluent styles to `QListWidget` (or switch to `ListWidget` from library).
    - Ensure `GalleryItemDelegate` plays nicely with Fluent selection styles.
- [ ] Task: Update `ImageViewer`.
    - Use Fluent buttons for navigation.
    - Ensure background transparency/blur works with `FluentWindow`.

## Phase 5: Cleanup & Verification
- [ ] Task: Remove obsolete QSS code from `src/ui/theme.py`.
- [ ] Task: Run full regression tests.
