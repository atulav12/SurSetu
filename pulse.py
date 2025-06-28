from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor
import random

class PulseBarWidget(QWidget):
    def __init__(self, num_bars=15, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.num_bars = num_bars
        self.bar_heights = [random.randint(10, 50) for _ in range(num_bars)]
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.setFixedHeight(60)

    def start(self):
        self.timer.start(100)

    def stop(self):
        self.timer.stop()
        self.bar_heights = [10] * self.num_bars
        self.update()

    def animate(self):
        self.bar_heights = [random.randint(10, 50) for _ in range(self.num_bars)]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        bar_width = self.width() // self.num_bars
        for i, height in enumerate(self.bar_heights):
            x = i * bar_width
            y = self.height() - height
            painter.setBrush(QColor("#1db954"))
            painter.setPen(Qt.NoPen)
            painter.drawRect(x + 2, y, bar_width - 4, height)
