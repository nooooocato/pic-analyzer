# Implementation Plan - Merge Dev to Main and Cleanup

Integrating development progress into `main`, cleaning up legacy artifacts, and ensuring project consistency.

## Phase 1: Preparation and Merge [checkpoint: e8d693d]
Integration of `dev` into `main` and initial environment synchronization.

- [x] Task: Switch to `main` branch and ensure it is up to date with remote fdaf106
- [x] Task: Merge `dev` into `main` using standard merge fdaf106
- [x] Task: Resolve any merge conflicts (if any) and verify basic app startup fdaf106
- [x] Task: Update `requirements.txt` to match `dev` environment fdaf106
- [x] Task: Run current test suite to establish a baseline on `main` fdaf106
- [x] Task: Conductor - User Manual Verification 'Phase 1: Preparation and Merge' (Protocol in workflow.md) e8d693d

## Phase 2: Dependency Analysis and Candidate Identification
Identifying files that are no longer needed after the UI refactor and architectural changes.

- [x] Task: Script/Automated check for unused imports across the codebase 3a079d4
- [x] Task: Manually identify legacy UI files in `src/ui/` (e.g., `gallery_view_new.py` if replaced) 3a079d4
- [x] Task: Identify orphaned test files in `tests/` and legacy root scripts (e.g., `test_sf_move.py`) 3a079d4
- [~] Task: Present list of cleanup candidates to user for confirmation
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Dependency Analysis and Candidate Identification' (Protocol in workflow.md)

## Phase 3: Safe Cleanup (Soft Delete) [checkpoint: 39566a3]
Removing confirmed files using a "soft delete" safety net.

- [x] Task: Create temporary backup directory `.cleanup_backup/` (ignored by git) 39566a3
- [x] Task: Move confirmed redundant files to `.cleanup_backup/` 39566a3
- [x] Task: Perform full regression test suite to ensure no breakage from removal 39566a3
- [x] Task: Conductor - User Manual Verification 'Phase 3: Safe Cleanup (Soft Delete)' (Protocol in workflow.md) 39566a3

## Phase 4: Finalization and Documentation
Final cleanup, documentation updates, and project synchronization.

- [x] Task: Permanently delete files in `.cleanup_backup/` 39566a3
- [x] Task: Update `README.md` with any new setup or architectural details 39566a3
- [x] Task: Synchronize Conductor registry and archive completed tracks if necessary 39566a3
- [x] Task: Final full test suite and linting check 39566a3
- [x] Task: Conductor - User Manual Verification 'Phase 4: Finalization and Documentation' (Protocol in workflow.md) 39566a3
