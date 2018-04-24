from sklearn.neural_network import MLPClassifier
import csv
from constants import *
from States import *
from Snake import *
import matplotlib.pyplot as plt

class predictorNeuralNet(object):
    def __init__(self, clfModel):
        self.model = clfModel
    def getDirection(self, ann_inputs):

        prediction = self.model.predict([ann_inputs])

        prediction = prediction[0]

        x_vel = ann_inputs[5]
        y_vel = ann_inputs[6]

        return self.getTextDirection(prediction, x_vel, y_vel)

    def getTextDirection(self, outputArray, xvel, yvel):
        index = 0

        if xvel == -1:
            index = DIRECTIONS.index("LEFT")
        elif xvel == 1:
            index = DIRECTIONS.index("RIGHT")
        elif yvel == -1:
            index = DIRECTIONS.index("DOWN")
        else:
            index = DIRECTIONS.index("UP")

        if outputArray[0] == 1:
            index = (index - 1) % 4
        if outputArray[1] == 1:
            pass
        else:
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
        Y.append(row[-3:])

    model.fit(X,Y)
    #print("Training set score: %f" % model.score(X, Y))
    print("Training set loss: %f" % model.loss_)
    plt.plot(model.loss_curve_)
    plt.show()

if __name__ == '__main__':
    clf = MLPClassifier(solver = 'sgd', learning_rate = 'invscaling', momentum = .9, nesterovs_momentum = True, learning_rate_init = 0.2)
    train(clf)
    for i in range(10):
        test(clf)
