# Implementation Plan - MVP Gallery

## Phase 1: Project Scaffolding & Database Setup [checkpoint: ef97933]
- [x] Task: Initialize Python project with PySide6 and standard directory structure (src, plugins, assets). c1ba088
    - [ ] Set up `requirements.txt`.
    - [ ] Create basic package structure.
- [x] Task: Design and implement the SQLite database schema for image metadata and analysis results. 392376b
    - [ ] Define tables for images, analysis_results, and plugin_metadata.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Project Scaffolding & Database Setup' (Protocol in workflow.md)

## Phase 2: Core UI Components [checkpoint: a06e7c8]
- [x] Task: Implement the Main Window with Fluent Design styling. 553e642
    - [ ] Create Top Toolbar placeholder.
    - [ ] Create Sidebar with a `QTreeView` for the Data Inspector.
- [x] Task: Implement the Tiled Gallery View. 9245a05
    - [ ] Use `QListView` or `QScrollArea` with a flow layout for responsive tiling.
    - [ ] Implement lazy loading for thumbnails.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Core UI Components' (Protocol in workflow.md)

## Phase 3: Plugin Framework & File Operations
- [x] Task: Design the Analysis Plugin interface and Factory pattern. f3619d6
    - [ ] Create a base class for plugins.
    - [ ] Implement dynamic loading from the `plugins/` directory.
- [x] Task: Implement "Safe Move" file operations with conflict resolution dialog. aae14dc
    - [ ] Use `shutil.move` for atomic operations.
    - [ ] Create interactive prompt for Rename/Skip/Overwrite.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Plugin Framework & File Operations' (Protocol in workflow.md)

## Phase 4: Integration & Initial Plugins
- [ ] Task: Implement the "Date Grouping" logic as a built-in feature/plugin.
- [ ] Task: Connect the Data Inspector to display real-time metadata from selected images.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Integration & Initial Plugins' (Protocol in workflow.md)
