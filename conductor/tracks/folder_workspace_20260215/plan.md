# Implementation Plan: Folder Selection & Workspace Management

## Phase 1: UI Foundations & Menu Bar [checkpoint: 81d866c]
- [x] Task: Add `QMenuBar` to `MainWindow` with `File > Open Folder` action. (81c1f55)
    - [ ] Write Tests: Verify `MainWindow` has a menu bar and the "Open Folder" action is present and connected.
    - [ ] Implement: Update `src/ui/main_window.py` to include a menu bar and trigger a folder selection dialog.
- [x] Task: Implement basic folder selection logic in `MainWindow`. (ed4a4f4)
    - [ ] Write Tests: Mock `QFileDialog` to ensure the selected path is correctly captured.
    - [ ] Implement: Add `_on_open_folder` method to `MainWindow` to handle the selection.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: UI Foundations & Menu Bar' (Protocol in workflow.md)

## Phase 2: Threaded Recursive Scanner [checkpoint: 69cea1c]
- [x] Task: Create `FolderScanner` worker for background file discovery. (56e75b1)
    - [ ] Write Tests: Verify `FolderScanner` correctly identifies image files recursively in a test directory.
    - [ ] Implement: Create `src/file_scanner.py` with a `QRunnable` that emits signals as it finds files.
- [x] Task: Integrate `FolderScanner` with `MainWindow` for real-time updates. (2ac9d33)
    - [ ] Write Tests: Verify `MainWindow` receives file signals and updates the gallery.
    - [ ] Implement: Connect `FolderScanner` signals to `GalleryView` to add images dynamically.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Threaded Recursive Scanner' (Protocol in workflow.md)

## Phase 3: Workspace & Database Management [checkpoint: f769477]
- [x] Task: Enhance `DatabaseManager` to support dynamic database switching. (193610e)
    - [ ] Write Tests: Verify `DatabaseManager` can close one DB and open another correctly.
    - [ ] Implement: Update `src/database.py` to handle dynamic paths and session management.
- [x] Task: Implement Workspace Prompt and Management logic. (4c81c3a)
    - [ ] Write Tests: Verify the application prompts the user when switching folders if a workspace is active.
    - [ ] Implement: Add a `WorkspaceManager` or update `MainWindow` to handle the "Save/Clear" prompt and manage the hybrid storage logic (centralized vs `.pa` file).
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Workspace & Database Management' (Protocol in workflow.md)

## Phase 4: Final Integration & Refinement [checkpoint: 23fb1d2]
- [x] Task: Ensure clean state transitions and cross-platform hidden database files. (9549f28)
    - [ ] Write Tests: Verify gallery and database are cleared/reset when a new folder is opened.
    - [ ] Implement: Final wiring in `MainWindow` to ensure all components reset correctly during workspace changes.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Final Integration & Refinement' (Protocol in workflow.md)

## Phase 5: Thumbnail Engine & Persistent Storage
- [x] Task: Update database schema to store thumbnails. (266cfee)
    - [ ] Write Tests: Verify `images` table can store and retrieve BLOB data for thumbnails.
    - [ ] Implement: Add `thumbnail` column to `images` table in `src/database.py`.
- [x] Task: Create `ThumbnailGenerator` utility. (0888346)
    - [ ] Write Tests: Verify a thumbnail is correctly generated from a test image using Pillow.
    - [ ] Implement: Create `src/ui/thumbnail_gen.py` to handle scaling and conversion to bytes.
- [x] Task: Implement background thumbnail processing in `FolderScanner`. (006fb44)
    - [ ] Write Tests: Verify `FolderScanner` emits thumbnails along with file paths.
    - [ ] Implement: Update `FolderScanner` to generate (or load from DB) thumbnails during the scan.
- [ ] Task: Update `GalleryView` to display real thumbnails.
    - [ ] Write Tests: Verify `GalleryItem` can display a `QPixmap` from bytes.
    - [ ] Implement: Update `GalleryItem` and `GalleryView` to render the received thumbnail data.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Thumbnail Engine & Persistent Storage' (Protocol in workflow.md)
