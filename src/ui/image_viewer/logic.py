from PySide6.QtWidgets import QFrame, QLabel, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QSize, Signal, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QMargins
from PySide6.QtGui import QPixmap, QMovie
from .layout import ImageViewerLayout
from .style import get_style

class ImageViewer(QFrame):
    """A full-area overlay viewer for high-resolution images and animations."""
    closed = Signal()
    next_requested = Signal()
    prev_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_engine = ImageViewerLayout()
        self.layout_engine.setup_ui(self)
        self.setStyleSheet(get_style())
        
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Opacity effect for fade animation
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(250)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        self.slide_group = QParallelAnimationGroup()
        self.current_movie = None
        self.next_movie = None
        
        # Connect signals
        self.layout_engine.btn_back.clicked.connect(self.close_viewer)
        self.layout_engine.btn_prev.clicked.connect(self.prev_requested.emit)
        self.layout_engine.btn_next.clicked.connect(self.next_requested.emit)
        
        self.hide()
        self._is_active = False

    def _get_scaled_movie_size(self, movie_size: QSize, target_rect_size: QSize) -> QSize:
        if movie_size.isEmpty(): return target_rect_size
        return movie_size.scaled(target_rect_size, Qt.KeepAspectRatio)

    def _set_media(self, label: QLabel, file_path: str) -> QMovie:
        label.clear()
        if file_path.lower().endswith(('.gif', '.webp')):
            movie = QMovie(file_path)
            if movie.isValid():
                label.setMovie(movie)
                movie.jumpToFrame(0)
                orig_size = movie.currentPixmap().size()
                target_size = self.size().shrunkBy(QMargins(10, 10, 10, 10))
                fit_size = self._get_scaled_movie_size(orig_size, target_size)
                movie.setScaledSize(fit_size)
                movie.start()
                return movie
        
        pixmap = QPixmap(file_path)
        if not pixmap.isNull():
            label.setPixmap(pixmap.scaled(
                self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
        else:
            label.setText("Failed to load image")
        return None

    def show_image(self, file_path: str):
        if self.fade_animation.state() == QPropertyAnimation.Running or \
           self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        if self.current_movie:
            self.current_movie.stop()
            
        self.current_movie = self._set_media(self.layout_engine.current_label, file_path)
        self.layout_engine.update_geometries(self)
        self.layout_engine.next_label.hide()
        
        if self.parent():
            self.resize(self.parent().size())
            
        self.show()
        self.raise_()
        self.setFocus()
        self._is_active = True
        
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def switch_image(self, file_path: str, direction: str = "next"):
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        if self.next_movie:
            self.next_movie.stop()
            
        self.next_movie = self._set_media(self.layout_engine.next_label, file_path)
        self.layout_engine.next_label.setGeometry(self.rect())
        
        width = self.width()
        start_pos = QPoint(width if direction == "next" else -width, 0)
        end_pos = QPoint(-width if direction == "next" else width, 0)
            
        self.layout_engine.next_label.move(start_pos)
        self.layout_engine.next_label.show()
        
        self.slide_group.clear()
        anim_current = QPropertyAnimation(self.layout_engine.current_label, b"pos")
        anim_current.setDuration(300)
        anim_current.setStartValue(QPoint(0, 0))
        anim_current.setEndValue(end_pos)
        anim_current.setEasingCurve(QEasingCurve.OutQuad)
        
        anim_next = QPropertyAnimation(self.layout_engine.next_label, b"pos")
        anim_next.setDuration(300)
        anim_next.setStartValue(start_pos)
        anim_next.setEndValue(QPoint(0, 0))
        anim_next.setEasingCurve(QEasingCurve.OutQuad)
        
        self.slide_group.addAnimation(anim_current)
        self.slide_group.addAnimation(anim_next)
        self.slide_group.finished.connect(self._on_slide_finished)
        self.slide_group.start()

    def _on_slide_finished(self):
        try: self.slide_group.finished.disconnect(self._on_slide_finished)
        except RuntimeError: pass
            
        if self.current_movie: self.current_movie.stop()
            
        if self.next_movie:
            self.layout_engine.current_label.setMovie(self.next_movie)
            self.current_movie = self.next_movie
        else:
            self.layout_engine.current_label.setPixmap(self.layout_engine.next_label.pixmap())
            self.current_movie = None
            
        self.layout_engine.current_label.move(0, 0)
        self.layout_engine.next_label.hide()
        self.next_movie = None

    def close_viewer(self):
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        self.fade_animation.stop()
        self.fade_animation.setStartValue(self.opacity_effect.opacity())
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self._on_close_animation_finished)
        self.fade_animation.start()

    def _on_close_animation_finished(self):
        try: self.fade_animation.finished.disconnect(self._on_close_animation_finished)
        except RuntimeError: pass
        if self.current_movie: self.current_movie.stop()
        self.hide()
        self._is_active = False
        self.closed.emit()

    def keyPressEvent(self, event):
        if self.slide_group.state() == QParallelAnimationGroup.Running: return
        if event.key() == Qt.Key_Escape: self.close_viewer()
        elif event.key() == Qt.Key_Left: self.prev_requested.emit()
        elif event.key() == Qt.Key_Right: self.next_requested.emit()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        if self.slide_group.state() == QParallelAnimationGroup.Running: return
        if event.button() == Qt.XButton1: self.close_viewer()
        elif event.button() == Qt.XButton2: self.next_requested.emit()
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        if self.slide_group.state() == QParallelAnimationGroup.Running: return
        delta = event.angleDelta().y()
        if delta > 0: self.prev_requested.emit()
        elif delta < 0: self.next_requested.emit()
        super().wheelEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.layout_engine.update_geometries(self)
        if self.current_movie and self.slide_group.state() != QParallelAnimationGroup.Running:
             self.current_movie.jumpToFrame(self.current_movie.currentFrameNumber())
             orig_size = self.current_movie.currentPixmap().size()
             if not orig_size.isEmpty():
                 fit_size = self._get_scaled_movie_size(orig_size, self.size().shrunkBy(QMargins(10, 10, 10, 10)))
                 self.current_movie.setScaledSize(fit_size)
