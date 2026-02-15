from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QFrame, QStyle, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QSize, Signal, QRect, QPropertyAnimation, QEasingCurve, QParallelAnimationGroup, QPoint, QMargins
from PySide6.QtGui import QPixmap, QColor, QPalette, QIcon, QMovie

class ImageViewer(QFrame):
    """A full-area overlay viewer for high-resolution images and animations."""
    closed = Signal()
    next_requested = Signal()
    prev_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("ImageViewerOverlay")
        self.setMouseTracking(True)
        self.setFocusPolicy(Qt.StrongFocus)
        
        # Opacity effect for fade animation (open/close)
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.fade_animation = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.fade_animation.setDuration(250)
        self.fade_animation.setEasingCurve(QEasingCurve.InOutQuad)
        
        # Slide animations
        self.slide_group = QParallelAnimationGroup()
        
        # UI Elements
        self.current_label = QLabel(self)
        self.current_label.setAlignment(Qt.AlignCenter)
        
        self.next_label = QLabel(self)
        self.next_label.setAlignment(Qt.AlignCenter)
        self.next_label.hide()
        
        self.current_movie = None
        self.next_movie = None
        
        button_style = """
            QPushButton {
                background-color: rgba(255, 255, 255, 50);
                border: none;
                border-radius: 20px;
                color: white;
            }
            QPushButton:hover {
                background-color: rgba(255, 255, 255, 100);
            }
        """
        
        self.btn_back = QPushButton(self)
        self.btn_back.setFixedSize(40, 40)
        self.btn_back.setIcon(self.style().standardIcon(QStyle.SP_ArrowBack))
        self.btn_back.setStyleSheet(button_style)
        self.btn_back.clicked.connect(self.close_viewer)
        
        self.btn_prev = QPushButton(self)
        self.btn_prev.setFixedSize(60, 100)
        self.btn_prev.setIcon(self.style().standardIcon(QStyle.SP_ArrowLeft))
        self.btn_prev.setIconSize(QSize(32, 32))
        self.btn_prev.setStyleSheet(button_style)
        self.btn_prev.clicked.connect(self.prev_requested.emit)
        
        self.btn_next = QPushButton(self)
        self.btn_next.setFixedSize(60, 100)
        self.btn_next.setIcon(self.style().standardIcon(QStyle.SP_ArrowRight))
        self.btn_next.setIconSize(QSize(32, 32))
        self.btn_next.setStyleSheet(button_style)
        self.btn_next.clicked.connect(self.next_requested.emit)
        
        self.setStyleSheet("""
            #ImageViewerOverlay {
                background-color: rgba(0, 0, 0, 230);
            }
        """)
        self.hide()

    def _get_scaled_movie_size(self, movie_size: QSize, target_rect_size: QSize) -> QSize:
        """Calculates scaled size maintaining aspect ratio."""
        if movie_size.isEmpty():
            return target_rect_size
        return movie_size.scaled(target_rect_size, Qt.KeepAspectRatio)

    def _set_media(self, label: QLabel, file_path: str) -> QMovie:
        """Sets either pixmap or movie to the label with aspect ratio preservation."""
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
        """Displays the specified image with a fade-in animation."""
        if self.fade_animation.state() == QPropertyAnimation.Running or \
           self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        if self.current_movie:
            self.current_movie.stop()
            
        self.current_movie = self._set_media(self.current_label, file_path)
        self.current_label.setGeometry(0, 0, self.width(), self.height())
        self.next_label.hide()
        
        if self.parent():
            self.resize(self.parent().size())
            
        self.show()
        self.raise_()
        self.setFocus()
        
        self.fade_animation.stop()
        self.fade_animation.setStartValue(0.0)
        self.fade_animation.setEndValue(1.0)
        self.fade_animation.start()

    def switch_image(self, file_path: str, direction: str = "next"):
        """Switches to another image using a horizontal slide animation."""
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        if self.next_movie:
            self.next_movie.stop()
            
        self.next_movie = self._set_media(self.next_label, file_path)
        self.next_label.setGeometry(self.rect())
        
        width = self.width()
        if direction == "next":
            start_pos = QPoint(width, 0)
            end_pos = QPoint(-width, 0)
        else:
            start_pos = QPoint(-width, 0)
            end_pos = QPoint(width, 0)
            
        self.next_label.move(start_pos)
        self.next_label.show()
        
        self.slide_group.clear()
        anim_current = QPropertyAnimation(self.current_label, b"pos")
        anim_current.setDuration(300)
        anim_current.setStartValue(QPoint(0, 0))
        anim_current.setEndValue(end_pos)
        anim_current.setEasingCurve(QEasingCurve.OutQuad)
        
        anim_next = QPropertyAnimation(self.next_label, b"pos")
        anim_next.setDuration(300)
        anim_next.setStartValue(start_pos)
        anim_next.setEndValue(QPoint(0, 0))
        anim_next.setEasingCurve(QEasingCurve.OutQuad)
        
        self.slide_group.addAnimation(anim_current)
        self.slide_group.addAnimation(anim_next)
        self.slide_group.finished.connect(self._on_slide_finished)
        self.slide_group.start()

    def _on_slide_finished(self):
        """Cleanup after slide animation completes."""
        try:
            self.slide_group.finished.disconnect(self._on_slide_finished)
        except RuntimeError:
            pass
            
        if self.current_movie:
            self.current_movie.stop()
            
        if self.next_movie:
            self.current_label.setMovie(self.next_movie)
            self.current_movie = self.next_movie
        else:
            self.current_label.setPixmap(self.next_label.pixmap())
            self.current_movie = None
            
        self.current_label.move(0, 0)
        self.next_label.hide()
        self.next_movie = None

    def close_viewer(self):
        """Closes the viewer with a fade-out animation."""
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        self.fade_animation.stop()
        self.fade_animation.setStartValue(self.opacity_effect.opacity())
        self.fade_animation.setEndValue(0.0)
        self.fade_animation.finished.connect(self._on_close_animation_finished)
        self.fade_animation.start()

    def _on_close_animation_finished(self):
        """Cleanup after close animation completes."""
        try:
            self.fade_animation.finished.disconnect(self._on_close_animation_finished)
        except RuntimeError:
            pass
        if self.current_movie:
            self.current_movie.stop()
        self.hide()
        self.closed.emit()

    def keyPressEvent(self, event):
        """Handles keyboard navigation inside the viewer."""
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        if event.key() == Qt.Key_Escape:
            self.close_viewer()
        elif event.key() == Qt.Key_Left:
            self.prev_requested.emit()
        elif event.key() == Qt.Key_Right:
            self.next_requested.emit()
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """Handles Mouse 4/5 navigation inside the viewer."""
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        if event.button() == Qt.XButton1: # Mouse 4 (Back)
            self.close_viewer()
        elif event.button() == Qt.XButton2: # Mouse 5 (Forward)
            self.next_requested.emit()
        super().mousePressEvent(event)

    def wheelEvent(self, event):
        """Handles mouse wheel navigation inside the viewer."""
        if self.slide_group.state() == QParallelAnimationGroup.Running:
            return
            
        delta = event.angleDelta().y()
        if delta > 0:
            self.prev_requested.emit()
        elif delta < 0:
            self.next_requested.emit()
        super().wheelEvent(event)

    def resizeEvent(self, event):
        """Rescales media on viewer resize."""
        super().resizeEvent(event)
        size = event.size()
        
        if self.slide_group.state() != QParallelAnimationGroup.Running:
            self.current_label.setGeometry(0, 0, size.width(), size.height())
            if self.current_movie:
                self.current_movie.jumpToFrame(self.current_movie.currentFrameNumber())
                orig_size = self.current_movie.currentPixmap().size()
                if not orig_size.isEmpty():
                    fit_size = self._get_scaled_movie_size(orig_size, size.shrunkBy(QMargins(10, 10, 10, 10)))
                    self.current_movie.setScaledSize(fit_size)
        
        margin = 20
        self.btn_back.move(margin, margin)
        btn_y = (size.height() - self.btn_prev.height()) // 2
        self.btn_prev.move(margin, btn_y)
        self.btn_next.move(size.width() - self.btn_next.width() - margin, btn_y)
