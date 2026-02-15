import pytest
from PySide6.QtGui import QAction
from PySide6.QtCore import Qt
from src.ui.main_window import MainWindow

def test_selection_overlay_initial_state(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    # Selection overlay should exist but be hidden initially
    assert hasattr(window, "selection_overlay")
    assert not window.selection_overlay.isVisible()

def test_selection_overlay_visibility_toggle(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.show()
    
    # Enable selection mode in gallery
    window.gallery.set_selection_mode_enabled(True)
    assert window.selection_overlay.isVisible()
    
    # Disable selection mode
    window.gallery.set_selection_mode_enabled(False)
    assert not window.selection_overlay.isVisible()

def test_selection_overlay_tooltips(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    
    assert window.selection_overlay.btn_all.toolTip() == "Select All"
    assert window.selection_overlay.btn_invert.toolTip() == "Invert Selection"
    assert window.selection_overlay.btn_cancel.toolTip() == "Cancel"

def test_selection_action_select_all(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.gallery.set_selection_mode_enabled(True)
    window.gallery.add_item("test1.jpg")
    window.gallery.add_item("test2.jpg")
    
    window._on_select_all()
    
    assert window.gallery.item(0).checkState() == Qt.Checked
    assert window.gallery.item(1).checkState() == Qt.Checked
    assert window.gallery.item(0).isSelected()
    assert window.gallery.item(1).isSelected()

def test_selection_action_invert(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.gallery.set_selection_mode_enabled(True)
    window.gallery.add_item("test1.jpg")
    window.gallery.add_item("test2.jpg")
    
    window.gallery.item(0).setCheckState(Qt.Checked)
    window.gallery.item(0).setSelected(True)
    
    window._on_invert_selection()
    
    assert window.gallery.item(0).checkState() == Qt.Unchecked
    assert not window.gallery.item(0).isSelected()
    assert window.gallery.item(1).checkState() == Qt.Checked
    assert window.gallery.item(1).isSelected()

def test_selection_action_cancel(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.gallery.set_selection_mode_enabled(True)
    window.gallery.add_item("test1.jpg")
    window.gallery.item(0).setCheckState(Qt.Checked)
    
    window._on_cancel_selection()
    
    assert not window.gallery.selection_mode_enabled
    assert not window.selection_overlay.isVisible()
    assert window.gallery.item(0).checkState() == Qt.Unchecked

def test_selection_esc_key(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    window.gallery.set_selection_mode_enabled(True)
    
    from PySide6.QtGui import QKeyEvent
    event = QKeyEvent(QKeyEvent.KeyPress, Qt.Key_Escape, Qt.NoModifier)
    window.keyPressEvent(event)
    
    assert not window.gallery.selection_mode_enabled
