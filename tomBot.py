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
    def getDirection(self,myPos,foodPos):
        #tombot takes self postion and food posion, looks at free space directly next to snake head, then moves snake towards goal without running into walls
        myX, myY = myPos
        food_x,food_y = foodPos
        left = Board.check_collision(self,(myX-1,myY) != -1
        right = Board.check_collision(self,(myX+1,myY) != -1
        up = Board.check_collision(self,(myX,myY+1) != -1
        down = Board.check_collision(self,(myX,myY-1) != -1
        
        
        if(myY == food_x) or (myY < food_y and up != EMPTY) or (myY > food_y and down != EMPTY)
            if(myX < food_x)
                if(right == EMPTY)
                    return 'RIGHT'
            else
                if(left == EMPTY)
                    return 'Left'
        else
            if(myY < food_y)
                if(up == EMPTY)
                    return 'UP'
            else
                if(down == EMPTY)
                    return 'DOWN'

        if(right == EMPTY) return 'RIGHT'
        elif (left == EMPTY) return 'LEFT'
        elif(up == EMPTY) return 'UP'
        else return 'DOWN'

def main(headless):
    gameOvered = False
    if LOADING_BAR:
        pbar = tqdm(total = POINTS_DESIRED, ascii = True, desc = "GETTING TOMBOT DATA")
    counter = 0
    while counter <= POINTS_DESIRED:
        bot = tomBot()
        pygame.init()
        pygame.display.set_caption("Snake")

        screen = None

        if headless:
            screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
            screen.fill((0, 0, 0))

        manager = StateManager(None, bot)
        manager.go_to(PlayState())

        while not isinstance(manager.state, GameOverState) and counter <= POINTS_DESIRED:
            if headless:
                clock.tick(FRAMES_PER_SEC)
            
            counter += 1
            if LOADING_BAR and not gameOvered:
                pbar.update(1)
            else:
                gameOvered = False
            manager.state.update()

            if headless:
                manager.state.render(screen)
                pygame.display.flip()
        if counter < POINTS_DESIRED:
            counter -= 1
            gameOvered = True
    if LOADING_BAR:
        pbar.close()

if __name__ == '__main__':
    # True here to display TomBot, false to just be speedy
    main(False)