# Specification: Image Viewer Navigation Bug

## 1. Overview

A bug has been identified in the image viewer's navigation functionality. When a user applies filtering, sorting, or grouping rules to the image gallery, the image viewer does not respect the resulting order when navigating between images (next/previous). Instead, it traverses the images in their original, unmodified order. This creates a disjointed and confusing user experience, as the viewer's navigation does not match the gallery's presentation.

## 2. Functional Requirements

### 2.1. Image Viewer State Synchronization

- The Image Viewer MUST be aware of the currently active list of images as determined by the gallery's applied rules (filters, sorting, grouping).
- When the user opens the image viewer for a specific image, the viewer MUST receive the complete, ordered list of images from the gallery view, not just the single image path.

### 2.2. Navigation Logic

- Clicking "Next" (or using the right arrow key / mouse forward button) in the image viewer MUST display the next image in the sequence provided by the gallery's current state.
- Clicking "Previous" (or using the left arrow key / mouse back button) in the image viewer MUST display the previous image in the sequence provided by the gallery's current state.
- If the user is viewing the last image in the filtered list, the "Next" button should be disabled or loop back to the first image.
- If the user is viewing the first image in the filtered list, the "Previous" button should be disabled or loop back to the last image.

## 3. Acceptance Criteria

- **GIVEN** a user has applied a filter that reduces the number of visible images.
- **WHEN** the user opens an image in the viewer from the filtered list.
- **AND** the user clicks the "Next" button.
- **THEN** the viewer MUST show the next image from the filtered list, not the next image from the original, unfiltered list.

- **GIVEN** a user has applied a sorting rule that changes the order of images.
- **WHEN** the user opens the first image in the sorted list.
- **AND** the user clicks the "Next" button.
- **THEN** the viewer MUST show the second image according to the new sort order.

- **GIVEN** a user has applied a grouping rule.
- **WHEN** the user is viewing the last image of a group.
- **AND** the user clicks "Next".
- **THEN** the viewer MUST show the first image of the *next* group.
