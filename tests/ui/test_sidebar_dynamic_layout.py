import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt
from src.ui.sidebar import SidebarContainer
from src.ui.common.collapsible import CollapsibleSection
from src.app.state import state

@pytest.fixture
def sidebar(qtbot):
    state.initialize()
    sb = SidebarContainer()
    qtbot.addWidget(sb)
    return sb

def test_sidebar_fixed_order(sidebar):
    """Sections should ALWAYS be in their default order (Filtering, Grouping, Sorting) in the splitter."""
    splitter = sidebar.findChild(QSplitter)
    assert splitter is not None
    assert splitter.count() == 3
    assert splitter.widget(0).title == "Filtering"
    assert splitter.widget(1).title == "Grouping"
    assert splitter.widget(2).title == "Sorting"
    
    # Collapse Filtering
    sidebar.filtering_section.toggle_button.setChecked(False)
    
    # Order should still be the same
    assert splitter.widget(0).title == "Filtering"
    assert splitter.widget(1).title == "Grouping"
    assert splitter.widget(2).title == "Sorting"
    
    # Expand Filtering, Collapse Grouping
    sidebar.filtering_section.toggle_button.setChecked(True)
    sidebar.grouping_section.toggle_button.setChecked(False)
    
    # Order should still be the same
    assert splitter.widget(0).title == "Filtering"
    assert splitter.widget(1).title == "Grouping"
    assert splitter.widget(2).title == "Sorting"

def test_sidebar_splitter_handles_all_sections(sidebar):
    """The splitter should manage all three sections."""
    splitter = sidebar.findChild(QSplitter)
    assert splitter is not None
    assert splitter.count() == 3
