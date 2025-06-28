from PyQt5.QtWidgets import QApplication
from ui_layout import MusicPlayer
import sys

app = QApplication(sys.argv)
window = MusicPlayer()
window.show()
with open("resources/style.qss", "r") as file:
    app.setStyleSheet(file.read())
sys.exit(app.exec_())
