import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from src.ui.sidebar import SidebarContainer
from src.ui.common.collapsible import CollapsibleSection
from src.app.state import state

def test_sidebar_container_initialization(qtbot):
    """Test that SidebarContainer initializes correctly as a QWidget."""
    state.initialize()
    sidebar = SidebarContainer()
    qtbot.addWidget(sidebar)
    
    assert isinstance(sidebar, QWidget)
    assert sidebar.layout() is not None
    assert isinstance(sidebar.layout(), QVBoxLayout)

def test_sidebar_sections_exist(qtbot):
    """Test that the initial sidebar contains the required collapsible sections."""
    state.initialize()
    sidebar = SidebarContainer()
    qtbot.addWidget(sidebar)
    
    # Find all CollapsibleSection objects
    sections = sidebar.findChildren(CollapsibleSection)
    
    assert len(sections) == 3
    
    section_titles = [s.title for s in sections]
    assert "Grouping" in section_titles
    assert "Filtering" in section_titles
    assert "Sorting" in section_titles
