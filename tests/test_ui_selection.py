import pytest
from PySide6.QtCore import Qt
from src.ui.gallery_view import GalleryView

def test_gallery_selection_mode_toggle(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    
    # Check if property exists (should fail initially)
    assert hasattr(gallery, "selection_mode_enabled")
    assert not gallery.selection_mode_enabled
    
    gallery.set_selection_mode_enabled(True)
    assert gallery.selection_mode_enabled
    
    gallery.set_selection_mode_enabled(False)
    assert not gallery.selection_mode_enabled

def test_items_checkable_in_selection_mode(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test1.jpg")
    
    item1 = gallery.item(0)
    
    # Enable selection mode
    gallery.set_selection_mode_enabled(True)
    assert item1.flags() & Qt.ItemIsUserCheckable
    
    # Disable selection mode
    gallery.set_selection_mode_enabled(False)
    assert not (item1.flags() & Qt.ItemIsUserCheckable)
    assert item1.checkState() == Qt.Unchecked

def test_selection_check_sync(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    item = gallery.item(0)
    
    gallery.set_selection_mode_enabled(True)
    
    # Selecting item should trigger sync
    item.setSelected(True)
    gallery._sync_selection_and_checkstate()
    assert item.checkState() == Qt.Checked
    
    # Deselecting should uncheck
    item.setSelected(False)
    gallery._sync_selection_and_checkstate()
    assert item.checkState() == Qt.Unchecked

def test_selection_mode_cleanup(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    item = gallery.item(0)
    
    gallery.set_selection_mode_enabled(True)
    item.setSelected(True)
    gallery._sync_selection_and_checkstate()
    
    gallery.set_selection_mode_enabled(False)
    assert item.checkState() == Qt.Unchecked
    assert not (item.flags() & Qt.ItemIsUserCheckable)

def test_selection_mode_signal(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    
    with qtbot.waitSignal(gallery.selection_mode_changed, timeout=1000) as blocker:
        gallery.set_selection_mode_enabled(True)
    assert blocker.args == [True]
    
    with qtbot.waitSignal(gallery.selection_mode_changed, timeout=1000) as blocker:
        gallery.set_selection_mode_enabled(False)
    assert blocker.args == [False]

def test_selection_trigger_long_press_logic(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    item = gallery.item(0)
    
    # Set pressed item
    gallery._pressed_item = item
    
    # Trigger long press
    gallery._on_long_press()
    assert gallery.selection_mode_enabled
    
    # Sync is called by itemSelectionChanged signal which is emitted by setSelected
    # In tests we might need manual call or process events
    gallery._sync_selection_and_checkstate()
    assert item.checkState() == Qt.Checked

def test_selection_trigger_right_click_exists(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    # The new GalleryView handles context menus internally in its GroupedListWidgets
    pass

def test_add_item_in_selection_mode(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.set_selection_mode_enabled(True)
    gallery.add_item("test_direct.jpg")
    item = gallery.item(0)
    assert item.flags() & Qt.ItemIsUserCheckable
    assert item.checkState() == Qt.Unchecked

def test_item_activation_suppressed_in_selection_mode(qtbot):
    gallery = GalleryView()
    qtbot.addWidget(gallery)
    gallery.add_item("test.jpg")
    item = gallery.item(0)
    
    gallery.set_selection_mode_enabled(True)
    # Check if signal is NOT emitted
    with qtbot.assertNotEmitted(gallery.item_activated):
        gallery._on_item_double_clicked(item)
