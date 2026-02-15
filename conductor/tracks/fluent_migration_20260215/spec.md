# Specification: Fluent Design Migration (PySide6-Fluent-Widgets)

## 1. Goal
Replace the current manual QSS-based UI implementation with **PySide6-Fluent-Widgets** to achieve a native Windows 11 aesthetic (Mica, Acrylic, animations) and reduce maintenance overhead.

## 2. Core Library
- **Library:** `PySide6-Fluent-Widgets`
- **License:** GPLv3 (Compatible with our current project structure).
- **Key Features to Adopt:**
    - `FluentWindow`: For native title bars and background effects.
    - `InfoBar`: To replace custom Toast notifications.
    - `Flyout` / `TeachingTip`: For overlays and context menus.
    - `FluentIcon`: For high-quality, scalable vector icons.

## 3. Architecture Impact
We will retain the **Triple-Python Pattern** (Logic/Layout/Style), but the content of these files will change:
- **`xxx.style.py`**: Will be significantly reduced. Instead of writing raw QSS, we will configure library component properties (e.g., `setBorderRadius`).
- **`xxx.layout.py`**: Will instantiate library widgets (e.g., `PrimaryPushButton` instead of `QPushButton`).
- **`xxx.logic.py`**: Minimal changes expected, mainly adapting to new signal signatures if they differ.

## 4. Visual Standards
- **Theme:** Auto-detect system theme (Dark/Light).
- **Icons:** Use `FluentIcon` enum exclusively. No mixed `QStyle.SP_` icons.
- **Typography:** `Segoe UI Variable` (handled automatically by the library).
