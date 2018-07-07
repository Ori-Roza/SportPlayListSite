import os
import enum

__author__ = "Ori Roza"


class TEMPOS(enum.Enum):
    RHYTHMIC = "Rhythmic"
    NON_RHYTHMIC = "NotRhythmic"


DEBUG = False
MONGO_SERVER = ('127.0.0.1', 27017)
MP3_AUDIO_EXT = ".mp3"
WAV_AUDIO_EXT = ".wav"
SERVER_SONGS_SOURCE = os.path.join("static", "songs")
BASE_SONG_SOURCE = os.path.join(os.path.dirname(__file__), "static", "songs")
GOOD_DATASET_PATH = os.path.join(os.path.dirname(__file__), "knn", "good_dataset.pkl")
K_POINTS = 3
SAMPLES_QUANTITY = -200 # Last 200 samples from each WAV file
HIGH_BPM_TRESHOLD = 120  # BPM > 120 means rhythmic
ACCURACY_TRESHOLD = 95  # LEARNING ACCURACY
DATASET_SPLIT_RANGE_OPTIONS = range(3, 6)  # Split between training set and test set
