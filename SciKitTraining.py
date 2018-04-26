from sklearn.neural_network import MLPClassifier
import csv
from constants import *
from States import *
from Snake import *
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler


params = [{'solver': 'sgd', 'learning_rate': 'constant', 'momentum': 0,
           'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': .9,
           'nesterovs_momentum': False, 'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': .9,
           'nesterovs_momentum': True, 'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': 0,
           'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': .9,
           'nesterovs_momentum': True, 'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': .9,
           'nesterovs_momentum': False, 'learning_rate_init': 0.2},
          {'solver': 'adam', 'learning_rate_init': 0.01}]

labels = ["constant learning-rate", "constant with momentum",
          "constant with Nesterov's momentum",
          "inv-scaling learning-rate", "inv-scaling with momentum",
          "inv-scaling with Nesterov's momentum", "adam"]

plot_args = [{'c': 'red', 'linestyle': '-'},
             {'c': 'green', 'linestyle': '-'},
             {'c': 'blue', 'linestyle': '-'},
             {'c': 'red', 'linestyle': '--'},
             {'c': 'green', 'linestyle': '--'},
             {'c': 'blue', 'linestyle': '--'},
             {'c': 'black', 'linestyle': '-'}]


def plot_on_dataset(X, y, ax, name):
    # for each dataset, plot learning for each learning strategy
    print("\nlearning on dataset %s" % name)
    ax.set_title(name)
    X = MinMaxScaler().fit_transform(X)
    mlps = []
    if name == "digits":
        # digits is larger but converges fairly quickly
        max_iter = 15
    else:
        max_iter = 400

    for label, param in zip(labels, params):
        print("training: %s" % label)
        mlp = MLPClassifier(verbose=0, random_state=0,
                            max_iter=max_iter, **param)
        mlp.fit(X, y)
        mlps.append(mlp)
        print("Training set score: %f" % mlp.score(X, y))
        print("Training set loss: %f" % mlp.loss_)
    for mlp, label, args in zip(mlps, labels, plot_args):
            ax.plot(mlp.loss_curve_, label=label, **args)
"""
Everything above this line is used to compare classifiers.
++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
Everything below this line is to use a particular classifier to play snake.
"""
class predictorNeuralNet(object):
    def __init__(self, clfModel):
        self.model = clfModel
    def getDirection(self, ann_inputs):

        prediction = self.model.predict([ann_inputs])

        prediction = prediction[0]

        x_vel = ann_inputs[5]
        y_vel = ann_inputs[6]

        return self.getTextDirection(prediction, x_vel, y_vel)

    def getTextDirection(self, output, xvel, yvel):
        index = 0

        if xvel == -1:
            index = DIRECTIONS.index("LEFT")
        elif xvel == 1:
            index = DIRECTIONS.index("RIGHT")
        elif yvel == -1:
            index = DIRECTIONS.index("DOWN")
        else:
            index = DIRECTIONS.index("UP")

        if output == 0:
            index = (index - 1) % 4
        elif output == 1:
            pass
        elif output == 2:
           index = (index + 1) % 4

        return DIRECTIONS[index]

def test(model):
    predictorNet = predictorNeuralNet(model)
    pygame.init()
    pygame.display.set_caption("Snake")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))

    manager = StateManager(predictor = predictorNet)
    manager.go_to(PlayState())

    while not isinstance(manager.state, GameOverState):
        clock.tick(FRAMES_PER_SEC)
        manager.state.update()
        manager.state.render(screen)
        pygame.display.flip()


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
        output = row[-3:]
        if output[0] == 1:
            Y.append(0)
        elif output[1] == 1:
            Y.append(1)
        else:
            Y.append(2)

    model.fit(X,Y)
    print("Training set score: %f" % model.score(X, Y))
    print("Training set loss: %f" % model.loss_)
    plt.plot(model.loss_curve_)
    plt.xlabel('Iterations')
    plt.ylabel('Loss')
    plt.title('Loss over time for this classifier')
    plt.show()



# This main contains what we think to be the best nn, and simply trains it on the 200 000 data points, and then displays it 10 times

if __name__ == '__main__':
    clf = MLPClassifier(solver = 'adam', learning_rate_init = 0.001)
    train(clf)
    for i in range(10):
        test(clf)

"""

# This main can be used if you wish to compare the different learning methods...

if __name__ == '__main__':
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
        output = row[-3:]
        if output[0] == 1:
            Y.append(0)
        elif output[1] == 1:
            Y.append(1)
        else:
            Y.append(2)

    fig, axes = plt.subplots(figsize=(15, 10))
    plot_on_dataset(X,Y, axes, name = 'SnakeBot')
    fig.legend(axes.get_lines(), labels, ncol=3, loc="upper center")
    plt.show()
"""