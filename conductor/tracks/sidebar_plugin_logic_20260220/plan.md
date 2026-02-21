# Implementation Plan: Sidebar & Plugin Logic Upgrade

#### Phase 1: Sidebar Layout & Splitter [checkpoint: b6c11b8]
Refactor the sidebar container to support dynamic grouping and resizable expanded sections.
- [x] Task: [RED] Write tests for Sidebar dynamic reordering and splitter initialization c435435
- [x] Task: [GREEN] Implement sidebar grouping logic (Expanded top, Collapsed bottom) 5bc1f55
- [x] Task: [GREEN] Integrate `QSplitter` for expanded sections to allow manual resizing 5bc1f55
- [x] Task: [REFACTOR] Clean up sidebar layout management and handle expansion events 5bc1f55
- [x] Task: Conductor - User Manual Verification 'Phase 1: Sidebar Layout' (Protocol in workflow.md) b346064

#### Phase 2: Multi-Item UI Framework
Create the base UI components for managing multiple instances of filter/sort plugins.
- [x] Task: [RED] Write tests for `PluginItemWrapper` (Close button, Toggle state, Drag handle) 1ac4757
- [x] Task: [GREEN] Implement `PluginItemWrapper` to provide common controls for plugin widgets 1ac4757
- [x] Task: [GREEN] Implement the "+" button and dynamic widget generation in the Sidebar 1ac4757
- [x] Task: [GREEN] Implement the AND/OR logical operator UI for filter items 1ac4757
- [x] Task: Conductor - User Manual Verification 'Phase 2: Multi-Item UI' (Protocol in workflow.md) db8ed75

#### Phase 3: Compound Filter Logic
Update the core application logic to evaluate multiple filters with logical connectors.
- [ ] Task: [RED] Write unit tests for the compound filter evaluation engine (AND/OR chains)
- [ ] Task: [GREEN] Refactor `FilterPluginManager` to support sequential filter evaluation
- [ ] Task: [GREEN] Implement the boolean logic processor for `((F1 Op F2) Op F3)` chains
- [ ] Task: [REFACTOR] Optimize filter application to minimize redundant database queries
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Filter Logic' (Protocol in workflow.md)

#### Phase 4: Sequential Sorting Logic
Implement sequential "Then" sorting with drag-and-drop reordering support.
- [ ] Task: [RED] Write unit tests for stable sequential sorting (Primary > Secondary > Tertiary)
- [ ] Task: [GREEN] Refactor `SortPluginManager` to perform stable, multi-stage sorting
- [ ] Task: [GREEN] Implement drag-and-drop reordering logic within the Sort UI section
- [ ] Task: [REFACTOR] Ensure UI order and sorting logic order remain synchronized
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Sequential Sorting' (Protocol in workflow.md)

#### Phase 5: Workspace State Persistence
Integrate state saving and restoration into the workspace database.
- [ ] Task: [RED] Write tests for sidebar state serialization and DB persistence
- [ ] Task: [GREEN] Update Peewee models to include tables for persistent sidebar configurations
- [ ] Task: [GREEN] Implement auto-save logic triggered by sidebar UI changes
- [ ] Task: [GREEN] Implement state restoration logic on workspace load
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Persistence' (Protocol in workflow.md)
