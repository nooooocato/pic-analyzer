# Implementation Plan: Image Viewer & Multi-Selection Mode

## Phase 1: Multi-Selection Foundations & Toolbar
- [x] Task: Extend `GalleryView` (QListWidget) to support selection mode UI. [0a1b2c3]
    - [x] Write Tests: Verify items can display checkboxes and borders when selected.
    - [x] Implement: Update `src/ui/gallery_view.py` stylesheets and item delegates to show selection feedback.
- [x] Task: Add selection batch controls to `MainWindow` toolbar. [4d5e6f7]
    - [x] Write Tests: Verify "Select All", "Invert", and "Cancel" buttons exist and are initially hidden.
    - [x] Implement: Update `src/ui/main_window.py` to include a context-sensitive toolbar section.
- [x] Task: Implement selection triggers (Long-press & Right-click). [8g9h0i1]
    - [x] Write Tests: Verify selection mode is activated via simulated long-press or context menu.
    - [x] Implement: Add event handlers for long-press and a custom context menu in `GalleryView`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Multi-Selection Foundations & Toolbar' (Protocol in workflow.md)

## Phase 2: Image Viewer Overlay & Navigation
- [x] Task: Create the `ImageViewer` overlay widget. [a1b2c3d]
    - [x] Write Tests: Verify the overlay covers the gallery and has a dimming effect.
    - [x] Implement: Create `src/ui/image_viewer.py` as a semi-transparent overlay widget.
- [x] Task: Add controls to the `ImageViewer`. [b2c3d4e]
    - [x] Write Tests: Verify Top-left Back button and Next/Prev buttons are present and functional.
    - [x] Implement: Add `QPushButton` instances for navigation and exit.
- [~] Task: Implement Viewer pop-up and close animations.
    - [ ] Write Tests: Verify `QPropertyAnimation` is triggered on open/close.
    - [ ] Implement: Use `QVariantAnimation` or `QPropertyAnimation` for smooth opacity/scale transitions.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Image Viewer Overlay & Navigation' (Protocol in workflow.md)

## Phase 3: Input Handling & Integration
- [x] Task: Implement Mouse 4/5 and Keyboard navigation. [c3d4e5f]
    - [x] Write Tests: Verify Mouse 4/5 and Arrow keys correctly trigger back/forward actions.
    - [x] Implement: Override `keyPressEvent` and `mousePressEvent` in `MainWindow` and `ImageViewer`.
- [x] Task: Integrate Gallery with Viewer. [f6g7h8i]
    - [x] Write Tests: Verify double-clicking an item opens the viewer with the correct image.
    - [x] Implement: Connect `GalleryView` signals to launch the overlay with index-based image loading.
- [x] Task: Implement rubber-band selection in `GalleryView`. [j9k0l1m]
    - [x] Write Tests: Verify dragging across items updates the selection state.
    - [x] Implement: Enable `RubberBandSelection` in `QListWidget` and connect to selection mode logic.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Input Handling & Integration' (Protocol in workflow.md)

## Phase 4: Final Refinement & Performance
- [x] Task: Optimize animation performance. [k2l3m4n]
    - [x] Write Tests: Profile UI responsiveness during rapid pagination.
    - [x] Implement: Ensure image loading in the viewer uses lazy-loading or background caching.
- [x] Task: Conductor - User Manual Verification 'Phase 4: Final Refinement & Performance' (Protocol in workflow.md)
