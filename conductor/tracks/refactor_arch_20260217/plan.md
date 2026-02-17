# Implementation Plan: Architecture Refactoring

This plan outlines the steps for refactoring the plugin system and separating the application logic from the UI logic.

## Phase 1: Preparation and Baseline [checkpoint: 9eb0a01]
- [x] Task: Conduct a thorough audit of `src/ui/main_window/logic.py` to identify all business logic, state management, and core service calls.
- [x] Task: Identify and document all current dependencies of the `PluginManager` and `PluginBase`.
- [x] Task: Create a baseline of existing unit tests and ensure they pass before refactoring begins.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation and Baseline' (Protocol in workflow.md)

## Phase 2: Refactor Plugin System (`src/plugin/`) [checkpoint: 571e00d]
- [x] Task: Create the `src/plugin/` directory structure if it doesn't exist.
- [x] Task: Move `PluginBase` and `PluginManager` from their current locations to `src/plugin/`.
- [x] Task: Update all internal imports within the plugin system to reflect the new structure.
- [x] Task: Refactor the plugin discovery mechanism to separate "Statistical Rules" plugins from core management logic.
- [x] Task: Write/Update unit tests for `PluginManager` in its new location.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Refactor Plugin System' (Protocol in workflow.md)

## Phase 3: Establish Core Application Layer (`src/app/`)
- [x] Task: Create the `src/app/` directory.
- [x] Task: Implement/Move Global State Management to `src/app/state.py` (or similar).
- [x] Task: Implement/Move Database Operations to `src/app/database.py`.
- [x] Task: Implement/Move File Operations (Safe move logic) to `src/app/file_ops.py`.
- [x] Task: Implement/Move Centralized Logging to `src/app/logger.py`.
- [x] Task: Implement the new application entry point in `src/app/main.py` and migrate initialization logic.
- [~] Task: Write unit tests for new components in `src/app/` (State, DB, File Ops, Logger).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Establish Core Application Layer' (Protocol in workflow.md)

## Phase 4: Decouple MainWindow Logic (`src/ui/`)
- [ ] Task: Refactor `src/ui/main_window/logic.py` to delegate business logic calls to the `src/app/` services.
- [ ] Task: Migrate application state from `MainWindow` to `src/app/state.py`.
- [ ] Task: Update `MainWindow` to use the new registration hooks for plugins via the `src/app/` layer.
- [ ] Task: Ensure `MainWindow` only manages UI-specific states (signals, layouts, active tabs).
- [ ] Task: Verify that all UI events correctly trigger the corresponding application logic in `src/app/`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Decouple MainWindow Logic' (Protocol in workflow.md)

## Phase 5: Final Integration and Verification
- [ ] Task: Run the full test suite (automated and manual) to ensure no regressions in file operations, analysis, or preview features.
- [ ] Task: Verify that all statistical plugins load and function correctly.
- [ ] Task: Perform a final code review to ensure adherence to architectural goals (separation of concerns).
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Final Integration and Verification' (Protocol in workflow.md)
