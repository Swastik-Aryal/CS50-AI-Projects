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
        headers = next(reader)

        int_values = [
            "Administrative",
            "Informational",
            "ProductRelated",
            "OperatingSystems",
            "Browser",
            "Region",
            "TrafficType",
        ]
        float_values = [
            "Administrative_Duration",
            "Informational_Duration",
            "ProductRelated_Duration",
            "BounceRates",
            "ExitRates",
            "PageValues",
            "SpecialDay",
        ]
        month_dict = {
            "Jan": 0,
            "Feb": 1,
            "Mar": 2,
            "April": 3,
            "May": 4,
            "June": 5,
            "Jul": 6,
            "Aug": 7,
            "Sep": 8,
            "Oct": 9,
            "Nov": 10,
            "Dec": 11,
        }
        visitor_type = {"Returning_Visitor": 1, "New_Visitor": 0, "Other": 0}
        weekend_type = {"TRUE": 1, "FALSE": 0}
        labels_type = {"TRUE": 1, "FALSE": 0}

        evidence = []
        labels = []
        idx = 0

        for row in reader:
            row_evidence = []

            for i in range(len(row) - 1):
                if i in [headers.index(header) for header in int_values]:
                    row_evidence.append(int(row[i]))
                elif i in [headers.index(header) for header in float_values]:
                    row_evidence.append(float(row[i]))
                elif row[i] in month_dict:
                    row_evidence.append(month_dict[row[i]])
                elif row[i] in visitor_type:
                    row_evidence.append(visitor_type[row[i]])
                elif row[i] in weekend_type:
                    row_evidence.append(weekend_type[row[i]])

            evidence.append(row_evidence)
            labels.append(labels_type[row[-1]])

            idx += 1

    return (evidence, labels)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """

    model = KNeighborsClassifier(n_neighbors=1)

    model.fit(evidence, labels)

    return model


def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """

    pos_labels_identified = 0
    total_pos_labels = 0

    neg_labels_identified = 0
    total_neg_labels = 0

    for actual, predicted in zip(labels, predictions):
        # count for sensitivity
        if actual == 1:
            total_pos_labels += 1
            if predicted == 1:
                pos_labels_identified += 1
        if actual == 0:
            total_neg_labels += 1
            if predicted == 0:
                neg_labels_identified += 1

    sensitivity = float(pos_labels_identified / total_pos_labels)
    specificity = float(neg_labels_identified / total_neg_labels)

    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
