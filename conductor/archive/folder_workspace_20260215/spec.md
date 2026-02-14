# Specification: Folder Selection & Workspace Management (Demo Transition)

## Overview
Transform the current MVP into a functional demo that allows users to select a local folder, recursively scan it for images, and manage the resulting analysis data as "Workspaces."

## Functional Requirements
- **Folder Selection:**
    - Implement a standard menu bar with `File > Open Folder`.
    - Use a native system folder picker dialog.
- **Recursive Scanning:**
    - Automatically find all image files (supported formats: JPG, PNG, GIF, WEBP, BMP) in the selected folder and all subfolders.
- **Real-time Gallery Updates:**
    - The UI must update dynamically as images are discovered, rather than waiting for the entire scan to complete.
- **Workspace Management:**
    - **Prompt on Change:** When opening a new folder, prompt the user to save the current workspace or clear it.
    - **Hybrid Storage:**
        - **Centralized:** Automatically track workspaces in the application's local data directory for quick access.
        - **File-based:** Support saving/loading `.pa` files to store analysis data (SQLite path + metadata) in user-defined locations.
- **SQLite Integration:**
    - Each workspace maps to a specific SQLite database instance containing the analysis results.

## Non-Functional Requirements
- **Threaded Scanning:** File system scanning must occur on a background thread to prevent UI freezing.
- **Responsive UI:** The gallery should handle large numbers of images (1000+) efficiently using existing lazy-loading principles.

## Acceptance Criteria
1. User can click "File > Open Folder" and pick a directory.
2. The gallery begins populating with images from that directory and its subdirectories immediately.
3. If a workspace is already active, the user is asked if they want to save/close it before opening the new one.
4. The application correctly creates or loads a SQLite database associated with the selected folder.

## Out of Scope
- Advanced "Recent Workspaces" list (to be handled in a future track).
- Multi-folder selection in a single workspace.
