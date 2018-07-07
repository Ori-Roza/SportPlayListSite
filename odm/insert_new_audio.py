
from knn import classifier
from odm.audios import Audios, BASE_SONG_SOURCE, MP3_AUDIO_EXT, os, DEBUG

__author__ = "Ori Roza"


def insert_options():
    audios_odm = Audios()
    option = int(raw_input("OPTION 1 TO FIND BEST DATASET\nOPTION 2 TO INSERT NEW AUDIO\n> "))
    if option == 1:
        while True:
            if classifier.run(audios_odm.audios_db):
                break
    elif option == 2:
        option = int(raw_input("OPTION 1 TO TRAIN\nOPTION 2 TO INSERT NEW AUDIO USING MODEL\n> "))
        if option == 1:
            train = True
        elif option == 2:
            train = False
        else:
            raise ValueError("Value %d is incorrect" % option)
        for song in os.listdir(BASE_SONG_SOURCE):
            if song.endswith(MP3_AUDIO_EXT):
                print song
                if audios_odm.insert_new_audio(os.path.join(BASE_SONG_SOURCE, song), train=train):
                    print "%s is added successfully" % song
                    if DEBUG:
                        raw_input("---")

    else:
        raise ValueError("Value %d is incorrect" % option)


if __name__ == '__main__':
    insert_options()