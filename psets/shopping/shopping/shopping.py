import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix

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
        data = {"evidence" : [], "label" : []}
        # for row in reader:
        #     data["evidence"].append([cell for cell in row[:-1]])
        #     data["label"].append(1 if row[len(row) - 1] == "TRUE" else 0)
        # print(f"Data: {data}")
        months = {"Jan" : 0,
                  "Feb" : 1,
                  "Mar" : 2,
                  "Apr" : 3,
                  "May" : 4,
                  "June" : 5,
                  "Jul" : 6,
                  "Aug" : 7,
                  "Sep" : 8,
                  "Oct" : 9,
                  "Nov" : 10,
                  "Dec" : 11}
        for dataRow in reader : 
            row = []
            for cell in range(len(dataRow) - 1):
                if cell == 0 or cell == 2 or cell == 4 or cell == 11 or cell == 12 or cell == 13 or cell == 14:
                    row.append(int(dataRow[cell]))
                elif cell == 10:
                    row.append(months[dataRow[cell]]) 
                elif cell == 15:
                    if dataRow[cell] == "Returning_Visitor":
                        row.append(1)
                    else:
                        row.append(0)
                elif cell == 16:
                    if dataRow[cell] == "TRUE":
                        row.append(1)
                    else:
                        row.append(0)
                else : 
                    row.append(float(dataRow[cell]))
            
            data["evidence"].append(row)

            if dataRow[-1] == "TRUE":
                data["label"].append(1)
            else:
                data["label"].append(0)
        
        # print(f"evidence[0] : {data['evidence'][0]}")
        # print(f"label[0] : {data['label'][0]}")
    return (data["evidence"], data["label"])


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
    # correct = (labels == predictions).sum()
    # # incorrect = (labels != predictions).sum()
    # print(f"correct in function : {correct}")

    
    # # sensitivity = correct/len(labels)
    # # specificity = incorrect/len(labels)

    # sensitivity = correct/counterRight
    # specificity = incorrect/counterWrong

    # tp = ((labels == 1) & (predictions == 1)).sum()
    # fp = ((labels == 0) & (predictions == 1)).sum()
    # tn = ((labels == 0) & (predictions == 0)).sum()
    # fn = ((labels == 1) & (predictions == 0)).sum()
    
    # sensitivity = tp / (tp + fn) if (tp + fn) != 0 else 0.0 
    # specificity = tn / (tn + fp) if (tn + fp) != 0 else 0.0

    tn, fp, fn, tp = confusion_matrix(labels, predictions).ravel()

    sensitivity = tp / (tp + fn)
    specificity = tn / (tn + fp)
    
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
