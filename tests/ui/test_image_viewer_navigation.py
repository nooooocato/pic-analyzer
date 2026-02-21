
import pytest
from unittest.mock import patch, MagicMock

from PySide6.QtCore import QObject, Signal

from src.ui.main_window.logic import MainWindow

@pytest.fixture
def main_app(qtbot):
    """Fixture to set up the main application window."""
    # Mock the app state initialization and plugin manager
    with patch('src.app.state.state.initialize'), \
         patch('src.app.state.state.plugin_manager') as mock_plugin_manager:
        
        # The sidebar UI needs some basic plugin lists to populate dropdowns
        mock_plugin_manager.group_plugins = {}
        mock_plugin_manager.sort_plugins = {}
        mock_plugin_manager.filter_plugins = {}

        main_win = MainWindow()
        qtbot.addWidget(main_win)
        yield main_win

def setup_gallery_with_filter(gallery, qtbot):
    """Helper function to populate and filter the gallery."""
    all_items = [{"path": f"path/to/image_{i}.jpg", "thumb": None} for i in range(10)]
    for item in all_items:
        gallery.add_item(item)
    qtbot.wait(100) # Wait for debounced refresh

    class MockFilterPlugin:
        def filter(self, items, params):
            return [item for item in items if item['path'] in [
                "path/to/image_2.jpg", "path/to/image_5.jpg", "path/to/image_8.jpg"
            ]]
    
    rules = {"filters": [{"type": "plugin", "plugin": MockFilterPlugin(), "params": {}}]}
    gallery.set_rules(rules)
    qtbot.wait(100)
    assert gallery.count() == 3

def test_navigation_respects_filtered_list_integration(main_app, qtbot):
    """
    Integration test to verify that the image viewer navigation respects
    the gallery's filtered and sorted list.
    """
    gallery = main_app.layout_engine.gallery
    viewer = main_app.layout_engine.image_viewer
    setup_gallery_with_filter(gallery, qtbot)

    first_filtered_image_path = gallery._visible_items[0]['path']
    
    with patch.object(viewer, '_set_media', return_value=None), \
         patch.object(viewer, 'switch_image') as mock_switch_image:
        
        gallery.item_activated.emit(first_filtered_image_path)
        qtbot.wait(100)
        
        viewer.next_requested.emit()
        qtbot.wait(100)
        
        expected_next_image_path = gallery._visible_items[1]['path']
        mock_switch_image.assert_called_with(expected_next_image_path, "next")

def test_navigation_wraps_around_at_end(main_app, qtbot):
    """Test that navigating past the end of the list wraps to the first item."""
    gallery = main_app.layout_engine.gallery
    viewer = main_app.layout_engine.image_viewer
    setup_gallery_with_filter(gallery, qtbot)

    last_filtered_image_path = gallery._visible_items[-1]['path'] # image_8

    with patch.object(viewer, '_set_media', return_value=None), \
         patch.object(viewer, 'switch_image') as mock_switch_image:

        gallery.item_activated.emit(last_filtered_image_path)
        qtbot.wait(100)
        
        viewer.next_requested.emit()
        qtbot.wait(100)
        
        expected_wrapped_image_path = gallery._visible_items[0]['path'] # image_2
        mock_switch_image.assert_called_with(expected_wrapped_image_path, "next")

def test_navigation_wraps_around_at_beginning(main_app, qtbot):
    """Test that navigating before the start of the list wraps to the last item."""
    gallery = main_app.layout_engine.gallery
    viewer = main_app.layout_engine.image_viewer
    setup_gallery_with_filter(gallery, qtbot)

    first_filtered_image_path = gallery._visible_items[0]['path'] # image_2

    with patch.object(viewer, '_set_media', return_value=None), \
         patch.object(viewer, 'switch_image') as mock_switch_image:

        gallery.item_activated.emit(first_filtered_image_path)
        qtbot.wait(100)
        
        viewer.prev_requested.emit()
        qtbot.wait(100)
        
        expected_wrapped_image_path = gallery._visible_items[-1]['path'] # image_8
        mock_switch_image.assert_called_with(expected_wrapped_image_path, "prev")

