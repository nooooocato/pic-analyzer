# Implementation Plan - Fluent Design Migration

## Phase 1: Foundation
- [x] Task: Install `PySide6-Fluent-Widgets` and update `requirements.txt`. [a3d8224]
- [x] Task: Refactor `src/ui/theme.py` to integrate with `qfluentwidgets` theme system (Ensure compatibility with existing QMainWindow). [b047c94]
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Atomic Components
- [ ] Task: Replace `IconButton` with `TransparentToolButton` / `tool_button`.
    - Update `src/ui/common/icon_button/`.
- [ ] Task: Replace `Card` with `SimpleCardWidget` or `CardWidget`.
    - Update `src/ui/common/card/`.
- [ ] Task: Replace `Toast` with `InfoBar`.
    - Refactor `src/ui/common/toast/` to wrap `InfoBar.success/warning/error`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Overlays & Specialized UI
- [ ] Task: Refactor `SelectionOverlay` to use `Flyout` or `TeachingTip`.
- [ ] Task: Refactor `SortOverlay` to use `CommandBar` or `DropDownMenu`.
    - Ensure sorting logic connected in previous track is preserved.
- [ ] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md)

## Phase 4: Complex Views
- [ ] Task: Update `GalleryView` styling.
    - Apply Fluent styles to `QListWidget` (or switch to `ListWidget` from library).
    - Ensure `GalleryItemDelegate` plays nicely with Fluent selection styles.
- [ ] Task: Update `ImageViewer`.
    - Use Fluent buttons for navigation.
    - Ensure background transparency/blur works.
- [ ] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md)

## Phase 5: Main Window Integration
- [ ] Task: Migrate `MainWindow` to `FluentWindow`.
    - Replace `QMainWindow` with `FluentWindow`.
    - Setup `NavigationInterface` (Sidebar) if applicable, or keep current Toolbar structure using Fluent equivalent.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

## Phase 6: Cleanup & Verification
- [ ] Task: Remove obsolete QSS code from `src/ui/theme.py`.
- [ ] Task: Run full regression tests.
- [ ] Task: Conductor - User Manual Verification 'Phase 6' (Protocol in workflow.md)
