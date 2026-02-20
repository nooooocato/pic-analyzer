import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from src.ui.common.sidebar import SidebarContainer
from src.ui.common.collapsible import CollapsibleSection

def test_sidebar_container_initialization(qtbot):
    """Test that SidebarContainer initializes correctly as a QWidget."""
    sidebar = SidebarContainer()
    qtbot.addWidget(sidebar)
    
    assert isinstance(sidebar, QWidget)
    assert sidebar.layout() is not None
    assert isinstance(sidebar.layout(), QVBoxLayout)

def test_sidebar_sections_exist(qtbot):
    """Test that the initial sidebar contains the required collapsible sections."""
    sidebar = SidebarContainer()
    qtbot.addWidget(sidebar)
    
    # Find all CollapsibleSection objects in the layout
    sections = [sidebar.layout().itemAt(i).widget() for i in range(sidebar.layout().count()) if isinstance(sidebar.layout().itemAt(i).widget(), CollapsibleSection)]
    
    assert len(sections) == 3
    
    section_titles = [s.title for s in sections]
    assert "Grouping" in section_titles
    assert "Filtering" in section_titles
    assert "Sorting" in section_titles
