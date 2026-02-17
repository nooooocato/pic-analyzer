# Specification: Database Refactor and Component Decoupling

## Overview
This track focuses on modernizing the data persistence layer using Peewee ORM and improving the UI architecture by decoupling the `Toast` and `Data Inspector` components from the `MainWindow`. These changes aim to enhance maintainability, type safety, and component reusability.

## Functional Requirements

### 1. Database Layer (Peewee ORM)
- **New Location:** All database-related logic will reside in `/src/db`.
- **ORM Implementation:** Use Peewee to define models for `Workspace`, `Image`, and `AnalysisResult`.
- **Standardized CRUD:** Provide a clean API for upper layers:
    - `upsert_image(metadata, analysis_data)`
    - `manage_workspace(action, data)` (Create, Delete, Load)
    - `query_images(filters, group_by)` (Batch queries)
    - `update_metrics(image_id, metrics)` (Specific metric updates)
- **Plugin Integration:** The DB layer will return Peewee `Select` objects to allow plugins (sorting/grouping) to append filters and ordering before execution.
- **Migration:** Systematically replace existing calls to `src/app/database.py` with the new ORM-based methods.

### 2. Component Decoupling
- **Signal/Slot Architecture:** Implement a centralized `Communicator` (or similar event bus) to handle cross-component communication.
- **Toast Component:**
    - Decouple from `MainWindow` logic.
    - Trigger notifications via global signals (e.g., `communicator.notify.emit("Message", level)`).
- **Data Inspector Component:**
    - Refactor into a standalone, reusable widget (Sidebar/Overlay).
    - Implement automatic data-binding: it should listen for selection change signals and update its display automatically based on the currently selected image(s).

## Non-Functional Requirements
- **Maintainability:** Clear separation between data access patterns and business logic.
- **Testability:** Ensure all new DB methods and decoupled components have >80% unit test coverage.
- **Performance:** ORM queries must be optimized; Peewee's `Select` objects should be used efficiently to avoid N+1 query problems.

## Acceptance Criteria
- [ ] Peewee models fully defined in `/src/db`.
- [ ] `src/app/database.py` is successfully replaced/deprecated.
- [ ] `Toast` notifications work without direct references from `MainWindow`.
- [ ] `Data Inspector` updates its view correctly when the gallery selection changes, without being managed by `MainWindow`.
- [ ] All existing and new tests pass.

## Out of Scope
- Migrating existing user data (since this is an MVP/internal tool, a database reset is acceptable if needed).
- Adding new statistical plugins during this refactor.
