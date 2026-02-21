from PySide6.QtWidgets import QStyledItemDelegate, QStyle
from PySide6.QtCore import Qt, QSize, QRect, QPoint
from PySide6.QtGui import QColor, QPen, QPalette
from src.ui.theme import Theme

class GalleryItemDelegate(QStyledItemDelegate):
    """Custom delegate that respects system palette."""
    
    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        painter.save()
        
        palette = option.palette
        highlight = palette.color(QPalette.Highlight)
        
        # Draw background/selection border if selected or hovered
        if option.state & QStyle.State_Selected:
            bg_color = QColor(highlight)
            bg_color.setAlpha(60)
            painter.fillRect(option.rect, bg_color)
            
            pen = QPen(highlight, 2)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
        elif option.state & QStyle.State_MouseOver:
            bg_color = QColor(highlight)
            bg_color.setAlpha(30)
            painter.fillRect(option.rect, bg_color)

        # Draw Icon
        icon = index.data(Qt.DecorationRole)
        if icon:
            icon_rect = option.rect.adjusted(4, 4, -4, -4)
            icon.paint(painter, icon_rect, Qt.AlignCenter)

        # Draw Checkbox
        view = self.parent()
        if hasattr(view, "selection_mode_enabled") and view.selection_mode_enabled:
            is_checked = option.state & QStyle.State_Selected
            cb_size = 22
            cb_rect = QRect(option.rect.left() + 8, option.rect.top() + 8, cb_size, cb_size)
            
            painter.setPen(QPen(palette.color(QPalette.Shadow), 1))
            if is_checked:
                painter.setBrush(highlight)
            else:
                painter.setBrush(palette.color(QPalette.Base))
            
            painter.drawRoundedRect(cb_rect, 4, 4)
            
            if is_checked:
                painter.setPen(QPen(palette.color(QPalette.HighlightedText), 2))
                p1 = QPoint(cb_rect.left() + 5, cb_rect.top() + 11)
                p2 = QPoint(cb_rect.left() + 9, cb_rect.top() + 15)
                p3 = QPoint(cb_rect.left() + 17, cb_rect.top() + 7)
                painter.drawLine(p1, p2)
                painter.drawLine(p2, p3)
        
        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        return QSize(150, 150)

def get_gallery_style():
    # Rely more on system colors for text
    return f"""
        QScrollArea {{ background: transparent; border: none; }}
        GroupedListWidget {{ background: transparent; outline: none; }}
        QLabel#GroupHeader {
            font-weight: bold;
            font-size: 11px;
            color: #ccc;
            padding: 0 8px;
            background-color: #222;
            border-bottom: 1px solid #333;
            max-height: 22px;
            min-height: 22px;
        }
    """
