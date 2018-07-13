import random
from conf import DATASET_SPLIT_RANGE_OPTIONS, TEMPOS

__author__ = "Ori Roza"


def create_dataset(audio_db):
    parsed = []
    audios = audio_db["files"].find()
    for audio in audios:
        rhytmic = TEMPOS.RHYTHMIC if audio["to_sport_list"] else TEMPOS.NON_RHYTHMIC
        parsed.append([audio["bpm_avg"], audio["bpm_counter"], audio["high_bpm_sequence"], rhytmic])
    return parsed


def load_dataset(audio_db, new_song=None):
    training_set = []
    test_set = []
    dataset = create_dataset(audio_db)
    random.shuffle(dataset)
    if not new_song:
        x = int((random.choice(DATASET_SPLIT_RANGE_OPTIONS) / 10.0) * len(dataset))
        training_set.extend(dataset[x:])
        test_set.extend(dataset[:x])
        random.shuffle(training_set)
        random.shuffle(test_set)

    else:
        training_set = dataset
        test_set.append([new_song[0], new_song[1], new_song[2], new_song[3]])
    return training_set, test_set