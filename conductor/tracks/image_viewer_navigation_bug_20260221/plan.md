# Implementation Plan: Image Viewer Navigation Bug

This plan outlines the steps to fix the bug where the image viewer does not respect the gallery's filtered and sorted order.

## Phase 1: Replicate the Bug with a Failing Test

- `[ ]` **Task:** Create a new test file `tests/ui/test_image_viewer_navigation.py`.
    - `[ ]` Sub-task: Set up a mock `GalleryView` that can provide a filtered/sorted list of image paths.
    - `[ ]` Sub-task: Write a test `test_navigation_respects_filtered_list`.
        - `[ ]` In the test, create a mock gallery with 10 images.
        - `[ ]` "Apply" a filter that results in a list of 3 specific images (e.g., items 2, 5, 8).
        - `[ ]` "Open" the viewer with the first item from the filtered list (item 2).
        - `[ ]` Simulate a "next" action.
        - `[ ]` Assert that the viewer now shows the second item from the filtered list (item 5), not the next item from the original list (item 3).
    - `[ ]` Sub-task: Run the test and confirm it fails as expected (Red phase).
- `[ ]` **Task:** Conductor - User Manual Verification 'Replicate the Bug with a Failing Test' (Protocol in workflow.md)

## Phase 2: Implement the Fix

- `[ ]` **Task:** Modify the `GalleryView` to pass the current item list to the `ImageViewer`.
    - `[ ]` Sub-task: Locate the signal or method call that opens the `ImageViewer`.
    - `[ ]` Sub-task: Instead of passing a single image path, modify it to pass the full list of image paths currently displayed in the gallery and the index of the selected item.
- `[ ]` **Task:** Update the `ImageViewer` to use the new item list.
    - `[ ]` Sub-task: Modify `ImageViewer.__init__` or a setup method to accept and store the list of image paths and the current index.
    - `[ ]` Sub-task: Refactor the `go_next` and `go_previous` methods to increment/decrement the current index and retrieve the corresponding path from the stored list.
- `[ ]` **Task:** Run the tests from Phase 1 and confirm they now pass (Green phase).
- `[ ]` **Task:** Conductor - User Manual Verification 'Implement the Fix' (Protocol in workflow.md)

## Phase 3: Refactoring and Final Testing

- `[ ]` **Task:** Refactor the code for clarity and simplicity.
    - `[ ]` Sub-task: Review the changes in `GalleryView` and `ImageViewer` for any code smells or opportunities for improvement.
    - `[ ]` Sub-task: Ensure the navigation logic correctly handles edge cases (first item, last item).
- `[ ]` **Task:** Add more tests for edge cases.
    - `[ ]` Sub-task: Write a test for navigating past the end of the list (e.g., it should loop or disable the button).
    - `[ ]` Sub-task: Write a test for navigating before the beginning of the list.
- `[ ]` **Task:** Run all related tests again to ensure no regressions were introduced.
- `[ ]` **Task:** Conductor - User Manual Verification 'Refactoring and Final Testing' (Protocol in workflow.md)
