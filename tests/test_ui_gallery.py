import pytest
from PySide6.QtWidgets import QScrollArea, QWidget
from src.ui.gallery_view import GalleryView
from src.ui.main_window import MainWindow

def test_gallery_view_init(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    assert isinstance(gallery, QScrollArea)
    assert gallery.widget() is not None

def test_main_window_has_gallery(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    # Check if a GalleryView exists in central widget
    gallery = window.findChild(GalleryView)
    assert gallery is not None

def test_gallery_add_item(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("Test Image")
    
    # Check if a GalleryItem was added to the layout
    items = gallery.findChildren(QWidget)
    # GalleryItem is a QFrame which is a QWidget. 
    # The container widget itself is also a child.
    # We look for children that are GalleryItem (or labels within them)
    from src.ui.gallery_view import GalleryItem
    gallery_items = gallery.findChildren(GalleryItem)
    assert len(gallery_items) == 1
    assert gallery_items[0].label.text() == "Test Image"

def test_gallery_add_thumbnail(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    
    # Create fake thumbnail bytes (a red 1x1 png)
    from PIL import Image
    import io
    img = Image.new('RGB', (1, 1), color='red')
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    thumb_bytes = buffer.getvalue()
    
    gallery.add_item("test.jpg", thumb_bytes)
    
    from src.ui.gallery_view import GalleryItem
    gallery_items = gallery.findChildren(GalleryItem)
    assert len(gallery_items) == 1
    # Check if pixmap is set on some label or custom property
    # We'll need to update GalleryItem to handle pixmap
    assert gallery_items[0].pixmap() is not None
