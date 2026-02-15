# Implementation Plan - Advanced Sorting Plugins

## Phase 1: Sorting Plugin Framework [checkpoint: ]
- [x] Task: Define the `BaseSortPlugin` interface. 043e03d
    - [ ] Create `src/plugins/sort/base.py`.
    - [ ] Define methods for calculating order based on a list of values.
- [ ] Task: Implement `SortPluginManager`.
    - [ ] Create `src/plugins/sort/manager.py` for dynamic loading of sorting algorithms.
    - [ ] Write Tests: Verify plugins are correctly discovered and loaded from `src/plugins/sort/`.
- [ ] Task: Implement basic sorting plugins.
    - [ ] Create `src/plugins/sort/ascending.py`.
    - [ ] Create `src/plugins/sort/descending.py`.
    - [ ] Write Tests: Verify correct ordering for simple numeric sets.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Sorting Plugin Framework' (Protocol in workflow.md)

## Phase 2: Statistical Sorting & Logic [checkpoint: ]
- [ ] Task: Implement the Normal Distribution (Peak First) plugin.
    - [ ] Create `src/plugins/sort/normal_dist.py`.
    - [ ] Implement Mean (μ) and Sigma (σ) calculation using `numpy`.
    - [ ] Write Tests: Verify items are sorted by proximity to the mean.
- [ ] Task: Enhance `MainWindow` to extract numeric metrics from the database.
    - [ ] Update `src/database.py` or `MainWindow` to fetch all numeric analysis result keys.
    - [ ] Write Tests: Ensure only numeric columns/results are identified as sortable metrics.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Statistical Sorting & Logic' (Protocol in workflow.md)

## Phase 3: Floating Sort UI [checkpoint: ]
- [ ] Task: Create the `SortOverlay` widget.
    - [ ] Implement a floating button in the top-right of `GalleryView`.
    - [ ] Implement a menu to select Metric and Algorithm.
    - [ ] Write Tests: Verify the overlay is visible and the menu contains the expected items.
- [ ] Task: Integrate sorting with `GalleryView`.
    - [ ] Update `GalleryView` to trigger the selected sort plugin and refresh the layout.
    - [ ] Handle re-sorting across multiple groups if applicable.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Floating Sort UI' (Protocol in workflow.md)

## Phase 4: Debug Stats & Refinement [checkpoint: ]
- [ ] Task: Implement the "Show Stats" toggle and display.
    - [ ] Add the toggle to the `SortOverlay` or View menu.
    - [ ] Update `GalleryView` to display Mean/Sigma labels at the end of groups when enabled.
    - [ ] Write Tests: Verify labels are shown/hidden based on the toggle state.
- [ ] Task: Performance optimization for large galleries.
    - [ ] Ensure sorting calculations don't freeze the UI.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Debug Stats & Refinement' (Protocol in workflow.md)
