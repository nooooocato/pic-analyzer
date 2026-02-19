# Implementation Plan: Test Suite Reorganization and Decentralization

## Phase 1: Preparation and Environment Check [checkpoint: 570ef1e]
- [x] Task: Verify current test state by running all tests.
    - [x] Run `pytest` and ensure 100% pass rate before starting.
- [x] Task: Create new directory structure in `tests/`. (8d252ac)
    - [x] Create `tests/app/`
    - [x] Create `tests/db/`
    - [x] Create `tests/plugin/`
    - [x] Create `tests/ui/`

## Phase 2: Core Test Categorization [checkpoint: dc15c75]
- [x] Task: Move App-related tests to `tests/app/`. (cb30396)
    - [x] Move `tests/test_app_state.py`, `tests/test_communicator.py`, `tests/test_file_ops.py`, `tests/test_file_scanner.py`, `tests/test_scaffolding.py`, `tests/test_sys_path.py` to `tests/app/`.
- [x] Task: Move DB-related tests to `tests/db/`. (119ccb2)
    - [x] Move `tests/test_peewee_db.py` to `tests/db/`.
- [x] Task: Move Plugin-framework-related tests to `tests/plugin/`. (cdc8373)
    - [x] Move `tests/test_plugin_discovery.py`, `tests/test_plugin_framework.py`, `tests/test_plugin_structure.py`, `tests/test_malformed_plugins.py`, `tests/test_plugin_conflicts.py`, `tests/test_plugin_integration.py`, `tests/test_base_plugin_update.py` to `tests/plugin/`.
- [x] Task: Reorganize and rename UI tests. (3af0eeb)
    - [x] Move `tests/test_thumbnail_gen.py`, `tests/test_toast_decoupled.py`, `tests/test_data_inspector.py`, `tests/test_main_window_hooks.py`, `tests/test_main_window_plugin_init.py` to `tests/ui/`.
    - [x] Move and rename `tests/ui_refactor/` to `tests/ui/ui_basic/`.
- [x] Task: Conductor - User Manual Verification 'Core Categorization' (Protocol in workflow.md)

## Phase 3: Plugin Test Decentralization
- [ ] Task: Extract and move Sort plugin tests.
    - [ ] Split `tests/test_basic_sort_plugins.py` into `plugins/sort/ascending/test_algo.py` and `plugins/sort/descending/test_algo.py`.
    - [ ] Move `tests/test_normal_dist_plugin.py` to `plugins/sort/normal_dist/test_algo.py`.
- [ ] Task: Move Group plugin tests.
    - [ ] Move `tests/test_plugin_date_grouping.py` to `plugins/group/date_grouping/test_plugin.py`.
- [ ] Task: Conductor - User Manual Verification 'Plugin Decentralization' (Protocol in workflow.md)

## Phase 4: Verification and Cleanup
- [ ] Task: Update test discovery (if necessary).
    - [ ] Check if `pytest` discovers tests in `plugins/` automatically; if not, add configuration.
- [ ] Task: Run all tests to ensure no regressions.
    - [ ] Run `pytest` from the root and verify all tests pass.
- [ ] Task: Final Cleanup.
    - [ ] Remove empty directories and delete `tests/test_basic_sort_plugins.py`.
    - [ ] Clean up `__pycache__` and `.pytest_cache`.
- [ ] Task: Conductor - User Manual Verification 'Final Verification' (Protocol in workflow.md)
