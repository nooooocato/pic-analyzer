from PySide6.QtWidgets import QListWidget, QListWidgetItem, QListView, QMenu, QStyledItemDelegate, QStyle, QApplication
from PySide6.QtCore import Qt, QSize, Signal, QTimer, QRect, QPoint, QMargins
from PySide6.QtGui import QAction, QIcon, QPixmap, QCursor, QColor, QPen
import logging

logger = logging.getLogger(__name__)

class GalleryItemDelegate(QStyledItemDelegate):
    """Custom delegate for rendering gallery items with overlaid checkboxes."""
    def __init__(self, parent=None):
        super().__init__(parent)

    def paint(self, painter, option, index):
        """Paints the item icon and selection checkbox."""
        self.initStyleOption(option, index)
        painter.save()
        
        # Draw background/selection border if selected or hovered
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor(0, 120, 212, 60))
            pen = QPen(QColor(0, 120, 212), 2)
            painter.setPen(pen)
            painter.drawRect(option.rect.adjusted(1, 1, -1, -1))
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QColor(0, 120, 212, 30))
            pen = QPen(QColor(0, 120, 212, 100), 1)
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
            
            # Position checkbox at top-left with some margin
            cb_size = 20
            cb_rect = QRect(option.rect.left() + 5, option.rect.top() + 5, cb_size, cb_size)
            
            # Background for checkbox
            if is_checked:
                painter.setBrush(QColor(0, 120, 212))
                painter.setPen(QColor(0, 120, 212))
            else:
                painter.setBrush(QColor(255, 255, 255, 200))
                painter.setPen(QColor(100, 100, 100))
            
            painter.drawRoundedRect(cb_rect, 2, 2)
        
        painter.restore()

    def sizeHint(self, option, index) -> QSize:
        """Returns the fixed size for each gallery item."""
        return QSize(150, 150)

