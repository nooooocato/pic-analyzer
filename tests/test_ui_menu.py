import pytest
from PySide6.QtWidgets import QMainWindow, QMenuBar
from PySide6.QtGui import QAction
from src.ui.main_window import MainWindow

def test_main_window_has_menu_bar(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    menu_bar = window.menuBar()
    assert menu_bar is not None
    assert isinstance(menu_bar, QMenuBar)

def test_file_menu_exists(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    menu_bar = window.menuBar()
    actions = menu_bar.actions()
    file_menu_action = next((a for a in actions if a.text().replace("&", "") == "File"), None)
    assert file_menu_action is not None
    assert file_menu_action.menu() is not None

def test_open_folder_action_exists(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    menu_bar = window.menuBar()
    actions = menu_bar.actions()
    file_menu_action = next((a for a in actions if a.text().replace("&", "") == "File"), None)
    assert file_menu_action is not None
    
    file_menu = file_menu_action.menu()
    menu_actions = file_menu.actions()
    open_folder_action = next((a for a in menu_actions if a.text().replace("&", "") == "Open Folder"), None)
    assert open_folder_action is not None
    assert isinstance(open_folder_action, QAction)
