from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPainter, QFontMetrics


class MarqueeLabel(QLabel):
    def __init__(self, text='', parent=None):
        super().__init__(text, parent)
        self.offset = 0
        self.speed = 2  # Pixels per tick
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.scrollText)
        self.setMinimumHeight(24)
        self.setStyleSheet("font-weight: bold; font-size: 14px;")

    def start(self):
        metrics = QFontMetrics(self.font())
        if metrics.width(self.text()) > self.width():
            self.timer.start(50)

    def stop(self):
        self.timer.stop()
        self.offset = 0
        self.update()

    def scrollText(self):
        self.offset += self.speed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(self.palette().windowText().color())
        metrics = QFontMetrics(self.font())
        text_width = metrics.width(self.text())

        if text_width > self.width():
            x = -self.offset % (text_width + 20)
            y = self.height() - 5
            painter.drawText(x, y, self.text())
            painter.drawText(x + text_width + 20, y, self.text())
        else:
            painter.drawText(0, self.height() - 5, self.text())
