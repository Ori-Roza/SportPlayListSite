import operator

__author__ = "Ori Roza"


def predict(neighbors):
    classes_vote = {}
    for x in range(len(neighbors)):
        response = neighbors[x][-1]
        if response in classes_vote:
            classes_vote[response] += 1
        else:
            classes_vote[response] = 1
    sorted_votes = sorted(classes_vote.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sorted_votes[0][0]


def get_accuracy(target_set, predictions):
    correct = 0
    for x in range(len(predictions)):
        if target_set[x][-1] == predictions[x]:
            correct += 1
    return (correct / float(len(target_set))) * 100.0