from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QLabel
from PySide6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QFont
class BubbleToast(QWidget):
    def __init__(self, message, parent=None, duration=2500):
        super().__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.ToolTip | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel(message, self)
        self.label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: white;
            padding: 12px 24px;
            border-radius: 12px;
            font-size: 14px;
        """)
        self.label.setFont(QFont("Segoe UI", 10))
        self.label.adjustSize()
        self.resize(self.label.size())

        # 位置后面设置

        # 计时自动关闭
        QTimer.singleShot(duration, self.fade_out)

    def fade_out(self):
        self.anim = QPropertyAnimation(self, b"windowOpacity")
        self.anim.setDuration(1000)
        self.anim.setStartValue(1.0)
        self.anim.setEndValue(0.0)
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)
        self.anim.finished.connect(self.close)
        self.anim.start()

    def show_center(self, parent=None):
        if parent:
            geo = parent.geometry()
        else:
            from PySide6.QtGui import QGuiApplication
            geo = QGuiApplication.primaryScreen().geometry()
        center = geo.center()
        self.move(center.x() - self.width() // 2, center.y() - self.height() // 2)
        self.show()
        self.raise_()
        self.activateWindow()


def show_message(parent, title, message, icon=QMessageBox.Information):
    msg_box = QMessageBox(parent)
    msg_box.setWindowTitle(title)
    msg_box.setText(message)
    msg_box.setIcon(icon)
    msg_box.setStandardButtons(QMessageBox.Ok)

    # 清爽现代风格样式表
    msg_box.setStyleSheet("""
        QMessageBox {
            background-color: #ffffff;
            border-radius: 12px;
            padding: 20px;
        }

        QLabel {
            color: #202124;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
            font-size: 15px;
            padding: 10px 5px;
        }

        QPushButton {
            background-color: #e0e0e0;
            color: #202124;
            border: none;
            padding: 8px 16px;
            border-radius: 8px;
            min-width: 80px;
            font-size: 14px;
        }

        QPushButton:hover {
            background-color: #d5d5d5;
        }

        QPushButton:pressed {
            background-color: #c0c0c0;
        }
    """)

    msg_box.exec()

