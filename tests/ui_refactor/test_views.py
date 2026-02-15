import pytest
from PySide6.QtCore import Qt
from src.ui.image_viewer.logic import ImageViewer
from src.ui.gallery.logic import GalleryView

def test_gallery_view_initial_state(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    assert gallery.count() == 0
    assert not gallery.selection_mode_enabled

def test_gallery_view_add_item(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    assert gallery.count() == 1
    # Check if a group was created
    assert len(gallery._group_widgets) == 1
    assert gallery._group_widgets[0].count() == 1

def test_gallery_view_selection_mode(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    
    gallery.set_selection_mode_enabled(True)
    assert gallery.selection_mode_enabled
    assert gallery._group_widgets[0].selection_mode_enabled
    
    gallery.set_selection_mode_enabled(False)
    assert not gallery.selection_mode_enabled
    assert not gallery._group_widgets[0].selection_mode_enabled
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    assert viewer.isHidden()
    assert viewer.layout_engine.btn_back is not None
    assert viewer.layout_engine.btn_prev is not None
    assert viewer.layout_engine.btn_next is not None

def test_image_viewer_signals(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    with qtbot.waitSignal(viewer.closed, timeout=1000):
        # Trigger close via back button (bypassing animation for speed if possible)
        # But here we test the real logic
        viewer.show_image("") # empty path still triggers some logic
        qtbot.mouseClick(viewer.layout_engine.btn_back, Qt.LeftButton)
        
    with qtbot.waitSignal(viewer.prev_requested, timeout=1000):
        qtbot.mouseClick(viewer.layout_engine.btn_prev, Qt.LeftButton)
        
    with qtbot.waitSignal(viewer.next_requested, timeout=1000):
        qtbot.mouseClick(viewer.layout_engine.btn_next, Qt.LeftButton)

def test_image_viewer_show_image(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    viewer.show_image("") # empty path
    assert viewer.isVisible()
    assert viewer.opacity_effect.opacity() == 0.0 # Starts at 0 for animation

def test_image_viewer_resize(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    viewer.show()
    
    viewer.resize(800, 600)
    assert viewer.layout_engine.current_label.width() == 800
    assert viewer.layout_engine.btn_next.x() > 700

def test_image_viewer_mouse_events(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    viewer.show()
    
    with qtbot.waitSignal(viewer.next_requested, timeout=1000):
        # Mouse button 5 (Forward) - XButton2
        qtbot.mousePress(viewer, Qt.XButton2)
        
    with qtbot.waitSignal(viewer.closed, timeout=1000):
        # Mouse button 4 (Back) - XButton1
        qtbot.mousePress(viewer, Qt.XButton1)

def test_image_viewer_wheel_event(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    viewer.show()
    
    with qtbot.waitSignal(viewer.next_requested, timeout=1000):
        # Scroll down -> next
        from PySide6.QtGui import QWheelEvent
        from PySide6.QtCore import QPointF, QPoint
        event = QWheelEvent(QPointF(10, 10), QPointF(10, 10), QPoint(0, 0), QPoint(0, -120), Qt.NoButton, Qt.NoModifier, Qt.ScrollUpdate, False)
        viewer.wheelEvent(event)
