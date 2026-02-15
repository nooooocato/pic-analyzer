# Track Specification: Advanced Sorting & Statistical Plugins

## 1.0 Overview
This track implements an extensible sorting framework for the gallery view. It introduces a dedicated plugin system for sorting algorithms, allowing the application to dynamically load rules like Ascending, Descending, and Normal Distribution (Peak First).

## 2.0 Functional Requirements

### 2.1 Plugin-Based Sorting Framework
- **Directory:** New sorting algorithms must be placed in `src/plugins/sort/`.
- **Architecture:** Each algorithm is a standalone Python file implementing a standard interface.
- **Dynamic Loading:** The application must automatically discover and load these plugins at startup.

### 2.2 Included Sorting Algorithms
- **Ascending:** Order items from lowest to highest value.
- **Descending:** Order items from highest to lowest value.
- **Normal Distribution (Peak First):** 
    - Calculate the Mean (μ) and Standard Deviation (σ) for a selected numeric metric.
    - Reorder items so those closest to the Mean appear first.

### 2.3 UI - Floating Sort Control
- **Location:** A floating button overlay in the top-right corner of the `GalleryView`.
- **Interaction:**
    - Clicking the button opens a menu to select the **Sort Metric** (detected from numeric DB columns/analysis results).
    - After selecting a metric, the user chooses the **Sorting Rule** (from loaded plugins).
- **Toggle Switch:** A "Show Stats" setting to display statistical feedback (Mean, Sigma) at the end of groups when enabled.

## 3.0 Technical Requirements
- **Plugin Interface:** Define a `BaseSortPlugin` that provides the algorithm logic.
- **Math Logic:** Use `numpy` or standard libraries for statistical calculations.
- **Database Integration:** The sorting system must query the `analysis_results` table for any numeric metrics provided by analysis plugins.

## 4.0 Acceptance Criteria
- [ ] Sorting algorithms are successfully loaded from `src/plugins/sort/`.
- [ ] Floating sort button is visible and displays available metrics and algorithms.
- [ ] Items are correctly reordered based on the selected metric and plugin logic.
- [ ] "Show Stats" toggle works correctly for the Normal Distribution plugin.

## 5.0 Out of Scope
- Sorting by non-numeric strings (except default filename/path).
