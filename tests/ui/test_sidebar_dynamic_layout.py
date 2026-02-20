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

def test_sidebar_initial_order(sidebar):
    """Initially, all sections should be in their default order (Filtering, Grouping, Sorting) in the splitter."""
    splitter = sidebar.findChild(QSplitter)
    assert splitter is not None
    assert splitter.count() == 3
    assert splitter.widget(0).title == "Filtering"
    assert splitter.widget(1).title == "Grouping"
    assert splitter.widget(2).title == "Sorting"

def test_sidebar_dynamic_reordering_on_expansion(sidebar, qtbot):
    """Expanded sections should move to the top splitter, collapsed to the bottom layout."""
    
    # Initially all are expanded.
    # Collapse Filtering and Sorting, leave Grouping expanded.
    sidebar.filtering_section.toggle_button.setChecked(False)
    sidebar.sorting_section.toggle_button.setChecked(False)
    sidebar.grouping_section.toggle_button.setChecked(True)
    
    # Splitter should have only Grouping
    splitter = sidebar.findChild(QSplitter)
    assert splitter.count() == 1
    assert splitter.widget(0).title == "Grouping"
    
    # Collapsed layout should have Filtering and Sorting
    collapsed_container = sidebar.layout_engine.collapsed_container
    collapsed_layout = sidebar.layout_engine.collapsed_layout
    
    # Check widgets in collapsed_layout
    widgets = []
    for i in range(collapsed_layout.count()):
        w = collapsed_layout.itemAt(i).widget()
        if w: widgets.append(w)
    
    assert [w.title for w in widgets] == ["Filtering", "Sorting"]

def test_sidebar_splitter_initialization(sidebar):
    """Expanded sections should be managed by a QSplitter."""
    sidebar.filtering_section.toggle_button.setChecked(True)
    sidebar.grouping_section.toggle_button.setChecked(True)
    sidebar.sorting_section.toggle_button.setChecked(False)
    
    splitter = sidebar.findChild(QSplitter)
    assert splitter is not None
    assert splitter.count() == 2
    
    # Verify Filtering is above Grouping in splitter (Filter > Group > Sort)
    assert splitter.widget(0).title == "Filtering"
    assert splitter.widget(1).title == "Grouping"

def test_sidebar_all_collapsed(sidebar):
    """Test when all sections are collapsed."""
    sidebar.filtering_section.toggle_button.setChecked(False)
    sidebar.grouping_section.toggle_button.setChecked(False)
    sidebar.sorting_section.toggle_button.setChecked(False)
    
    splitter = sidebar.findChild(QSplitter)
    assert splitter.isHidden()
    
    collapsed_container = sidebar.layout_engine.collapsed_container
    assert not collapsed_container.isHidden()
    assert sidebar.layout_engine.collapsed_layout.count() == 3

def test_sidebar_all_expanded(sidebar):
    """Test when all sections are expanded."""
    sidebar.filtering_section.toggle_button.setChecked(True)
    sidebar.grouping_section.toggle_button.setChecked(True)
    sidebar.sorting_section.toggle_button.setChecked(True)
    
    splitter = sidebar.findChild(QSplitter)
    assert not splitter.isHidden()
    assert splitter.count() == 3
    
    collapsed_container = sidebar.layout_engine.collapsed_container
    assert collapsed_container.isHidden()
