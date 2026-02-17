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
    
    # Debounce is 50ms, wait a bit
    qtbot.waitUntil(lambda: gallery.count() == 1, timeout=1000)
    
    # Check if a group was created
    assert len(gallery._group_widgets) == 1
    assert gallery._group_widgets[0].count() == 1

from unittest.mock import MagicMock

def test_gallery_view_grouping(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("path1.jpg")
    gallery.add_item("path2.jpg")
    
    qtbot.waitUntil(lambda: gallery.count() == 2, timeout=1000)
    
    mock_plugin = MagicMock()
    mock_plugin.run.side_effect = lambda path, gran: {"date": "2023-01"} if "path1" in path else {"date": "2023-02"}
    
    gallery.set_grouping(mock_plugin)
    assert len(gallery._group_widgets) == 2
    assert gallery.layout_engine.container_layout.count() >= 3 # 2 groups + stretch

from src.ui.gallery.style import GalleryItemDelegate
from PySide6.QtGui import QImage, QPainter
from PySide6.QtWidgets import QStyleOptionViewItem

def test_gallery_item_delegate_paint(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg") # Add item to ensure index is valid
    
    qtbot.waitUntil(lambda: len(gallery._group_widgets) > 0, timeout=1000)
    
    delegate = GalleryItemDelegate(gallery)
    
    image = QImage(200, 200, QImage.Format_RGB32)
    painter = QPainter(image)
    try:
        option = QStyleOptionViewItem()
        option.rect = image.rect()
        index = gallery._group_widgets[0].model().index(0, 0)
        delegate.paint(painter, option, index)
    finally:
        painter.end()

def test_gallery_view_esc_exits_selection(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    
    qtbot.waitUntil(lambda: len(gallery._group_widgets) > 0, timeout=1000)
    
    gallery.set_selection_mode_enabled(True)
    assert gallery.selection_mode_enabled
    
    # Simulating Esc key on the group widget which has focus
    qtbot.keyClick(gallery._group_widgets[0], Qt.Key_Escape)
    assert not gallery.selection_mode_enabled

def test_image_viewer_close(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    viewer.show_image("test.jpg")
    
    with qtbot.waitSignal(viewer.closed, timeout=1000):
        viewer.close_viewer()
    assert viewer.isHidden()

def test_image_viewer_signals(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    with qtbot.waitSignal(viewer.closed, timeout=1000):
        viewer.show_image("") 
        qtbot.mouseClick(viewer.layout_engine.btn_back, Qt.LeftButton)
        
    with qtbot.waitSignal(viewer.prev_requested, timeout=1000):
        qtbot.mouseClick(viewer.layout_engine.btn_prev, Qt.LeftButton)
        
    with qtbot.waitSignal(viewer.next_requested, timeout=1000):
        qtbot.mouseClick(viewer.layout_engine.btn_next, Qt.LeftButton)

def test_image_viewer_show_image(qtbot):
    viewer = ImageViewer()
    qtbot.addWidget(viewer)
    
    viewer.show_image("") 
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
