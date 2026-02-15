from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QSize, QRect, QPoint
from PySide6.QtGui import QColor, QPen
from src.ui.theme import Theme

class GalleryItemDelegate(QStyledItemDelegate):
    """Custom delegate for rendering gallery items with overlaid checkboxes."""
    
    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        painter.save()
        
        # Draw background/selection border if selected or hovered
        accent = Theme.get_qcolor(Theme.ACCENT_PRIMARY)
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, Theme.get_qcolor(Theme.ACCENT_PRIMARY, 60))
            pen = QPen(accent, 2)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, Theme.get_qcolor(Theme.ACCENT_PRIMARY, 30))
            pen = QPen(Theme.get_qcolor(Theme.ACCENT_PRIMARY, 100), 1)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))

        # Draw Icon (Image)
        icon = index.data(Qt.DecorationRole)
        if icon:
            icon_rect = option.rect.adjusted(4, 4, -4, -4)
            icon.paint(painter, icon_rect, Qt.AlignCenter)

        # Draw Checkbox if in selection mode
        view = self.parent()
        if hasattr(view, "selection_mode_enabled") and view.selection_mode_enabled:
            is_checked = option.state & QStyle.State_Selected
            
            cb_size = 22
            cb_rect = QRect(option.rect.left() + 8, option.rect.top() + 8, cb_size, cb_size)
            
            painter.setPen(QPen(Theme.get_qcolor("#000000", 60), 1))
            if is_checked:
                painter.setBrush(accent)
            else:
                painter.setBrush(Theme.get_qcolor("#ffffff", 220))
            
            painter.drawRoundedRect(cb_rect, 4, 4)
            
            if is_checked:
                painter.setPen(QPen(Qt.white, 2))
                p1 = QPoint(cb_rect.left() + 5, cb_rect.top() + 11)
                p2 = QPoint(cb_rect.left() + 9, cb_rect.top() + 15)
                p3 = QPoint(cb_rect.left() + 17, cb_rect.top() + 7)
                painter.drawLine(p1, p2)
                painter.drawLine(p2, p3)
        
        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        return QSize(150, 150)

def get_gallery_style():
    return f"""
        QScrollArea {{ background: transparent; border: none; }}
        GroupedListWidget {{ background: transparent; outline: none; }}
        QLabel#GroupHeader {{ 
            color: {Theme.TEXT_PRIMARY}; 
            padding-bottom: 5px; 
            border-bottom: 1px solid {Theme.BORDER_SUBTLE};
            font-weight: bold;
            font-size: 14px;
        }}
    """
