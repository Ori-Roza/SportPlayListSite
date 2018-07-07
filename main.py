import os
import random
from odm.audios import Audios
from gevent.pywsgi import WSGIServer
from flask import Flask, render_template

__author__ = "Ori Roza"

app = Flask(__name__)


def get_single_song(song):
    if os.path.exists(song["audio_path"]):
        return {song["audio_name"]: song["audio_path"]}
    return {}


def random_songs(songs, limit=-1):
    if limit > -1:
        return random.sample(songs, limit)
    random.shuffle(songs)
    return songs


@app.route('/')
def main():
    db = Audios()
    songs = db.get_rhythmic_songs()
    random_song = random_songs(songs, limit=10)
    songs_dict = {}
    for song in random_song:
        songs_dict.update(get_single_song(song))
    return render_template("index.html", songs_pathes=songs_dict)


if __name__ == '__main__':
    # Production Server for high performance and requests handling
    http_server = WSGIServer(('0.0.0.0', 5000), app)
    http_server.serve_forever()
