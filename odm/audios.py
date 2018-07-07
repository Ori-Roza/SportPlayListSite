from conf import *
from pymongo import MongoClient
from knn import classifier
from bpm_extractor import BMPExtractor

__author__ = "Ori Roza"


class Audios(object):
    def __init__(self):
        self._client = MongoClient(*MONGO_SERVER)
        self.audios_db = self._client['audios_db']

    def _predict_rhythmic(self, bpm_avg, bpm_counter, are_bigger_high_points, high_bpm_sequence):
        new_audio_set = [bpm_avg, bpm_counter, are_bigger_high_points, high_bpm_sequence]
        if os.path.exists(GOOD_DATASET_PATH):
            with open(GOOD_DATASET_PATH, "rb") as f:
                is_rhythmic = classifier.run(self.audios_db, prepared_dataset=f, new_song=new_audio_set)
            return 1 if TEMPOS.RHYTHMIC == is_rhythmic else 0
        else:
            raise ValueError("%s not found" % GOOD_DATASET_PATH)

    @staticmethod
    def _manual_insert():
        is_rhythmic = int(raw_input("Is rhythmic? "))
        if is_rhythmic == -1:  # If BPM does not seem right, correct it (if it's too high)
            # Magic numbers
            bpm_avg = 120
            are_bigger_high_points = 0
            bpm_counter = 49
            is_rhythmic = 0
            high_bpm_sequence = 5
        elif is_rhythmic == 100:  # If BPM does not seem right, correct it (if it's too low)
            # Magic number
            bpm_avg = 121
            are_bigger_high_points = 1
            bpm_counter = 51
            is_rhythmic = 1
            high_bpm_sequence = 100
        else:
            raise ValueError("Invalid option")
        return bpm_avg, are_bigger_high_points, bpm_counter, is_rhythmic, high_bpm_sequence

    def insert_new_audio(self, new_audio, train=False):
        try:
            audio_name = os.path.basename(new_audio)
            audio_path_in_server = os.path.join(SERVER_SONGS_SOURCE, audio_name)
            if not self.does_song_exist(audio_path_in_server):
                bpm_ex = BMPExtractor(new_audio)
                samples = bpm_ex.get_bpm_samples().tolist()
                bpm_counter, bpm_avg, are_bigger_high_points, high_bpm_sequence = bpm_ex.get_song_stats(samples)
                if train:
                    # Add and analyze audios manually
                    print "BPM AVG: %d, HIGH BPM PERCENTAGE: %d ARE BIGGER HIGH?: %d SEQ: %d\n" \
                          % (bpm_avg, bpm_counter, are_bigger_high_points, high_bpm_sequence)
                    bpm_avg, are_bigger_high_points, bpm_counter, is_rhythmic, high_bpm_sequence = self._manual_insert()

                else:
                    # Use the magic
                    is_rhythmic = self._predict_rhythmic(bpm_avg, bpm_counter, are_bigger_high_points, high_bpm_sequence)

                self.audios_db["files"].insert_one({
                    "audio_name": audio_name,
                    "audio_path": audio_path_in_server,
                    "to_sport_list": is_rhythmic,
                    "bpm_avg": int(bpm_avg),
                    "bpm_counter": bpm_counter,
                    "are_bigger_high_points": are_bigger_high_points,
                    "high_bpm_sequence": high_bpm_sequence,
                })
                return True
            else:
                print "%s already exists" % new_audio
                return False
        except Exception, e:
            raise

    def does_song_exist(self, new_audio):
        audio_name = os.path.basename(new_audio)
        return 1 if self.audios_db.files.find({"audio_name": audio_name, "audio_path": new_audio}).count() > 0 else 0

    def get_rhythmic_songs(self):
        return list(self.audios_db["files"].find({"to_sport_list": 1}))