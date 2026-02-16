from qfluentwidgets import ListItemDelegate
from PySide6.QtWidgets import QStyle
from PySide6.QtCore import Qt, QSize, QRect, QPoint
from PySide6.QtGui import QColor, QPen, QPalette, QBrush, QPainter
from src.ui.theme import Theme

class GalleryItemDelegate(ListItemDelegate):
    """Custom delegate that provides Fluent-style selection and checkboxes."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.selectedRows = []

    def setSelectedRows(self, indexes):
        """Called by Fluent ListWidget to track selected rows."""
        self.selectedRows = [i.row() for i in indexes]

    def paint(self, painter: QPainter, option, index):
        # We don't call super().paint because we have a custom IconMode layout
        # But we use the state from option
        painter.save()
        painter.setRenderHint(QPainter.Antialiasing)
        
        palette = option.palette
        highlight = palette.color(QPalette.Highlight)
        
        # Draw background/selection border if selected or hovered
        rect = option.rect.adjusted(2, 2, -2, -2)
        radius = 8
        
        if option.state & QStyle.State_Selected:
            # Selection background
            bg_color = QColor(highlight)
            bg_color.setAlpha(40)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, radius, radius)
            
            # Selection indicator border
            pen = QPen(highlight, 2)
            painter.setPen(pen)
            painter.setBrush(Qt.NoBrush)
            painter.drawRoundedRect(rect, radius, radius)
            
        elif option.state & QStyle.State_MouseOver:
            bg_color = QColor(highlight)
            bg_color.setAlpha(20)
            painter.setBrush(QBrush(bg_color))
            painter.setPen(Qt.NoPen)
            painter.drawRoundedRect(rect, radius, radius)

        # Draw Icon
        icon = index.data(Qt.DecorationRole)
        if icon:
            # Scale down slightly to show selection border
            icon_rect = option.rect.adjusted(10, 10, -10, -10)
            icon.paint(painter, icon_rect, Qt.AlignCenter)

        # Draw Checkbox in Selection Mode
        view = self.parent()
        if hasattr(view, "selection_mode_enabled") and view.selection_mode_enabled:
            is_selected = option.state & QStyle.State_Selected
            cb_size = 20
            cb_rect = QRect(option.rect.left() + 10, option.rect.top() + 10, cb_size, cb_size)
            
            # Checkbox border
            painter.setPen(QPen(QColor(128, 128, 128, 150), 1))
            if is_selected:
                painter.setBrush(highlight)
            else:
                painter.setBrush(QColor(255, 255, 255, 200) if not Theme.is_dark_mode() else QColor(40, 40, 40, 200))
            
            painter.drawRoundedRect(cb_rect, 4, 4)
            
            if is_selected:
                painter.setPen(QPen(Qt.white, 2))
                # Simple check mark
                p1 = QPoint(cb_rect.left() + 5, cb_rect.top() + 10)
                p2 = QPoint(cb_rect.left() + 9, cb_rect.top() + 14)
                p3 = QPoint(cb_rect.left() + 15, cb_rect.top() + 6)
                painter.drawLine(p1, p2)
                painter.drawLine(p2, p3)
        
        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        return QSize(160, 160)

def get_gallery_style():
    return f"""
        QScrollArea {{ background: transparent; border: none; }}
        QLabel#GroupHeader {{ 
            padding-bottom: 5px; 
            border-bottom: 1px solid rgba(128, 128, 128, 60);
            font-weight: bold;
            font-size: 14px;
        }}
    """
