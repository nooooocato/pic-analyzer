# Specification: Image Viewer & Multi-Selection Mode

## Overview
Enhance the gallery experience by adding a dedicated full-area image viewer with smooth animations and implementing a robust multi-selection system for batch operations.

## Functional Requirements
### 1. Image Viewer (Overlay)
- **Trigger:** Double-click an image or press Mouse 5 (Forward) to view the image currently under the cursor.
- **UI Style:** A semi-transparent overlay that dims the gallery background.
- **Top Controls:** A permanent "Back" button in the top-left corner to return to the gallery.
- **Animations:** Slide or scale "Pop-up" and "Close" transitions.
- **Pagination:** 
    - "Previous" and "Next" buttons permanently visible on the left and right sides of the image.
    - Support for Keyboard Left/Right arrow keys to cycle images.
- **Navigation:**
    - Mouse 4 (Back) / Keyboard Esc / Top-left Back Button: Close viewer and return to gallery.
    - Mouse Wheel: Navigate between images.

### 2. Multi-Selection System
- **Triggers:**
    - Long-press on an image.
    - Right-click context menu action ("Select").
    - Rubber-band selection (click and drag in the gallery).
- **Selection UI:**
    - Active items display a visible checkbox in the corner.
    - Active items display a thick theme-colored border (Fluent Design style).
- **Batch Controls:**
    - When one or more items are selected, a context-sensitive toolbar section appears at the top.
    - Buttons: "Select All", "Invert Selection", and "Cancel Selection".

## Non-Functional Requirements
- **Performance:** Animations must maintain 60 FPS even with high-resolution image backgrounds.
- **Responsiveness:** Rubber-band selection must handle 1000+ items without UI lag.

## Acceptance Criteria
1. Double-clicking an image opens it in a full-area animated overlay.
2. Clicking the top-left "Back" button successfully exits the viewer.
3. Using Keyboard Left/Right arrows or clicking "Next/Previous" correctly cycles through images.
4. Pressing Mouse 4 button successfully exits the viewer.
5. Drag-selecting multiple images activates the multi-selection mode UI and displays the "Select All/Invert" buttons in the toolbar.
6. "Select All" correctly toggles the state of all images currently visible in the gallery.

## Out of Scope
- Direct file operations (Move/Delete) from the viewer (to be implemented in a separate track).
- Image zooming or rotation within the viewer.
