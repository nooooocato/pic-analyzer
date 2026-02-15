import pytest
from unittest.mock import patch, MagicMock
from PySide6.QtWidgets import QApplication, QWidget
from src.ui.common.toast.logic import Toast
from qfluentwidgets import InfoBar, InfoBarPosition

@pytest.fixture
def app(qtbot):
    return QApplication.instance() or QApplication([])

def test_toast_wrapper(qtbot):
    parent = QWidget()
    toast = Toast("Initial", parent=parent)
    
    with patch('qfluentwidgets.InfoBar.info') as mock_info:
        toast.show_message("Hello World")
        
        mock_info.assert_called_once()
        args, kwargs = mock_info.call_args
        
        # InfoBar.info(title, content, ..., parent=parent, ...)
        # Using kwargs verification is safer as argument order might vary or defaults used
        
        # Check title (either arg 0 or keyword 'title')
        title = kwargs.get('title') or (args[0] if len(args) > 0 else None)
        assert title == 'Info'
        
        # Check content (arg 1 or keyword 'content')
        content = kwargs.get('content') or (args[1] if len(args) > 1 else None)
        assert content == "Hello World"
        
        # Check parent
        assert kwargs.get('parent') == parent
        # Check position
        assert kwargs.get('position') == InfoBarPosition.TOP_RIGHT

def test_toast_types(qtbot):
    parent = QWidget()
    toast = Toast("Initial", parent=parent)

    with patch('qfluentwidgets.InfoBar.success') as mock_success:
        toast.show_success("Great Success")
        mock_success.assert_called_once()
        kwargs = mock_success.call_args.kwargs
        assert kwargs.get('title') == 'Success'

    with patch('qfluentwidgets.InfoBar.warning') as mock_warning:
        toast.show_warning("Watch Out")
        mock_warning.assert_called_once()
        kwargs = mock_warning.call_args.kwargs
        assert kwargs.get('title') == 'Warning'
        
    with patch('qfluentwidgets.InfoBar.error') as mock_error:
        toast.show_error("Fail")
        mock_error.assert_called_once()
        kwargs = mock_error.call_args.kwargs
        assert kwargs.get('title') == 'Error'
