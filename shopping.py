import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    with open(filename) as f:
        reader = csv.reader(f)
        next(reader)
        mon = {"Jan":0, "Feb":1, "Mar":2, "Apr":3, "May":4, "June":5, "Jul":6, "Aug":7, "Sep":8, "Oct":9, "Nov":10, "Dec":11}
        vis = {"Returning_Visitor":1,"New_Visitor":0}
        weekend = {"TRUE":1, "FALSE":0}
        label = {"TRUE":1, "FALSE":0}
        data = {"evidence": [], "labels": []}

        for i in reader:
            a = i[::]
            for j in [0,2,4,11,12,13,14]:
                a[j] = int(a[j])
            for j in [1,3,5,6,7,8,9]:
                a[j] = float(a[j])
            a[10] = mon[a[10]]
            a[16] = weekend[a[16]]
            if a[15] not in vis.keys():
                a[15] = 0
            else:
                a[15] = vis[a[15]]
            a[17] = label[a[17]]
            data["evidence"].append(a[:17])
            data["labels"].append(a[17])
        return (data["evidence"], data["labels"],)
            
    # raise NotImplementedError


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    b = KNeighborsClassifier(n_neighbors = 1)
    b.fit(evidence,labels)
    return b
    # raise NotImplementedError


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    pos = 0
    neg = 0
    pos1 = 0
    neg1 = 0
    for label,prediction in zip(labels,predictions):
        if label == 0:
            neg +=1
            if prediction == 0:
                neg1 += 1
        elif label == 1:
            pos += 1
            if prediction == 1:
                pos1 +=1
        else:
            raise ValueError

    c = float(pos1/pos)
    d = float(neg1/neg)

    return (c,d,)
    # raise NotImplementedError


if __name__ == "__main__":
    main()
