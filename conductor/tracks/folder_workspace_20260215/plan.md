# Implementation Plan: Folder Selection & Workspace Management

## Phase 1: UI Foundations & Menu Bar [checkpoint: 81d866c]
- [x] Task: Add `QMenuBar` to `MainWindow` with `File > Open Folder` action. (81c1f55)
- [x] Task: Implement basic folder selection logic in `MainWindow`. (ed4a4f4)

## Phase 2: Threaded Recursive Scanner [checkpoint: 69cea1c]
- [x] Task: Create `FolderScanner` worker for background file discovery. (56e75b1)
- [x] Task: Integrate `FolderScanner` with `MainWindow` for real-time updates. (2ac9d33)

## Phase 3: Workspace & Database Management [checkpoint: f769477]
- [x] Task: Enhance `DatabaseManager` to support dynamic database switching. (193610e)
- [x] Task: Implement Workspace Prompt and Management logic. (4c81c3a)

## Phase 4: Final Integration & Refinement [checkpoint: 23fb1d2]
- [x] Task: Ensure clean state transitions and cross-platform hidden database files. (9549f28)

## Phase 5: Thumbnail Engine & Persistent Storage [checkpoint: 3dd0dac]
- [x] Task: Update database schema to store thumbnails. (266cfee)
- [x] Task: Create `ThumbnailGenerator` utility. (0888346)
- [x] Task: Implement background thumbnail processing in `FolderScanner`. (006fb44)
- [x] Task: Update `GalleryView` to display real thumbnails. (2f2eb16)
- [x] Task: Implement change detection and UI/UX refinements. (9c59232)
