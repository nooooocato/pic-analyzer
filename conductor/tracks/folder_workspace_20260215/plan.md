# Implementation Plan: Folder Selection & Workspace Management

## Phase 1: UI Foundations & Menu Bar [checkpoint: 81d866c]
- [x] Task: Add `QMenuBar` to `MainWindow` with `File > Open Folder` action. (81c1f55)
    - [ ] Write Tests: Verify `MainWindow` has a menu bar and the "Open Folder" action is present and connected.
    - [ ] Implement: Update `src/ui/main_window.py` to include a menu bar and trigger a folder selection dialog.
- [x] Task: Implement basic folder selection logic in `MainWindow`. (ed4a4f4)
    - [ ] Write Tests: Mock `QFileDialog` to ensure the selected path is correctly captured.
    - [ ] Implement: Add `_on_open_folder` method to `MainWindow` to handle the selection.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: UI Foundations & Menu Bar' (Protocol in workflow.md)

## Phase 2: Threaded Recursive Scanner
- [x] Task: Create `FolderScanner` worker for background file discovery. (56e75b1)
    - [ ] Write Tests: Verify `FolderScanner` correctly identifies image files recursively in a test directory.
    - [ ] Implement: Create `src/file_scanner.py` with a `QRunnable` that emits signals as it finds files.
- [ ] Task: Integrate `FolderScanner` with `MainWindow` for real-time updates.
    - [ ] Write Tests: Verify `MainWindow` receives file signals and updates the gallery.
    - [ ] Implement: Connect `FolderScanner` signals to `GalleryView` to add images dynamically.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Threaded Recursive Scanner' (Protocol in workflow.md)

## Phase 3: Workspace & Database Management
- [ ] Task: Enhance `DatabaseManager` to support dynamic database switching.
    - [ ] Write Tests: Verify `DatabaseManager` can close one DB and open another correctly.
    - [ ] Implement: Update `src/database.py` to handle dynamic paths and session management.
- [ ] Task: Implement Workspace Prompt and Management logic.
    - [ ] Write Tests: Verify the application prompts the user when switching folders if a workspace is active.
    - [ ] Implement: Add a `WorkspaceManager` or update `MainWindow` to handle the "Save/Clear" prompt and manage the hybrid storage logic (centralized vs `.pa` file).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Workspace & Database Management' (Protocol in workflow.md)

## Phase 4: Final Integration & Refinement
- [ ] Task: Ensure clean state transitions.
    - [ ] Write Tests: Verify gallery and database are cleared/reset when a new folder is opened.
    - [ ] Implement: Final wiring in `MainWindow` to ensure all components reset correctly during workspace changes.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Integration & Refinement' (Protocol in workflow.md)
