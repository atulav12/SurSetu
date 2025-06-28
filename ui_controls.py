from PyQt5.QtWidgets import QPushButton, QHBoxLayout
import player

def create_control_buttons():
    prev_btn = QPushButton("⏮")
    play_btn = QPushButton("▶")
    pause_btn = QPushButton("⏸")
    next_btn = QPushButton("⏭")

    for btn in [prev_btn, play_btn, pause_btn, next_btn]:
        btn.setFixedSize(45, 45)
        btn.setStyleSheet("font-size: 20px;")

    return {
        "prev": prev_btn,
        "play": play_btn,
        "pause": pause_btn,
        "next": next_btn
    }

def assemble_controls(btns):
    layout = QHBoxLayout()
    for key in ["prev", "play", "pause", "next"]:
        layout.addWidget(btns[key])
    return layout

def connect_control_signals(ui, btns):
    btns["play"].clicked.connect(lambda: player.play_next(ui))
    btns["pause"].clicked.connect(lambda: player.pause_song(ui.pulse_widget))
    btns["next"].clicked.connect(lambda: player.play_next(ui))
    btns["prev"].clicked.connect(lambda: player.skip_back(ui))
