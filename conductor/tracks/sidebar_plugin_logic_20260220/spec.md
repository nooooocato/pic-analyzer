# Specification: Sidebar & Plugin Logic Upgrade

#### Overview
This track will upgrade the Rule Sidebar to support dynamic layout management, resizable sections via splitters, and compound logic for filtering and sorting. Filter configurations will support AND/OR logic per item, and sorting will support sequential "Then" logic with drag-and-drop reordering. All states will be automatically persisted to the workspace.

#### Functional Requirements
1.  **Sidebar Layout & Splitter:**
    -   **Fixed Order:** Maintain a fixed relative order (Filter > Group > Sort) regardless of expansion state.
    -   **Resizable Sections:** Implement a splitter managing all sections to allow users to manually adjust the vertical space allocated to each expanded section.
    -   **Compact Design:** When collapsed, sections take minimal height (header only).
    -   **Robust Reordering:** Drag-and-drop must be resilient; items should never disappear if dropped in invalid areas.
2.  **Compound Filtering:**
    -   **Multi-Item Support:** Allow users to add multiple filter items within the Filter section via a "+" button.
    -   **Logical Connectors:** Implement "AND" / "OR" dropdowns between adjacent filter items to define complex selection logic.
    -   **Gallery Integration:** When any filter is active, a "Filtered Images" header is permanently anchored at the top of the gallery.
3.  **Sequential Sorting:**
    -   **Multi-Item Support:** Allow adding multiple sort items via a "+" button.
    -   **Stable Reordering:** Priority is defined top-to-bottom in the UI (Top = Primary). Logic uses stable sequential sorting in reverse order to achieve this.
4.  **State Persistence:**
    -   **Auto-Save:** The current configuration of filters (types, parameters, connectors, active state) and sorts (types, parameters, order) will be automatically saved to the workspace database.
    -   **Restoration:** Reopening a workspace will restore the exact sidebar configuration and rule sets.

#### Acceptance Criteria
-   Expanding a section moves it to the expanded group while maintaining its relative order among other expanded items.
-   Splitters correctly resize expanded sections without breaking the layout.
-   Filter logic (AND/OR) correctly influences the image selection in the gallery.
-   Sequential sorting correctly orders images according to the defined hierarchy.
-   Workspace state is successfully persisted and restored.

#### Out of Scope
-   Development of new individual filter/sort algorithms (focus is on the framework).
-   Manual naming or management of multiple presets (focus is on auto-save).
