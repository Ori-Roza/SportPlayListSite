# SportPlayListSite
Flask app that shows only rhythmic songs for a sport playlist using KNN algorithm model.

Aubio Library has been used for analyzing Audio files.
The BPM extractor is not that accurate. (That's why I've added data correction option)

KNN has been used for predict whether a song is rhythmic.

I took the example from:
 https://machinelearningmastery.com/tutorial-to-implement-k-nearest-neighbors-in-python-from-scratch/

Thanks for this tutorial!


# How to use:

    * add songs to /static/songs directory

    * Run insert_new_audio.py for adding new audios

    * Follow the script instructions (Using existing dataset or add data manually and train model

    * run main.py for accessing the server
