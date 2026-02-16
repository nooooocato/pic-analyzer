# Implementation Plan - Fluent Design Migration

## Phase 1: Foundation [checkpoint: 006e58a]
- [x] Task: Install `PySide6-Fluent-Widgets` and update `requirements.txt`. [a3d8224]
- [x] Task: Refactor `src/ui/theme.py` to integrate with `qfluentwidgets` theme system (Ensure compatibility with existing QMainWindow). [b047c94]
- [ ] Task: Conductor - User Manual Verification 'Phase 1' (Protocol in workflow.md)

## Phase 2: Atomic Components [checkpoint: bcc93d9]
- [x] Task: Replace `IconButton` with `TransparentToolButton` / `tool_button`. [2f510ae]
    - Update `src/ui/common/icon_button/`.
- [x] Task: Replace `Card` with `SimpleCardWidget` or `CardWidget`. [a74e7bf]
    - Update `src/ui/common/card/`.
- [x] Task: Replace `Toast` with `InfoBar`. [f311368, ad4bc07]
    - Refactor `src/ui/common/toast/` to wrap `InfoBar.success/warning/error`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2' (Protocol in workflow.md)

## Phase 3: Overlays & Specialized UI [checkpoint: 7b9d55e]
- [x] Task: Refactor `SelectionOverlay` to use `Flyout` or `TeachingTip`. [9385fef]
- [x] Task: Refactor `SortOverlay` to use `CommandBar` or `DropDownMenu`. [9385fef, 0702038, 084b833, 1b5e388]
    - Ensure sorting logic connected in previous track is preserved.
- [x] Task: Conductor - User Manual Verification 'Phase 3' (Protocol in workflow.md) [7b9d55e]

## Phase 4: Complex Views [checkpoint: 8d58018]
- [x] Task: Update `GalleryView` styling. [37c82a9]
    - Apply Fluent styles to `QListWidget` (or switch to `ListWidget` from library).
    - Ensure `GalleryItemDelegate` plays nicely with Fluent selection styles.
- [x] Task: Update `ImageViewer`. [46cb66e, 26f6e4f, 6e2c9d6]
    - Use Fluent buttons for navigation.
    - Ensure background transparency/blur works.
- [x] Task: Conductor - User Manual Verification 'Phase 4' (Protocol in workflow.md) [8d58018]

## Phase 5: Main Window Integration
- [ ] Task: Migrate `MainWindow` to `FluentWindow`.
    - Replace `QMainWindow` with `FluentWindow`.
    - Setup `NavigationInterface` (Sidebar) if applicable, or keep current Toolbar structure using Fluent equivalent.
- [ ] Task: Conductor - User Manual Verification 'Phase 5' (Protocol in workflow.md)

## Phase 6: Cleanup & Verification
- [ ] Task: Remove obsolete QSS code from `src/ui/theme.py`.
- [ ] Task: Run full regression tests.
- [ ] Task: Conductor - User Manual Verification 'Phase 6' (Protocol in workflow.md)
