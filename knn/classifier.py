import pickle
from random import shuffle
from conf import ACCURACY_THRESHOLD, GOOD_DATASET_PATH, K_POINTS
from data import load_dataset
from knn import get_neighbors
from prediction import get_accuracy, predict


__author__ = "Ori Roza"


def dump_best_accuracy(accuracy, dataset):
    if accuracy >= ACCURACY_THRESHOLD:
        with open(GOOD_DATASET_PATH, "wb") as f:
            pickle.dump(dataset, f)
            return True
    return False


def run(audio_db, prepared_dataset=None, new_song=None):
    # prepare data
    training_set, test_set = load_dataset(audio_db, new_song)
    if prepared_dataset:
        training_set = pickle.load(prepared_dataset)
        shuffle(training_set)
    print 'Train set: ' + repr(len(training_set))
    print 'Test set: ' + repr(len(test_set))
    # generate predictions
    predictions = []
    if not new_song:
        for x in range(len(test_set)):
            neighbors = get_neighbors(training_set, test_set[x], K_POINTS)
            result = predict(neighbors)
            predictions.append(result)
            print('> predicted=' + repr(result) + ', actual=' + repr(test_set[x][-1]))
        accuracy = get_accuracy(test_set, predictions)  # check accuracy
        print 'Accuracy: ' + repr(accuracy)
        return dump_best_accuracy(dataset=training_set, accuracy=accuracy)  # Returns True If accuracy is bigger than threshold else False
    else:
        neighbors = get_neighbors(training_set, test_set[0], K_POINTS)
        return predict(neighbors)