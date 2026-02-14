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

def test_on_open_folder_selects_directory(qtbot, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Mock QFileDialog.getExistingDirectory to return a specific path
    test_path = "/fake/path/to/images"
    def mock_get_existing_directory(*args, **kwargs):
        return test_path
    
    from PySide6.QtWidgets import QFileDialog
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", mock_get_existing_directory)
    
    # Trigger the action
    window._on_open_folder()
    
    # Check if the window has stored the selected path (we'll need to implement this)
    assert window.current_folder == test_path

def test_on_open_folder_starts_scanner(qtbot, monkeypatch):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Mock QFileDialog
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: "/fake/path")
    
    # Mock QThreadPool.start to verify scanner is started
    started_runnable = []
    from PySide6.QtCore import QThreadPool
    monkeypatch.setattr(QThreadPool, "start", lambda self, runnable: started_runnable.append(runnable))
    
    window._on_open_folder()
    
    assert len(started_runnable) == 1
    from src.file_scanner import FolderScanner
    assert isinstance(started_runnable[0], FolderScanner)

def test_main_window_adds_image_on_signal(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Initial count
    initial_count = window.gallery.layout.count()
    
    # Simulate a file being found
    test_image = "test.jpg"
    window._on_file_found(test_image)
    
    # Verify it was added to the gallery
    assert window.gallery.layout.count() == initial_count + 1
