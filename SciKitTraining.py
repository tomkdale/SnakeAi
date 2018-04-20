from sklearn.neural_network import MLPClassifier
import csv

def train(model):
    dataRows = []

    with open('data.txt') as f:
        reader = csv.reader(f)
        for row in reader:
            for x in row:
                row[row.index(x)] = float(x)
            dataRows.append(row)

    X = []
    Y = []

    for row in dataRows:
        X.append(row[:-3])
        Y.append(row[-3:])

    clf = MLPClassifier(solver = 'lbfgs', alpha = 1e-5,
                        hidden_layer_sizes = (15,), random_state = 1)

    clf.fit(X,Y)

    print(clf.predict([[0.0, 0.05263157894736842, 0, 0, 1, -1, 0]]))
    #output should be 0, 0, 1

if __name__ == '__main__':
    train(model = 0)