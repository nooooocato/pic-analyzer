from PySide6.QtWidgets import QFrame, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QTimer, QPoint
from .style import get_style
from .layout import ToastLayout

class Toast(QFrame):
    def __init__(self, text, duration=2000, parent=None):
        super().__init__(parent)
        self.layout_engine = ToastLayout()
        self.layout_engine.setup_ui(self)
        self.layout_engine.label.setText(text)
        self.setStyleSheet(get_style())
        
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        
        self.opacity_effect = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self.opacity_effect)
        
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setDuration(300)
        self.anim.setEasingCurve(QEasingCurve.OutQuad)
        
        self.timer = QTimer(self)
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.hide_toast)
        
        self.duration = duration
        self.hide()

    def show_message(self, text=None, reference_widget=None):
        if text:
            self.layout_engine.label.setText(text)
        
        # Determine target for positioning
        target = reference_widget or self.parent()
        
        if target:
            self.adjustSize()
            # Calculate global center of target
            target_rect = target.rect()
            global_center = target.mapToGlobal(target_rect.center())
            
            # Convert back to parent coordinates
            if self.parent():
                local_center = self.parent().mapFromGlobal(global_center)
                x = local_center.x() - self.width() // 2
                # Position near bottom of the target
                y = local_center.y() + (target_rect.height() // 2) - self.height() - 50
                self.move(x, y)
        
        self.show()
        self.raise_()
        self.anim.stop()
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()
        self.timer.start(self.duration)

    def hide_toast(self):
        self.anim.stop()
        self.anim.setStartValue(self.opacity_effect.opacity())
        self.anim.setEndValue(0.0)
        self.anim.finished.connect(self.hide)
        self.anim.start()
