# IMPORTS
import sys

from States import *
from constants import *
from NeuralNet import *


# GLOBAL VARIABLES
clock = pygame.time.Clock()
ann = NeuralNet(NUM_INPUTS, NUM_OUTPUTS, NUM_HIDDEN, NUM_PER_HIDDEN)


# STATE MANAGER
class StateManager(object):
    def __init__(self, ann=None, tomBot = None, predictor = None, GAinput = None):
        """
        Initializes the state manager.
        Contains "global" variables to hold neural network and score.
        """
        self.ann = ann
        self.tomBot = tomBot
        self.predictor = predictor
        self.GAinput = GAinput
        self.fitness = 0

        self.state = None
        self.go_to(MenuState())

    def go_to(self, state):
        self.state = state
        self.state.manager = self


# GAME ENGINE
def main():
    pygame.init()
    pygame.display.set_caption("Snake")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill((0, 0, 0))

    running = True
    manager = StateManager()

    while running:
        clock.tick(FRAMES_PER_SEC)

        if pygame.event.get(QUIT):
            sys.exit(0)

        manager.state.handle_events(pygame.event.get())
        manager.state.update()
        manager.state.render(screen)
        pygame.display.flip()


# FITNESS FUNCTION
def fitness(weights, headless=1):
    """
    Calculate the fitness function.
    :param weights: weights representing the ANN.
    :return: score of the ANN represented
    """
    ann.set_weights(weights)

    pygame.init()
    pygame.display.set_caption("Snake")

    screen = None

    if headless == 0:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill((0, 0, 0))

    manager = StateManager(ann)
    manager.go_to(PlayState())

    while not isinstance(manager.state, GameOverState):
        if headless == 0:
            clock.tick(FRAMES_PER_SEC)

        manager.state.update()

        if headless == 0:
            manager.state.render(screen)
            pygame.display.flip()

    return manager.fitness

def vectorFitness(vectorGA, headless = 1):

    pygame.init()
    pygame.display.set_caption("Snake")

    screen = None

    if headless == 0:
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.fill((0, 0, 0))

    manager = StateManager(GAinput = vectorGA)
    manager.go_to(PlayState())

    counter = 0

    while not isinstance(manager.state, GameOverState) and counter < MAX_MOVES:
        if headless == 0:
            clock.tick(FRAMES_PER_SEC)

        manager.state.update()
        counter += 1

        if headless == 0:
            manager.state.render(screen)
            pygame.display.flip()

    return manager.fitness




# PROGRAM EXECUTION
if __name__ == '__main__':
    main()
    """
    # Test ANN produced from GA
    best_weights = (
        [-0.9672259081515102, -0.10728386348933046, 1.1878966452172786, -0.9478098494388567, 1.0631734637054016, 0.5943329587331927, -0.8920517011350171, 0.12712039009361953, -0.4420322880482488, -0.6299301804207347, -0.564406980223174, 0.5689865246664952, -0.03967624577490548, 0.48583063847247443, 0.24498541448067646, -0.6561074059131791, -0.302742440771308, -0.9269103868913515, 0.07952861614382835, -0.972739946811265, 0.6040649644014084, -0.48556106530184784, -0.9434889002512998, 0.6165113224127585, -0.8897227354303252, -0.9468255626257698, 0.7526988913876951, 0.8273647072687531, -0.07536285845964197, -0.655307086415933])
    for x in range(16):
        print(fitness(best_weights, 0))
        """
     
    
