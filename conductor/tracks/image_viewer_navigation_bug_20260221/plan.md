# Implementation Plan: Image Viewer Navigation Bug

This plan outlines the steps to fix the bug where the image viewer does not respect the gallery's filtered and sorted order.

## Phase 1: Replicate the Bug with a Failing Test

- `[x]` **Task:** Create a new test file `tests/ui/test_image_viewer_navigation.py`.
    - `[x]` Sub-task: Set up a mock `GalleryView` that can provide a filtered/sorted list of image paths.
    - `[x]` Sub-task: Write a test `test_navigation_respects_filtered_list`.
        - `[x]` In the test, create a mock gallery with 10 images.
        - `[x]` "Apply" a filter that results in a list of 3 specific images (e.g., items 2, 5, 8).
        - `[x]` "Open" the viewer with the first item from the filtered list (item 2).
        - `[x]` Simulate a "next" action.
        - `[x]` Assert that the viewer now shows the second item from the filtered list (item 5), not the next item from the original list (item 3).
    - `[x]` Sub-task: Run the test and confirm it fails as expected (Red phase).
- `[x]` **Task:** Conductor - User Manual Verification 'Replicate the Bug with a Failing Test' (Protocol in workflow.md)

## Phase 2: Implement the Fix

- `[x]` **Task:** Modify the `GalleryView` to pass the current item list to the `ImageViewer`.
    - `[x]` Sub-task: Locate the signal or method call that opens the `ImageViewer`.
    - `[x]` Sub-task: Instead of passing a single image path, modify it to pass the full list of image paths currently displayed in the gallery and the index of the selected item.
- `[x]` **Task:** Update the `ImageViewer` to use the new item list.
    - `[x]` Sub-task: Modify `ImageViewer.__init__` or a setup method to accept and store the list of image paths and the current index.
    - `[x]` Sub-task: Refactor the `go_next` and `go_previous` methods to increment/decrement the current index and retrieve the corresponding path from the stored list.
- `[x]` **Task:** Run the tests from Phase 1 and confirm they now pass (Green phase).
- `[x]` **Task:** Conductor - User Manual Verification 'Implement the Fix' (Protocol in workflow.md)

## Phase 3: Refactoring and Final Testing

- `[x]` **Task:** Refactor the code for clarity and simplicity.
    - `[x]` Sub-task: Review the changes in `GalleryView` and `ImageViewer` for any code smells or opportunities for improvement.
    - `[x]` Sub-task: Ensure the navigation logic correctly handles edge cases (first item, last item).
- `[x]` **Task:** Add more tests for edge cases.
    - `[x]` Sub-task: Write a test for navigating past the end of the list (e.g., it should loop or disable the button).
    - `[x]` Sub-task: Write a test for navigating before the beginning of the list.
- `[x]` **Task:** Run all related tests again to ensure no regressions were introduced.
- `[x]` **Task:** Conductor - User Manual Verification 'Refactoring and Final Testing' (Protocol in workflow.md)
