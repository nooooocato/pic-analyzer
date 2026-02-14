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
            -   **Move Out:** Move to a user-specified path.
            -   **Delete:** Send to system recycle bin.
        -   **Workspace Management:**
            -   Folder-based workspaces with isolated analysis data.
            -   Automatic discovery of images in selected folders and subfolders.
            -   Hybrid storage: Centralized tracking of workspaces and localized analysis databases (`.pic_analyzer.db`).
            -   Cross-platform hidden file support for analysis data.
    
    2.  **Architecture:**
    
    -   Separation of analysis and file manipulation.
    -   Analysis results stored in SQLite.
    -   **Performance:** Multi-threaded analysis.
    -   **Maintainability:** Factory pattern, plugin-based architecture for statistical rules.
    -   **On-demand Analysis:** Each statistical rule is triggered by a user button.

3.  **Image Preview:**
    -   Default: Tiled view (like Android gallery).
    -   Thumbnail view with click-to-view original.
    -   Grouped tiled views based on analysis results (e.g., by date).
    -   **Switchable grouping views (similar to Windows Explorer grouping).

4.  **Statistical & Analysis Rules (Plugins):**
    -   pHash (Similarity)
    -   Color
    -   File Size
    -   Resolution
    -   Aspect Ratio (Landscape, Portrait, Ratios)
    -   Information Density (Size/Pixel)
    -   File Type (jpg, png, gif, etc.)

5.  **Sorting & Presentation:**
    -   Ascending, Descending.
    -   Normal Distribution Sorting (Mean +/- Sigma).

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
- **Lazy Loading:** UI elements and thumbnails are generated only as needed.
- **Workspace Management:** Users can open folders as discrete workspaces, with analysis data stored in hidden local databases.
- **Interactive Visualization:**
    - **Distribution Charts:** Histograms and scatter plots that act as interactive filters.
    - **Data Inspector:** A sidebar for deep-dives into raw metrics (pHash, information density).
- **Safe Operations:** Strictly uses `move` operations to protect SSD lifespan and ensures analysis data (SQLite) is isolated from original files.

## High-Level Requirements
- Separation of analysis logic and file system manipulation.
- Multi-threaded processing for statistical plugins.
- Advanced grouping using AND/OR logic and prioritized rules.
