# Initial Concept

I need a quick and simple image management tool for organizing scattered images from QQ files.

**Core Philosophy:**
- A geeky tool for statistics and data analysis, not just for reminiscing.
- Designed for rapid screening and selection of desired images.
- Scientific approach: statistics, analysis, and classification.

**Key Features:**

1.  **File Operations:**
    -   Use safe "move" operations (not copy/cut) to minimize SSD wear.
        - Selection actions:
            -   **Selection Mode:** Batch select images via long-press, right-click, or rubber-band drag.
            -   **Batch Actions:** "Select All", "Invert Selection", and "Cancel Selection" via a floating overlay.
            -   **Move Out:** Move selected items to a user-specified path.
            -   **Delete:** Send selected items to system recycle bin.
        -   **Workspace Management:**
            -   Folder-based workspaces with isolated analysis data.
            -   Automatic discovery of images in selected folders and subfolders.
            -   Hybrid storage: Centralized tracking of workspaces and localized analysis databases (`.pic_analyzer.db`).
            -   Cross-platform hidden file support for analysis data.
    
    2.  **Architecture:**
    
    -   Separation of business logic (App Layer) and Presentation (UI Layer).
    -   Analysis results stored in SQLite.
    -   **Performance:** Multi-threaded analysis.
    -   **Maintainability:** Factory pattern, plugin-based architecture for statistical rules.
    -   **On-demand Analysis:** Each statistical rule is triggered by a user button.

3.  **Image Preview:**
    -   Default: Tiled view (like Android gallery).
    -   **Full-Area Viewer:** Double-click or Mouse 5 to open a full-area overlay viewer with fade and slide animations.
    -   **Navigation:** Supports Keyboard arrows, Mouse wheel, and Mouse 4/5 for seamless browsing.
    -   **Animated Support:** Full support for GIF and WebP animations in the viewer.
    -   Grouped tiled views based on analysis results (e.g., by date).
    -   **Hierarchical Grouping:** Full-width visual headers for categorized views (e.g., by Date).
    -   **Granular Control:** Toggle between different grouping levels (e.g., Year, Month, Day for time-based views).

4.  **Statistical & Analysis Rules (Plugins):**
    -   pHash (Similarity)
    -   Color
    -   File Size
    -   Resolution
    -   Aspect Ratio (Landscape, Portrait, Ratios)
    -   Information Density (Size/Pixel)
    -   File Type (jpg, png, gif, etc.)

5.  **Sorting & Presentation:**
    -   **Extensible Sorting Plugins:** Dynamic loading of sorting algorithms (e.g., Ascending, Descending).
    -   **Statistical Sorting:** Normal Distribution Sorting (Peak First) based on calculated Mean (μ) and Sigma (σ).
    -   **On-Demand Metrics:** Toggleable display of group-level statistical insights.

6.  **Grouping Logic:**
    -   A group is the result of a set of statistical rules.
    -   Rules can be combined with AND/OR.
    -   Rules serve as both grouping and sorting criteria.
    -   Customizable priority order for rules within a group.
    -   *Example:* "Duplicate images, best quality first" -> Primary: pHash, Secondary: Info Density, Sort: Descending.

# Product Definition - Pic-Analyzer

## Target Audience
- **Primary Persona:** Data Hoarders, Archivists, Developers, and Data Scientists.
- **Proficiency:** High. Users are comfortable with file systems, metadata concepts, and technical analysis metrics (pHash, entropy).

## Core Vision
A "geeky," high-performance image management and analysis tool designed for scientific screening rather than nostalgic browsing. It prioritizes data-driven insights, safe file operations, and a plugin-based architecture for extensibility.

## Key Features
- **Utility-First UI:** A functional, data-dense interface following native Windows design patterns.
- **On-Demand Analysis:** Statistical rules are triggered manually via buttons to conserve resources.
- **Centralized App Layer:** Business logic, global state, and core services (DB, File Ops) are decoupled from the UI.
- **Lazy Loading:** UI elements and thumbnails are generated only as needed.
- **Workspace Management:** Users can open folders as discrete workspaces, with analysis data stored in hidden local databases.
- **Interactive Visualization:**
    - **Distribution Charts:** Histograms and scatter plots that act as interactive filters.
    - **Data Inspector:** A sidebar for deep-dives into raw metrics (pHash, information density).
- **Externalized Plugin System:** Users and developers can extend the application with new sorting and grouping algorithms via the root-level `./plugins` directory.
- **Safe Operations:** Strictly uses `move` operations to protect SSD lifespan and ensures analysis data (SQLite) is isolated from original files.

## High-Level Requirements
- Separation of core application logic and UI presentation.
- Multi-threaded processing for statistical plugins.
- Advanced grouping using AND/OR logic and prioritized rules.
