from PySide6.QtWidgets import QListWidget, QListWidgetItem, QListView
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon, QPixmap
import logging

logger = logging.getLogger(__name__)

class GalleryView(QListWidget):
    item_clicked = Signal(str)

    def __init__(self):
        super().__init__()
        # 启用图标模式，这最适合展示相册
        self.setViewMode(QListView.IconMode)
        # 允许项在窗口大小改变时自动重新排列
        self.setResizeMode(QListView.Adjust)
        # 禁止用户手动拖动图标位置
        self.setMovement(QListView.Static)
        # 紧凑间距
        self.setSpacing(2)
        # 图标展示大小
        self.setIconSize(QSize(148, 148))
        # 每个格子的固定大小（确保正方形排布）
        self.setGridSize(QSize(150, 150))
        
        # 移除边框，启用像素级平滑滚动
        self.setFrameShape(QListWidget.NoFrame)
        self.setVerticalScrollMode(QListView.ScrollPerPixel)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        # 信号连接
        self.itemClicked.connect(self._on_item_clicked)
        
        # 样式表优化：移除硬编码颜色，跟随系统主题
        # 仅保留悬停和选中时的半透明高亮，增加“触控感”
        self.setStyleSheet("""
            QListWidget {
                outline: none;
                background: transparent;
            }
            QListWidget::item {
                border: 1px solid transparent;
            }
            QListWidget::item:hover {
                background-color: rgba(0, 120, 212, 0.15);
                border: 1px solid rgba(0, 120, 212, 0.3);
            }
            QListWidget::item:selected {
                background-color: rgba(0, 120, 212, 0.25);
                border: 1px solid #0078d4;
            }
        """)

    def add_item(self, file_path, thumb_bytes=None):
        """向画廊添加一个新的图片项。"""
        item = QListWidgetItem()
        # 将文件路径存入 UserRole，以便点击时提取
        item.setData(Qt.UserRole, file_path)
        
        if thumb_bytes:
            pixmap = QPixmap()
            if pixmap.loadFromData(thumb_bytes):
                # 将缩略图设置为项的图标
                item.setIcon(QIcon(pixmap))
            else:
                logger.warning(f"Failed to load pixmap for {file_path}")
        
        self.addItem(item)

    def _on_item_clicked(self, item):
        file_path = item.data(Qt.UserRole)
        self.item_clicked.emit(file_path)

    def clear(self):
        """清空画廊。"""
        super().clear()
