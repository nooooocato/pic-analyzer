# Implementation Plan - Sidebar & Plugin Refactor

## Phase 1: Foundation & Sidebar UI
- [ ] Task: Create the new Sidebar Container component and its integration with the Main Window layout.
    - [ ] Implement the base `SidebarContainer` widget in `src/ui/common/sidebar.py`.
    - [ ] Integrate the sidebar into `src/ui/main_window/layout.py`.
- [ ] Task: Create Collapsible Section widget.
    - [ ] Implement a reusable `CollapsibleSection` component that can host other widgets.
    - [ ] Add 'Grouping', 'Filtering', and 'Sorting' sections to the sidebar.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Foundation & Sidebar UI' (Protocol in workflow.md)

## Phase 2: Core Architecture & Plugin Interface Refactor
- [ ] Task: Define the new Plugin Schema and Base Classes in `src/plugin/base.py`.
    - [ ] Design the `PluginSchema` data structure (TypedDict/JSON-like).
    - [ ] Update `BasePlugin`, `SortPlugin`, and `GroupPlugin` to use logic-only methods.
- [ ] Task: Refactor the Plugin Manager to support Schema-based discovery.
    - [ ] Update `src/plugin/manager.py` to handle the new metadata-driven approach.
- [ ] Task: Migrate existing Sorting plugins (Ascending, Descending, Normal Dist) to the new interface.
    - [ ] Rewrite `algo.py` and `ui.py` (or merge logic into `algo.py`) for existing plugins.
- [ ] Task: Migrate existing Grouping plugins (Date Grouping) to the new interface.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core Architecture & Plugin Interface Refactor' (Protocol in workflow.md)

## Phase 3: Dynamic UI Generation & Interaction
- [ ] Task: Implement Sidebar Rule Dropdowns for each section.
    - [ ] Dynamically populate dropdowns with discovered plugins from the manager.
    - [ ] Implement 'Live Update' logic when a new rule is selected.
- [ ] Task: Create Dynamic Widget Generator.
    - [ ] Implement a factory that maps schema types (int, str, choice) to PySide6 widgets.
    - [ ] Ensure widgets are correctly styled and sized for the sidebar.
- [ ] Task: Implement Parameter Interaction & 'Apply' Button.
    - [ ] Add an 'Apply' button that only appears/enables when parameters are modified.
    - [ ] Handle state synchronization between sidebar widgets and plugin logic.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Dynamic UI Generation & Interaction' (Protocol in workflow.md)

## Phase 4: Filtering & Metadata Implementation
- [ ] Task: Implement the 'Filter' plugin category.
    - [ ] Define the `FilterPlugin` base class.
- [ ] Task: Create Basic Metadata Filtering Plugins.
    - [ ] Implement File Type filter.
    - [ ] Implement File Size filter.
    - [ ] Implement Date Range filter.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Filtering & Metadata Implementation' (Protocol in workflow.md)

## Phase 5: Final Integration & Cleanup
- [ ] Task: Remove obsolete UI injection code from the Main Window and old plugin headers.
- [ ] Task: Perform comprehensive integration testing across all sorting, grouping, and filtering combinations.
- [ ] Task: Verify performance and responsiveness under large image sets.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Integration & Cleanup' (Protocol in workflow.md)
