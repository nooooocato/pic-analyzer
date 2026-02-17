# Implementation Plan: Externalized Plugin System with Dynamic UI Injection

## Phase 1: Infrastructure & Discovery Refactor [checkpoint: c7fc649]
This phase focuses on setting up the new directory structure and implementing the robust discovery mechanism.

- [x] Task: Create new root-level `./plugins` directory and subdirectories (`sort`, `group`, etc.) [8461cd8]
- [x] Task: Implement new `PluginManager` logic to scan the root `./plugins` directory instead of `src/plugins` [1d8a543]
- [x] Task: Implement conflict detection (name/ID) in the `PluginManager` with error logging [3c9ac5c]
- [x] Task: Update `run_app.py` or initialization logic to ensure `./plugins` is in the Python path [2e68e10]
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Infrastructure' (Protocol in workflow.md)

## Phase 2: Dynamic UI Injection Framework [checkpoint: 8efdecd]
This phase introduces the mechanism for plugins to interact with and inject components into the main UI.

- [x] Task: Define the `BasePlugin` interface update to include an `initialize_ui(self, main_window)` method [f3294b6]
- [x] Task: Modify `MainWindow` or UI controllers to call `initialize_ui` for all loaded plugins during startup [9439754]
- [x] Task: Implement a registration/hooks system in `MainWindow` to allow safe access to UI containers (e.g., toolbar, status bar) [bd4c545]
- [ ] Task: Conductor - User Manual Verification 'Phase 2: UI Framework' (Protocol in workflow.md)

## Phase 3: Migration of Existing Plugins [checkpoint: be60464]
This phase involves moving the built-in plugins to the new system and adapting them to the new UI injection model.

- [ ] Task: Migrate `src/plugins/sort` logic to `./plugins/sort/` (e.g., `ascending`, `descending`, `normal_dist`)
- [ ] Task: Implement `ui.py` for each migrated sorting plugin to handle its own UI placement (e.g., adding to the Sort menu)
- [ ] Task: Remove old `src/plugins` directory and cleanup any stale imports in the codebase
- [ ] Task: Update existing unit tests in `tests/` to target the new plugin locations
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Migration' (Protocol in workflow.md)

## Phase 4: Verification & Hardening [checkpoint: f7f8fed]
Final testing and error handling improvements.

- [x] Task: Write integration tests for the new plugin loading and UI injection lifecycle [be60464]
- [~] Task: Verify that a malformed plugin does not crash the entire application
- [ ] Task: Verify that plugin conflicts are correctly logged and handled
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Verification' (Protocol in workflow.md)

## Phase: Review Fixes
- [x] Task: Apply review suggestions (fix brittle imports, add docstrings, refactor run_app.py) [edd9611]
