import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from src.ui.common.sidebar import SidebarContainer

def test_sidebar_container_initialization(qtbot):
    """Test that SidebarContainer initializes correctly as a QWidget."""
    sidebar = SidebarContainer()
    qtbot.addWidget(sidebar)
    
    assert isinstance(sidebar, QWidget)
    assert sidebar.layout() is not None
    assert isinstance(sidebar.layout(), QVBoxLayout)

def test_sidebar_sections_exist(qtbot):
    """Test that the initial sidebar contains the required sections."""
    sidebar = SidebarContainer()
    qtbot.addWidget(sidebar)
    
    # Check for sections (initially they might just be labels or placeholders)
    # The spec mentions: Grouping, Filtering, Sorting
    sections = [sidebar.layout().itemAt(i).widget() for i in range(sidebar.layout().count()) if sidebar.layout().itemAt(i).widget()]
    
    # We expect at least some indication of the three sections
    # This might change as we implement CollapsibleSection
    section_texts = [w.text() if hasattr(w, 'text') else "" for w in sections]
    
    # At least check the titles for now to drive implementation
    assert any("Grouping" in t for t in section_texts)
    assert any("Filtering" in t for t in section_texts)
    assert any("Sorting" in t for t in section_texts)
