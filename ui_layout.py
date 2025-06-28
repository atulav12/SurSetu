from PyQt5.QtWidgets import (
    QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListWidget, QSlider
)
from PyQt5.QtCore import Qt, QTimer

from pulse import PulseBarWidget
from marquee import MarqueeLabel
from ui_controls import create_control_buttons, assemble_controls, connect_control_signals

queue = []
player = None

class MusicPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎧 SurSetu")
        self.resize(900, 520)

        self.queue = []
        self.history_stack = []
        self.current_track = None
        self.total_duration = 0
        self.search_results = []

        self.setup_ui()
        self.setup_connections()

        self.playback_timer = QTimer()
        self.playback_timer.setInterval(500)
        self.playback_timer.timeout.connect(self.monitor_playback)
        self.playback_timer.start()

    def setup_ui(self):
        main_layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)
        self.setLayout(main_layout)

        self.thumb_label = QLabel()
        self.thumb_label.setFixedSize(240, 135)
        self.thumb_label.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(self.thumb_label)

        self.search_box = QLineEdit()
        self.search_btn = QPushButton("🔍 Search")
        self.search_results_list = QListWidget()
        self.queue_list = QListWidget()
        self.add_btn = QPushButton("Add to Queue")

        self.now_playing = MarqueeLabel("Now Playing: None")
        self.time_label = QLabel("00:00 / 00:00")
        self.seek_slider = QSlider(Qt.Horizontal)
        self.seek_slider.setRange(0, 100)
        self.seek_slider.setEnabled(False)

        self.pulse_widget = PulseBarWidget()

        self.buttons = create_control_buttons()
        self.search_btn.clicked.connect(self.perform_search)
        controls_layout = assemble_controls(self.buttons)

        right_layout.addWidget(self.search_box)
        right_layout.addWidget(self.search_btn)
        right_layout.addWidget(QLabel("Search Results:"))
        right_layout.addWidget(self.search_results_list)
        right_layout.addWidget(self.add_btn)
        right_layout.addWidget(QLabel("Queue:"))
        right_layout.addWidget(self.queue_list)
        right_layout.addWidget(self.now_playing)
        right_layout.addWidget(self.time_label)
        right_layout.addWidget(self.seek_slider)
        right_layout.addWidget(self.pulse_widget)
        right_layout.addLayout(controls_layout)

    def perform_search(self):
        from yt_dlp import YoutubeDL

        query = self.search_box.text().strip()
        if not query:
            return

        self.search_results_list.clear()
        self.search_results = []

        ydl_opts = {
            'quiet': True,
            'extract_flat': 'in_playlist',
            'force_generic_extractor': True,
        }

        try:
            with YoutubeDL(ydl_opts) as ydl:
                search_results = ydl.extract_info(f"ytsearch10:{query}", download=False)['entries']

                for entry in search_results:
                    title = entry.get("title")
                    video_id = entry.get("id")
                    if title and video_id:
                        self.search_results.append((title, video_id))
                        self.search_results_list.addItem(f"{title}")
        except Exception as e:
            self.search_results_list.addItem(f"❌ Error: {e}")

    def setup_connections(self):
        self.add_btn.clicked.connect(self.add_selected_to_queue)
        connect_control_signals(self, self.buttons)

    def add_selected_to_queue(self):
        selected = self.search_results_list.currentRow()
        if selected >= 0:
            title, vid = self.search_results[selected]
            self.queue.append((title, vid))
            self.queue_list.addItem(title)

    def monitor_playback(self):
        pass  # Fill this in with seek slider and timer logic later
