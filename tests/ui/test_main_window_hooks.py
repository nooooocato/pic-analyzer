import pytest
from src.ui.main_window.logic import MainWindow
from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction

def test_main_window_registration_hooks(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Test getting a menu
    view_menu = window.get_menu("View")
    assert view_menu is not None
    assert isinstance(view_menu, QMenu)
    
    # Test adding to toolbar
    action = QAction("Test Action", window)
    window.add_toolbar_action(action)
    assert action in window.layout_engine.toolbar.actions()

    # Test adding a new menu
    new_menu = window.get_menu("Plugins")
    assert new_menu is not None
    assert new_menu.title() == "&Plugins"
