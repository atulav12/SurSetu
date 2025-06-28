import vlc
from yt_dlp import YoutubeDL
from utils import set_thumbnail

player = None

def get_stream_url(youtube_url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'noplaylist': True
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        for f in info['formats']:
            if f.get('acodec') != 'none' and f.get('vcodec') == 'none':
                return f['url']
    return None

def play_next(ui):
    global queue, player

    if player:
        player.stop()

    if hasattr(ui, "current_track") and ui.current_track:
        ui.history_stack.append(ui.current_track)

    if not ui.queue:
        ui.now_playing.setText("Queue empty.")
        ui.thumb_label.clear()
        ui.seek_slider.setEnabled(False)
        ui.pulse_widget.stop()
        return

    title, vid = ui.queue.pop(0)
    ui.queue_list.takeItem(0)
    ui.current_track = (title, vid)

    if "–" in title:
        song_title, artist = [s.strip() for s in title.split("–", 1)]
    else:
        song_title, artist = title, "Unknown Artist"

    ui.now_playing.setText(f"{song_title}\n{artist}")
    ui.now_playing.start()

    thumbnail = f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    set_thumbnail(ui.thumb_label, thumbnail)

    try:
        stream_url = get_stream_url(f"https://www.youtube.com/watch?v={vid}")
        player = vlc.MediaPlayer(stream_url)
        player.play()
        ui.seek_slider.setEnabled(True)
        ui.pulse_widget.start()
    except Exception as e:
        ui.now_playing.setText(f"❌ Error: {e}")
        ui.pulse_widget.stop()

def skip_back(ui):
    global queue, player

    if player:
        current = player.get_time()
        if current > 5000:
            player.set_time(0)
        elif ui.history_stack:
            prev_title, prev_vid = ui.history_stack.pop()
            ui.queue.insert(0, ui.current_track)
            ui.queue_list.insertItem(0, ui.current_track[0])
            ui.current_track = (prev_title, prev_vid)
            ui.queue.insert(0, (prev_title, prev_vid))
            ui.now_playing.setText(f"🔙 Rewinding to: {prev_title}")
            play_next(ui)

def pause_song(pulse_widget):
    global player
    if player:
        player.pause()
        pulse_widget.stop()

def resume_song(pulse_widget):
    global player
    if player:
        player.play()
        pulse_widget.start()

def skip_song(ui):
    play_next(ui)
