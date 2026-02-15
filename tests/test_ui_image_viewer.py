import pytest
from PySide6.QtWidgets import QWidget
from src.ui.image_viewer import ImageViewer

def test_image_viewer_init(qtbot):
    parent = QWidget()
    viewer = ImageViewer(parent)
    qtbot.addWidget(viewer)
    
    assert viewer.parent() == parent
    assert viewer.isHidden() # Should be hidden by default

def test_image_viewer_covers_parent(qtbot):
    parent = QWidget()
    parent.resize(800, 600)
    viewer = ImageViewer(parent)
    qtbot.addWidget(viewer)
    
    # Pass a valid-looking dummy path
    viewer.show_image("dummy.jpg")
    # Overlay should match parent size
    assert viewer.size() == parent.size()

def test_image_viewer_controls_exist(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    assert hasattr(viewer, "btn_back")
    assert hasattr(viewer, "btn_prev")
    assert hasattr(viewer, "btn_next")
    assert hasattr(viewer, "current_label")

def test_image_viewer_back_button(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    viewer.show()
    
    with qtbot.waitSignal(viewer.closed, timeout=1000):
        viewer.btn_back.click()
    assert viewer.isHidden()
