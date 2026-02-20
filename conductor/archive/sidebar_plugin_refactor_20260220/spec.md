# Specification - Sidebar & Plugin Refactor (2026-02-20)

## Overview
This track introduces a unified sidebar for image organization and refactors the plugin system to decouple logic from UI. The goals are to simplify plugin development, centralize control in a sidebar, and enable dynamic UI generation for plugin parameters.

## Functional Requirements

### 1. Unified Sidebar UI
- Implement a new sidebar (positioned on the left) containing three collapsible sections: **Grouping**, **Filtering**, and **Sorting**.
- All sections can be expanded or collapsed independently (Collapsible List style).
- Each section provides a dropdown menu to select the active rule (plugin).

### 2. Refactored Plugin Interface
- **Logic Isolation:** Plugins for `group`, `filter`, and `sort` will now focus exclusively on data processing and rule definition.
- **Parameter Schema:** Plugins must provide a **Typed Dictionary/JSON Schema** defining their configurable parameters (e.g., field names, types like `int`, `str`, `choice`, and default values).
- **Existing Rules Migration:** Refactor all current grouping and sorting plugins to conform to this new interface.

### 3. Dynamic UI Generation
- The sidebar will automatically generate appropriate input widgets (e.g., `QLineEdit`, `QComboBox`, `QSpinBox`) based on the active plugin's parameter schema.
- **Interaction Model (Hybrid):** 
    - Selecting a new rule from the dropdown triggers an **immediate (live)** update of the gallery.
    - Modifying parameters within a rule will show an **'Apply'** button to trigger the update, preventing excessive processing during typing/sliding.

### 4. Metadata Filtering
- Implement a 'Filter' section in the sidebar that supports basic metadata filtering (e.g., File Type, File Size, Date Range) using the new plugin pattern.

## Non-Functional Requirements
- **Performance:** Rule application must remain multi-threaded to ensure the UI stays responsive.
- **Maintainability:** Ensure the dynamic UI logic is centralized and easy to extend for new parameter types.

## Acceptance Criteria
- [ ] Sidebar is functional with three independently collapsible sections.
- [ ] Dropdown menus correctly list all available plugins for each category.
- [ ] Selecting a plugin dynamically populates its parameter UI in the sidebar.
- [ ] All existing grouping and sorting functionality is preserved after refactoring.
- [ ] Basic metadata filters are available in the Filter section.
- [ ] UI remains responsive during rule application.

## Out of Scope
- Advanced interactive distribution charts (histograms/scatter plots) integration in this phase.
- Complex nested boolean logic (e.g., `(A AND B) OR C`) for rule combinations.
