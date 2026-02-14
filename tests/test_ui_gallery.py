import pytest
from PySide6.QtWidgets import QListWidget
from src.ui.gallery_view import GalleryView
from src.ui.main_window import MainWindow

def test_gallery_view_init(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    assert isinstance(gallery, QListWidget)

def test_main_window_has_gallery(qtbot):
    window = MainWindow()
    qtbot.addWidget(window)
    # Check if a GalleryView exists in central widget
    gallery = window.findChild(GalleryView)
    assert gallery is not None

def test_gallery_add_item(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    
    assert gallery.count() == 1
    item = gallery.item(0)
    assert item is not None

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
    
    assert gallery.count() == 1
    item = gallery.item(0)
    assert not item.icon().isNull()
