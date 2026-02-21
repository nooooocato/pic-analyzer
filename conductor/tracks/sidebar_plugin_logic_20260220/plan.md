# Implementation Plan: Sidebar & Plugin Logic Upgrade

#### Phase 1: Sidebar Layout & Splitter [checkpoint: b6c11b8]
Refactor the sidebar container to support dynamic grouping and resizable expanded sections.
- [x] Task: [RED] Write tests for Sidebar dynamic reordering and splitter initialization c435435
- [x] Task: [GREEN] Implement sidebar grouping logic (Expanded top, Collapsed bottom) 5bc1f55
- [x] Task: [GREEN] Integrate `QSplitter` for expanded sections to allow manual resizing 5bc1f55
- [x] Task: [REFACTOR] Clean up sidebar layout management and handle expansion events 5bc1f55
- [x] Task: Conductor - User Manual Verification 'Phase 1: Sidebar Layout' (Protocol in workflow.md) b346064

#### Phase 2: Multi-Item UI Framework [checkpoint: 554c6ad]
Create the base UI components for managing multiple instances of filter/sort plugins.
- [x] Task: [RED] Write tests for `PluginItemWrapper` (Close button, Toggle state, Drag handle) 1ac4757
- [x] Task: [GREEN] Implement `PluginItemWrapper` to provide common controls for plugin widgets 1ac4757
- [x] Task: [GREEN] Implement the "+" button and dynamic widget generation in the Sidebar 1ac4757
- [x] Task: [GREEN] Implement the AND/OR logical operator UI for filter items 1ac4757
- [x] Task: Conductor - User Manual Verification 'Phase 2: Multi-Item UI' (Protocol in workflow.md) db8ed75

#### Phase 3: Compound Filter Logic [checkpoint: 4254141]
Update the core application logic to evaluate multiple filters with logical connectors.
- [x] Task: [RED] Write unit tests for the compound filter evaluation engine (AND/OR chains) db8ed75
- [x] Task: [x] Refactor `FilterPluginManager` to support sequential filter evaluation (Delegated to FilterEngine) db8ed75
- [x] Task: [x] Implement the boolean logic processor for `((F1 Op F2) Op F3)` chains db8ed75
- [x] Task: [REFACTOR] Optimize filter application to minimize redundant database queries db8ed75
- [x] Task: Conductor - User Manual Verification 'Phase 3: Filter Logic' (Protocol in workflow.md) 4254141

#### Phase 4: Sequential Sorting Logic [checkpoint: 5d5260e]
Implement sequential "Then" sorting with drag-and-drop reordering support.
- [x] Task: [RED] Write unit tests for stable sequential sorting (Primary > Secondary > Tertiary) 4254141
- [x] Task: [x] Refactor `SortPluginManager` to perform stable, multi-stage sorting (Delegated to Gallery) 4254141
- [x] Task: [x] Implement drag-and-drop reordering logic within the Sort UI section 4254141
- [x] Task: [REFACTOR] Ensure UI order and sorting logic order remain synchronized 4254141
- [x] Task: Conductor - User Manual Verification 'Phase 4: Sequential Sorting' (Protocol in workflow.md) 56a26d0

#### Phase 5: Workspace State Persistence [checkpoint: 554c6ad]
Integrate state saving and restoration into the workspace database.
- [x] Task: [RED] Write tests for sidebar state serialization and DB persistence 56a26d0
- [x] Task: [GREEN] Update Peewee models to include tables for persistent sidebar configurations 56a26d0
- [x] Task: [GREEN] Implement auto-save logic triggered by sidebar UI changes 56a26d0
- [x] Task: [GREEN] Implement state restoration logic on workspace load 56a26d0
- [x] Task: Conductor - User Manual Verification 'Phase 5: Persistence' (Protocol in workflow.md) a2cfa04

#### Track Summary & Refinements
- **Robust Drag-and-Drop:** Refactored `PluginItemWrapper` and `SidebarContainer` to ensure items never disappear when dropped outside and correctly return to their positions.
- **Gallery Header Logic:** Implemented specific anchoring for "Filtered Images" at the top when any filter is active, preventing header scaling issues.
- **Global Font Fix:** Set application-wide font in `main.py` to eliminate `QFont::setPointSize` warnings.
- **Crash Prevention:** Strengthened rule collection and widget deletion logic to handle rapid sidebar modifications without state corruption.