class GalleryView(QListWidget):
    """A grid-based view for displaying image thumbnails with selection support."""
    item_selected = Signal(str)
    item_activated = Signal(str)
    selection_mode_changed = Signal(bool)

    def __init__(self):
        super().__init__()
        self._selection_mode_enabled = False
        self._pressed_item = None
        self._pressed_pos = QPoint()
        self._long_press_active = False
        
        # Use custom delegate
        self.setItemDelegate(GalleryItemDelegate(self))
        
        # Long press timer
        self._long_press_timer = QTimer()
        self._long_press_timer.setSingleShot(True)
        self._long_press_timer.setInterval(800) # 800ms for long press
        self._long_press_timer.timeout.connect(self._on_long_press)
        
        # Context menu
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self._show_context_menu)
        
        # Synchronize selection and check state
        self.itemSelectionChanged.connect(self._sync_selection_and_checkstate)
        
        # Enable Icon Mode
        self.setViewMode(QListView.IconMode)
        self.setResizeMode(QListView.Adjust)
        self.setMovement(QListView.Static)
        self.setSpacing(2)
        self.setIconSize(QSize(148, 148))
        self.setGridSize(QSize(150, 150))
        
        self.setFrameShape(QListWidget.NoFrame)
        self.setVerticalScrollMode(QListView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # Signal connections
        self.itemDoubleClicked.connect(self._on_item_double_clicked)
        self.currentItemChanged.connect(self._on_current_item_changed)
        
        # Enable ExtendedSelection by default for RubberBand
        self.setSelectionMode(QListWidget.ExtendedSelection)
        self.setDragEnabled(False)
        
        self.setStyleSheet("QListWidget { outline: none; background: transparent; }")

    def _on_item_double_clicked(self, item: QListWidgetItem):
        """Internal handler for double click activation."""
        if not self._selection_mode_enabled:
            file_path = item.data(Qt.UserRole)
            self.item_activated.emit(file_path)

    def _sync_selection_and_checkstate(self):
        """Synchronizes checkbox check state with item selection state."""
        selected_items = self.selectedItems()
        # Auto-enable selection mode if multiple items selected via rubber-band
        if not self._selection_mode_enabled and len(selected_items) > 1:
            self.set_selection_mode_enabled(True)
            return

        if not self._selection_mode_enabled:
            return
            
        # Temporarily block signals to avoid recursion
        self.blockSignals(True)
        for i in range(self.count()):
            item = self.item(i)
            is_sel = item.isSelected()
            expected_check = Qt.Checked if is_sel else Qt.Unchecked
            if item.checkState() != expected_check:
                item.setCheckState(expected_check)
        self.blockSignals(False)
        self.viewport().update()

    @property
    def selection_mode_enabled(self) -> bool:
        """Returns whether multi-selection mode is currently active."""
        return self._selection_mode_enabled

    def set_selection_mode_enabled(self, enabled: bool):
        """Toggles the multi-selection mode and updates UI state."""
        if self._selection_mode_enabled == enabled:
            return
        self._selection_mode_enabled = enabled
        
        self.blockSignals(True)
        self.setSelectionMode(QListWidget.MultiSelection if enabled else QListWidget.ExtendedSelection)
        if not enabled:
            # Clear all selections and checkboxes when exiting mode
            for i in range(self.count()):
                item = self.item(i)
                item.setCheckState(Qt.Unchecked)
                item.setSelected(False)
                item.setFlags(item.flags() & ~Qt.ItemIsUserCheckable)
        else:
            # Make items checkable when entering mode
            for i in range(self.count()):
                item = self.item(i)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        self.blockSignals(False)
        
        self.selection_mode_changed.emit(enabled)
        self.viewport().update()

    def add_item(self, file_path: str, thumb_bytes: bytes = None):
        """Adds a new image item to the gallery."""
        item = QListWidgetItem()
        item.setData(Qt.UserRole, file_path)
        if self._selection_mode_enabled:
            item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
            item.setCheckState(Qt.Unchecked)
        if thumb_bytes:
            pixmap = QPixmap()
            if pixmap.loadFromData(thumb_bytes):
                item.setIcon(QIcon(pixmap))
        self.addItem(item)

    def _on_item_clicked(self, item: QListWidgetItem):
        """Legacy handler for item clicks."""
        pass

    def _on_current_item_changed(self, current: QListWidgetItem, previous: QListWidgetItem):
        """Emits selection signal when the highlighted item changes."""
        if current:
            file_path = current.data(Qt.UserRole)
            self.item_selected.emit(file_path)

    def mousePressEvent(self, event):
        """Handles mouse press for long-press detection and navigation."""
        if event.button() == Qt.LeftButton:
            self._pressed_pos = event.pos()
            self._pressed_item = self.itemAt(event.pos())
            if self._pressed_item:
                self._long_press_timer.start()
        elif event.button() == Qt.XButton2: # Mouse 5 (Forward)
            item = self.itemAt(event.pos())
            if item and not self._selection_mode_enabled:
                self.item_activated.emit(item.data(Qt.UserRole))
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Cancels long-press if mouse moves significantly or handles additive drag selection."""
        if self._long_press_timer.isActive():
            if (event.pos() - self._pressed_pos).manhattanLength() > QApplication.startDragDistance():
                self._long_press_timer.stop()
        
        if self._long_press_active:
            item = self.itemAt(event.pos())
            if item:
                item.setSelected(True)
            if self._pressed_item:
                self._pressed_item.setSelected(True)
            return

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Cleans up long-press state on mouse release."""
        self._long_press_timer.stop()
        self._pressed_item = None
        self._long_press_active = False
        super().mouseReleaseEvent(event)

    def _on_long_press(self):
        """Activates selection mode on long press."""
        if not self._selection_mode_enabled:
            self._long_press_active = True
            self.set_selection_mode_enabled(True)
            if self._pressed_item:
                self._pressed_item.setSelected(True)

    def _show_context_menu(self, pos: QPoint):
        """Displays custom context menu for gallery items."""
        item = self.itemAt(pos)
        menu = QMenu(self)
        if not self._selection_mode_enabled:
            select_action = menu.addAction("Select")
            select_action.triggered.connect(lambda: self.set_selection_mode_enabled(True))
        if item:
            open_action = menu.addAction("Open")
            open_action.triggered.connect(lambda: self.item_activated.emit(item.data(Qt.UserRole)))
        if not menu.isEmpty():
            menu.exec(self.mapToGlobal(pos))

    def clear(self):
        """Clears all items from the gallery."""
        super().clear()
