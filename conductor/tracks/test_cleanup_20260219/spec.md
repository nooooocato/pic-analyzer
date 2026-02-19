# Specification: Test Suite Reorganization and Decentralization

## Overview
This track focuses on cleaning up and reorganizing the test suite of Pic-Analyzer. The goal is to move plugin-specific tests directly into their respective plugin packages in the `./plugins/` directory, and to categorize core tests in the `./tests/` directory to match the structure of the `./src/` code.

## Functional Requirements

### 1. Plugin Test Decentralization
- Move tests related to individual plugins from `tests/` to their respective plugin directories.
- Tests will be placed directly in the plugin package directory (no `tests/` subfolder).
- Specific moves:
    - **`plugins/sort/ascending/test_algo.py`**: Extracted from `tests/test_basic_sort_plugins.py`.
    - **`plugins/sort/descending/test_algo.py`**: Extracted from `tests/test_basic_sort_plugins.py`.
    - **`plugins/sort/normal_dist/test_algo.py`**: Moved from `tests/test_normal_dist_plugin.py`.
    - **`plugins/group/date_grouping/test_plugin.py`**: Moved from `tests/test_plugin_date_grouping.py`.

### 2. Core Test Categorization
- Reorganize the `tests/` directory into subfolders that mirror the `src/` directory structure.
- **`tests/app/`**:
    - `test_app_state.py`
    - `test_communicator.py`
    - `test_file_ops.py`
    - `test_file_scanner.py`
    - `test_scaffolding.py`
    - `test_sys_path.py`
- **`tests/db/`**:
    - `test_peewee_db.py`
- **`tests/plugin/`**:
    - `test_plugin_discovery.py`
    - `test_plugin_framework.py`
    - `test_plugin_structure.py`
    - `test_malformed_plugins.py`
    - `test_plugin_conflicts.py`
    - `test_plugin_integration.py`
    - `test_base_plugin_update.py`
- **`tests/ui/`**:
    - `test_thumbnail_gen.py`
    - `test_toast_decoupled.py`
    - `test_data_inspector.py`
    - `test_main_window_hooks.py`
    - `test_main_window_plugin_init.py`
    - **`ui_basic/`**: Renamed from `tests/ui_refactor/` and moved into `tests/ui/`.

### 3. Test Configuration and Discovery
- Ensure `pytest` can still discover and run all tests in both the `tests/` and `plugins/` directories.
- Clean up any redundant tests or obsolete temporary files (`__pycache__`, `.pytest_cache`) during the process.

## Acceptance Criteria
- All tests pass when running `pytest` from the project root.
- The `./tests/` directory contains no files at the root level (except maybe `conftest.py` if needed).
- Each plugin directory contains its own functional tests.
- Core tests are logically grouped by their corresponding `src/` module.
- The `tests/ui/ui_basic/` folder exists and contains the previous `ui_refactor` tests.

## Out of Scope
- Adding new feature tests (this is strictly a refactor/chore).
- Modifying the actual implementation logic in `src/` or `plugins/`.
