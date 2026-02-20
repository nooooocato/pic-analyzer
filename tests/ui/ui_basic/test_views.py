import pytest
from PySide6.QtCore import Qt
from src.ui.gallery.logic import GalleryView
from unittest.mock import MagicMock

def test_gallery_view_init(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    assert gallery._items == []
    assert gallery.verticalScrollBar().isVisible() is False

def test_gallery_view_add_item(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item({"path": "path1.jpg"})
    assert len(gallery._items) == 1
    assert gallery._items[0]['path'] == "path1.jpg"

def test_gallery_view_clear(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item({"path": "path1.jpg"})
    gallery.clear()
    assert len(gallery._items) == 0

def test_gallery_view_grouping(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item({"path": "path1.jpg"})
    gallery.add_item({"path": "path2.jpg"})

    qtbot.waitUntil(lambda: gallery.count() == 2, timeout=1000)

    mock_plugin = MagicMock()
    mock_plugin.group.return_value = {"2023-01": [{"path": "path1.jpg"}], "2023-02": [{"path": "path2.jpg"}]}
    
    gallery.set_rules({"group": {"plugin": mock_plugin, "params": {}}, "filter": {}, "sort": {}})
    assert len(gallery._group_widgets) == 2
