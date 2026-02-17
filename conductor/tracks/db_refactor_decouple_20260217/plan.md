# Implementation Plan: Database Refactor and Component Decoupling

## Phase 1: Database Layer - Peewee ORM Implementation
Establish the new ORM-based database infrastructure in `/src/db` and define models.

- [x] Task: Create Peewee Models and Initial Setup (84b2f4e)
    - [x] Create `/src/db/models.py` with `Workspace`, `Image`, and `AnalysisResult` models.
    - [x] Create `/src/db/manager.py` for database initialization and connection handling.
- [x] Task: Implement Standardized CRUD Methods (ef6660a)
    - [x] Write tests for `upsert_image` and implement.
    - [x] Write tests for `manage_workspace` and implement.
    - [x] Write tests for `query_images` (returning `Select` objects) and implement.
    - [x] Write tests for `update_metrics` and implement.
- [x] Task: Integrate with Existing App Layer (9f8d38d)
    - [x] Update `src/app/state.py` to use the new Peewee manager.
    - [x] Migrate `src/app/file_scanner.py` to use Peewee models.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Database Layer' (Protocol in workflow.md)

## Phase 2: Component Decoupling - Event Bus and Toast
Decouple the notification system from the Main Window using a signal-based event bus.

- [ ] Task: Implement Global Communicator
    - [ ] Create `src/app/communicator.py` with singleton `Communicator` class and PySide6 signals.
- [ ] Task: Refactor Toast Component
    - [ ] Modify `src/ui/common/toast` to subscribe to `Communicator` signals.
    - [ ] Remove Toast management logic from `src/ui/main_window/logic.py`.
    - [ ] Update all callers (e.g., file_ops, plugins) to use `Communicator.notify`.
- [ ] Task: Verify Toast Functionality
    - [ ] Write integration tests for decoupled Toast notifications.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Event Bus and Toast' (Protocol in workflow.md)

## Phase 3: Component Decoupling - Data Inspector
Refactor the Data Inspector into a standalone, reactive widget.

- [ ] Task: Standalone Data Inspector Widget
    - [ ] Refactor `src/ui/main_window` related logic to move Data Inspector to a dedicated component (e.g., `src/ui/overlays/data_inspector`).
- [ ] Task: Implement Data-Binding
    - [ ] Update Data Inspector to listen for gallery selection signals from the `Communicator`.
    - [ ] Implement reactive view updates in Data Inspector based on Peewee model instances.
- [ ] Task: Cleanup MainWindow
    - [ ] Remove direct Data Inspector references and management code from `MainWindow`.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Data Inspector' (Protocol in workflow.md)

## Phase 4: Final Migration and Cleanup
Deprecated old database logic and ensure full system integration.

- [ ] Task: Deprecate `src/app/database.py`
    - [ ] Remove old SQL-string based database logic.
    - [ ] Ensure all tests originally using `database.py` now pass with the new Peewee implementation.
- [ ] Task: Final Integration Test Pass
    - [ ] Run full test suite and verify >80% coverage.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Migration' (Protocol in workflow.md)
