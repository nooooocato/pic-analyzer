import pytest
from PySide6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PySide6.QtCore import Qt
from src.ui.common.collapsible import CollapsibleSection

def test_collapsible_section_initialization(qtbot):
    """Test that CollapsibleSection initializes with a title and content."""
    content = QLabel("Test Content")
    section = CollapsibleSection("Test Title", content)
    qtbot.addWidget(section)
    
    assert section.title == "Test Title"
    assert section.content_widget == content
    assert section.is_expanded is True # Default state: expanded

def test_collapsible_section_toggle(qtbot):
    """Test that the section expands and collapses when toggled."""
    content = QLabel("Test Content")
    section = CollapsibleSection("Test Title", content)
    qtbot.addWidget(section)
    
    # Initially NOT hidden
    assert content.isHidden() is False
    
    # Collapse
    section.toggle()
    assert section.is_expanded is False
    assert content.isHidden() is True
    
    # Expand
    section.toggle()
    assert section.is_expanded is True
    assert content.isHidden() is False

def test_collapsible_section_header_click(qtbot):
    """Test that clicking the header button toggles the section."""
    content = QLabel("Test Content")
    section = CollapsibleSection("Test Title", content)
    qtbot.addWidget(section)
    
    # Find the toggle button
    # The header button is usually what toggles it
    header_button = section.findChild(QPushButton)
    assert header_button is not None
    
    # Click it
    qtbot.mouseClick(header_button, Qt.LeftButton)
    assert section.is_expanded is False
    assert content.isHidden() is True
    
    # Click again
    qtbot.mouseClick(header_button, Qt.LeftButton)
    assert section.is_expanded is True
    assert content.isHidden() is False
