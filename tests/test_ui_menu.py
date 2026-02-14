import pytest
import os
from PySide6.QtWidgets import QMainWindow, QMenuBar, QMessageBox
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

def test_on_open_folder_selects_directory(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Mock QFileDialog.getExistingDirectory to return a specific path
    test_path = str(tmp_path / "fake_images")
    os.makedirs(test_path)
    
    def mock_get_existing_directory(*args, **kwargs):
        return test_path
    
    from PySide6.QtWidgets import QFileDialog
    monkeypatch.setattr(QFileDialog, "getExistingDirectory", mock_get_existing_directory)
    
    # Mock global thread pool start to avoid side effects
    monkeypatch.setattr("PySide6.QtCore.QThreadPool.start", lambda self, runnable: None)

    # Trigger the action
    window._on_open_folder()
    
    # Check if the window has stored the selected path (we'll need to implement this)
    assert window.current_folder == test_path

def test_on_open_folder_starts_scanner(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    
    test_path = str(tmp_path / "fake_scanner_path")
    os.makedirs(test_path)

    # Mock QFileDialog
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: test_path)
    
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

def test_on_open_folder_prompts_if_active(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    
    old_path = str(tmp_path / "old_path")
    new_path = str(tmp_path / "new_path")
    os.makedirs(old_path)
    os.makedirs(new_path)

    # Set an active folder
    window.current_folder = old_path
    
    # Mock QFileDialog to return a new path
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: new_path)
    
    # Mock QMessageBox.question to return Yes (Accept change)
    from PySide6.QtWidgets import QMessageBox
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
    
    # Mock _start_scan to avoid side effects
    monkeypatch.setattr(window, "_start_scan", lambda path: None)
    
    window._on_open_folder()
    
    assert window.current_folder == new_path

def test_on_open_folder_cancel_prompt(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    
    old_path = str(tmp_path / "old_path_cancel")
    new_path = str(tmp_path / "new_path_cancel")
    os.makedirs(old_path)
    os.makedirs(new_path)

    # Set an active folder
    window.current_folder = old_path
    
    # Mock QFileDialog to return a new path
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: new_path)
    
    # Mock QMessageBox.question to return No (Cancel change)
    from PySide6.QtWidgets import QMessageBox
    monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
    
    window._on_open_folder()
    
    # Should NOT change folder
    assert window.current_folder == old_path

def test_on_open_folder_switches_db(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    
    new_folder = str(tmp_path / "new_workspace")
    os.makedirs(new_folder)
    
    # Mock QFileDialog
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: new_folder)
    
    # Mock _start_scan to avoid thread pool issues in this test, 
    # but we want to check db_manager.switch_database which is called in _start_scan.
    # Actually, let's let _start_scan run but mock QThreadPool.globalInstance().start
    monkeypatch.setattr("PySide6.QtCore.QThreadPool.start", lambda self, runnable: None)
    
    window._on_open_folder()
    
    expected_db = os.path.join(new_folder, ".pic_analyzer.db")
    assert window.db_manager.db_path == expected_db
    assert os.path.exists(expected_db)

def test_on_open_folder_clears_gallery(qtbot, monkeypatch, tmp_path):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Add an item to the gallery
    window.gallery.add_item("old_image.jpg")
    assert window.gallery.layout.count() == 1
    
    # Mock QFileDialog
    new_folder = str(tmp_path / "clear_gallery_test")
    os.makedirs(new_folder)
    monkeypatch.setattr("PySide6.QtWidgets.QFileDialog.getExistingDirectory", lambda *args: new_folder)
    
    # Mock QThreadPool.start
    monkeypatch.setattr("PySide6.QtCore.QThreadPool.start", lambda self, runnable: None)
    
    window._on_open_folder()
    
    # Gallery should be cleared
    assert window.gallery.layout.count() == 0
