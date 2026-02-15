# Implementation Plan - UI Refactor (Triple-Python Pattern)

## Phase 1: Foundation & Common Components [checkpoint: 2464f53]
- [x] Task: Initialize Global Theme System. (147bba8)
    - [ ] Create `src/ui/theme.py` with standard colors, spacing, and shared QSS fragments.
- [x] Task: Refactor Small Reusable Components. (45fd835)
    - [ ] Identify common widgets (e.g., custom buttons, status labels).
    - [ ] Create `src/ui/common/` and implement the Style/Layout/Logic triplet for each.
    - [ ] Write Tests: Create `tests/ui_refactor/test_common.py`.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Common Components' (Protocol in workflow.md)

## Phase 2: Overlays & Specialized Widgets [checkpoint: ]
- [x] Task: Refactor Selection Overlay. (8752abe)
    - [ ] Create `src/ui/overlays/selection/` with Style/Layout/Logic triplets.
    - [ ] Migrate batch action logic (Select All, Invert, etc.) to Logic layer.
- [x] Task: Refactor Sort Overlay. (c01bab3)
    - [ ] Create `src/ui/overlays/sort/` with Style/Layout/Logic triplets.
    - [ ] Integrate SortPluginManager logic into the Logic layer.
- [x] Task: Write Tests for Overlays. (c01bab3)
    - [ ] Create `tests/ui_refactor/test_overlays.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Overlays & Specialized Widgets' (Protocol in workflow.md)

## Phase 3: Complex Views (Gallery & Viewer) [checkpoint: ]
- [ ] Task: Refactor Image Viewer.
    - [ ] Create `src/ui/image_viewer/` with Style/Layout/Logic triplets.
    - [ ] Move animation and navigation logic to the Logic layer.
- [ ] Task: Refactor Gallery View & Grouping.
    - [ ] Create `src/ui/gallery/` with Style/Layout/Logic triplets for `GroupedListWidget` and `GalleryView`.
    - [ ] Ensure item delegate rendering is handled in the Style layer.
- [ ] Task: Write Tests for Complex Views.
    - [ ] Create `tests/ui_refactor/test_views.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Complex Views' (Protocol in workflow.md)

## Phase 4: Main Window & Integration [checkpoint: ]
- [ ] Task: Refactor Main Window.
    - [ ] Create `src/ui/main_window/` with Style/Layout/Logic triplets.
    - [ ] Move Menu/Toolbar assembly to Layout; Move scanner/database orchestration to Logic.
- [ ] Task: Big Bang Integration & Cleanup.
    - [ ] Update `run_app.py` to launch the new `MainWindow` logic class.
    - [ ] Verify all inter-component signals (Gallery -> Viewer, etc.) are restored.
    - [ ] Delete legacy files in `src/ui/` after verification.
- [ ] Task: Final Regression Test.
    - [ ] Run full test suite (new and legacy) to ensure zero feature loss.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Main Window & Integration' (Protocol in workflow.md)
