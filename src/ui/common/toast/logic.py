from PySide6.QtCore import QObject, Qt
from PySide6.QtWidgets import QWidget
from qfluentwidgets import InfoBar, InfoBarPosition

class Toast(QObject):
    """
    Wrapper around qfluentwidgets.InfoBar for compatibility with existing code.
    """
    def __init__(self, text="", duration=2000, parent=None):
        super().__init__(parent)
        self.default_text = text
        self.duration = duration
        self.parent_widget = parent

    def show_message(self, text=None, reference_widget=None):
        """Shows an info message."""
        content = text if text else self.default_text
        parent = reference_widget if isinstance(reference_widget, QWidget) else self.parent_widget
        
        if not parent:
            return

        InfoBar.info(
            title='Info',
            content=content,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=self.duration,
            parent=parent
        )

    def show_success(self, text, title='Success', reference_widget=None):
        parent = reference_widget if isinstance(reference_widget, QWidget) else self.parent_widget
        if not parent: return
        
        InfoBar.success(
            title=title,
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=self.duration,
            parent=parent
        )

    def show_warning(self, text, title='Warning', reference_widget=None):
        parent = reference_widget if isinstance(reference_widget, QWidget) else self.parent_widget
        if not parent: return

        InfoBar.warning(
            title=title,
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=self.duration,
            parent=parent
        )

    def show_error(self, text, title='Error', reference_widget=None):
        parent = reference_widget if isinstance(reference_widget, QWidget) else self.parent_widget
        if not parent: return

        InfoBar.error(
            title=title,
            content=text,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=self.duration,
            parent=parent
        )
