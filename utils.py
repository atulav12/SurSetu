import requests
from PyQt5.QtGui import QPixmap
from io import BytesIO

def set_thumbnail(label, url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        pixmap = QPixmap()
        pixmap.loadFromData(image_data.read())
        scaled = pixmap.scaled(label.size(), aspectRatioMode=1, transformMode=1)
        label.setPixmap(scaled)
    except Exception as e:
        print(f"[Thumbnail Error] {e}")
        label.clear()

def format_time(seconds):
    try:
        minutes = int(seconds) // 60
        remaining = int(seconds) % 60
        return f"{minutes:02}:{remaining:02}"
    except:
        return "00:00"
