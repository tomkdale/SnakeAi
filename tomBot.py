import sys

from States import *
from constants import *
from NeuralNet import *
from Snake import *
from tqdm import tqdm

LOADING_BAR = True

class tomBot(object):
    def __init__(self):
        pass
    def getDirection(self, ann_inputs):
        # modify inputs, do math and determine direction
        # output a 'LEFT','RIGHT','DOWN','UP'
        return 'LEFT'

def main(headless):
    if LOADING_BAR:
        pbar = tqdm(total = POINTS_DESIRED, ascii = True, desc = "GETTING TOMBOT DATA")
    counter = 0
    while counter < POINTS_DESIRED:
        bot = tomBot()
        pygame.init()
        pygame.display.set_caption("Snake")

        screen = None

        if headless:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.fill((0, 0, 0))

        manager = StateManager(None, bot)
        manager.go_to(PlayState())

        while not isinstance(manager.state, GameOverState) and counter < POINTS_DESIRED:
            if headless:
                clock.tick(FRAMES_PER_SEC)
            
            counter += 1
            if LOADING_BAR:
                pbar.update(1)
            manager.state.update()

            if headless:
                manager.state.render(screen)
                pygame.display.flip()
    if LOADING_BAR:
        pbar.close()

if __name__ == '__main__':
    # True here to display TomBot, false to just be speedy
    main(False)