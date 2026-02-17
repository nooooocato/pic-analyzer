# Implementation Plan - Merge Dev to Main and Cleanup

Integrating development progress into `main`, cleaning up legacy artifacts, and ensuring project consistency.

## Phase 1: Preparation and Merge
Integration of `dev` into `main` and initial environment synchronization.

- [ ] Task: Switch to `main` branch and ensure it is up to date with remote
- [ ] Task: Merge `dev` into `main` using standard merge
- [ ] Task: Resolve any merge conflicts (if any) and verify basic app startup
- [ ] Task: Update `requirements.txt` to match `dev` environment
- [ ] Task: Run current test suite to establish a baseline on `main`
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Preparation and Merge' (Protocol in workflow.md)

## Phase 2: Dependency Analysis and Candidate Identification
Identifying files that are no longer needed after the UI refactor and architectural changes.

- [ ] Task: Script/Automated check for unused imports across the codebase
- [ ] Task: Manually identify legacy UI files in `src/ui/` (e.g., `gallery_view_new.py` if replaced)
- [ ] Task: Identify orphaned test files in `tests/` and legacy root scripts (e.g., `test_sf_move.py`)
- [ ] Task: Present list of cleanup candidates to user for confirmation
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Dependency Analysis and Candidate Identification' (Protocol in workflow.md)

## Phase 3: Safe Cleanup (Soft Delete)
Removing confirmed files using a "soft delete" safety net.

- [ ] Task: Create temporary backup directory `.cleanup_backup/` (ignored by git)
- [ ] Task: Move confirmed redundant files to `.cleanup_backup/`
- [ ] Task: Perform full regression test suite to ensure no breakage from removal
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Safe Cleanup (Soft Delete)' (Protocol in workflow.md)

## Phase 4: Finalization and Documentation
Final cleanup, documentation updates, and project synchronization.

- [ ] Task: Permanently delete files in `.cleanup_backup/`
- [ ] Task: Update `README.md` with any new setup or architectural details
- [ ] Task: Synchronize Conductor registry and archive completed tracks if necessary
- [ ] Task: Final full test suite and linting check
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Finalization and Documentation' (Protocol in workflow.md)
