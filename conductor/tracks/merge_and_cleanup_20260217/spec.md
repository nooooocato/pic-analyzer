# Track Specification: Merge Dev to Main and Cleanup

## Overview
This track focuses on integrating the significant development changes (including the UI refactor and plugin system) from the `dev` branch into the `main` branch. A secondary but critical goal is to identify and remove legacy source files that are no longer referenced or required after the refactor, ensuring a clean and maintainable codebase.

## Functional Requirements
- **Branch Integration**: Merge the `dev` branch into `main` using a standard merge strategy.
- **Dependency Analysis**: Identify redundant files in `src/`, root directory, and `tests/` that are no longer imported or used.
- **Safe Cleanup**:
    - Perform an automated import/dependency check to flag potential candidates for removal.
    - Provide a list of candidates for manual user confirmation.
    - Implement a "soft delete" by moving confirmed files to a temporary backup directory (`.cleanup_backup/`) before final deletion.
- **Environment Update**: Ensure `requirements.txt` is synchronized with the latest development dependencies.
- **Documentation Sync**: Update `README.md` and Conductor registry/docs to reflect the post-merge project state.

## Non-Functional Requirements
- **Stability**: The application must remain fully functional after the cleanup.
- **Auditability**: Track the removal of files through the plan and git history.

## Acceptance Criteria
- `main` branch is successfully merged with `dev`.
- Identified redundant files (Old UI, legacy tests, root temp files) are removed.
- Full test suite passes on the `main` branch post-cleanup.
- `requirements.txt` and documentation are up to date.

## Out of Scope
- Implementing new features during this integration track.
- Major refactoring of existing logic (only removal of unused code).
