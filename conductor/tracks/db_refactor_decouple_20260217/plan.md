# Implementation Plan: Database Refactor and Component Decoupling

## Phase 1: Database Layer - Peewee ORM Implementation [checkpoint: f108ebd]
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
- [x] Task: Conductor - User Manual Verification 'Phase 1: Database Layer' (f108ebd)

## Phase 2: Component Decoupling - Event Bus and Toast [checkpoint: 49176fc]
Decouple the notification system from the Main Window using a signal-based event bus.

- [x] Task: Implement Global Communicator (253f2ad)
    - [x] Create `src/app/communicator.py` with singleton `Communicator` class and PySide6 signals.
- [x] Task: Refactor Toast Component (063c9d2)
    - [x] Modify `src/ui/common/toast` to subscribe to `Communicator` signals.
    - [x] Remove Toast management logic from `src/ui/main_window/logic.py`.
    - [x] Update all callers (e.g., file_ops, plugins) to use `Communicator.notify`.
- [x] Task: Verify Toast Functionality (063c9d2)
    - [x] Write integration tests for decoupled Toast notifications.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Event Bus and Toast' (49176fc)

## Phase 3: Component Decoupling - Data Inspector [checkpoint: 1cf7782]
Refactor the Data Inspector into a standalone, reactive widget.

- [x] Task: Standalone Data Inspector Widget (eb448df)
    - [x] Refactor `src/ui/main_window` related logic to move Data Inspector to a dedicated component (e.g., `src/ui/overlays/data_inspector`).
- [x] Task: Implement Data-Binding (eb448df)
    - [x] Update Data Inspector to listen for gallery selection signals from the `Communicator`.
    - [x] Implement reactive view updates in Data Inspector based on Peewee model instances.
- [x] Task: Cleanup MainWindow (eb448df)
    - [x] Remove direct Data Inspector references and management code from `MainWindow`.
- [x] Task: Conductor - User Manual Verification 'Phase 3: Data Inspector' (1cf7782)

## Phase 4: Final Migration and Cleanup (fff46c0)
Deprecated old database logic and ensure full system integration.

- [x] Task: Deprecate `src/app/database.py` (fff46c0)
    - [x] Remove old SQL-string based database logic.
    - [x] Ensure all tests originally using `database.py` now pass with the new Peewee implementation.
- [x] Task: Final Integration Test Pass (fff46c0)
    - [x] Run full test suite and verify >80% coverage.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Migration' (Protocol in workflow.md)
