import sys

from States import *
from constants import *
from NeuralNet import *
from Snake import *
from tqdm import tqdm

LOADING_BAR = False

class tomBot(object):
    def __init__(self):
        pass
    def getIndex(self,xvel,yvel):
        # Gets the DIRECTIONS index from constants that translates from the given values. (Pretty much a switch to avoid copy and paste)
        if xvel == -1:
            return (DIRECTIONS.index("LEFT"), "LEFT")
        elif xvel == 1:
            return (DIRECTIONS.index("RIGHT"), "RIGHT")
        elif yvel == 1:
            return (DIRECTIONS.index("UP"), "UP")
        else:
            return (DIRECTIONS.index("DOWN"), "DOWN")
    
    
    def heuristic(self, desiredDir):
        """
        Determines if the block is free in the direction we want to go in
        takes: currentDir, desiredDir, left, straight, right
        returns: if the desired direction is safe
        """
        # if we are trying to move in the opposite direction/the move is illegal, return -1
        if DIRECTIONS[(DIRECTIONS.index(self.currentDirection) + 2) % 4] == desiredDir:
            return -5
        elif self.currentDirection == desiredDir and self.straightCollision == -1:
            return -5
        elif DIRECTIONS[(DIRECTIONS.index(self.currentDirection) + 1) % 4] == desiredDir and self.rightCollision == -1:
            return -5
        elif DIRECTIONS[(DIRECTIONS.index(self.currentDirection) - 1) % 4] == desiredDir and self.leftCollision == -1:
            return -5

        # Otherwise we have a valid Direction to move in, so lets get the heuristic!

        if desiredDir == 'RIGHT':
            return self.relX
        elif desiredDir == 'UP':
            return self.relY
        elif desiredDir == 'LEFT':
            return -self.relX
        else:
            return -self.relY

    def getDirection(self, ann_inputs):
        # tomBot takes ann_inputs, looks at free space directly next to snake head, then moves snake towards goal without running into walls
        # ann_inputs have the come in a list in the following order:
        # [relX, relY, to_the_left, in_front, to_the_right, x_vel, y_vel]
        # relX is from -1 : 1 and is how far away the food is in the x direction. -1 means you need to go left, 1 means go right.
        # relY is from -1 : 1 and is how far away the food is in the y direction. -1 means you need to go down, 1 means go up.
        # the next three inputs are the things in the squares adjacent to the snake in the direction it is going
        # i.e it is what is in front of it if the snake turns left, right or straight.
        # -1 in this case means collision with itself or a wall, while 1 means food!
        # x_vel and y_vel describe the current direction with:
        #   (1,0) being right: (-1,0) being left: (0,1) being up: (0,-1) being down

        self.relX = ann_inputs[0]
        self.relY = ann_inputs[1]
        self.leftCollision = ann_inputs[2]
        self.straightCollision = ann_inputs[3]
        self.rightCollision = ann_inputs[4]
        self.x_vel = ann_inputs[5]
        self.y_vel = ann_inputs[6]

        #Don't actually use the Index part of this, can change this later.

        self.currentIndex, self.currentDirection = self.getIndex(self.x_vel,self.y_vel)

        temp = {}

        for x in DIRECTIONS:
            temp[x] = self.heuristic(x)

        if max(temp.values()) <= -1:
            print("Forced crash")
        return max(temp, key = temp.get)


        """
        Note to Tom: I tried to fix this, but there was a fundamental problem. I will explain it to you later.
                     I was bored, so I implemented something basic/what I think you tried to do above.
                     I also renamed the variables, and made a fat comment. Hopefully this helps!

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
        """
def main(headless):
    gameOvered = False
    if LOADING_BAR:
        pbar = tqdm(total = POINTS_DESIRED, ascii = True, desc = "GETTING TOMBOT DATA")
    counter = 0
    game_no = 1
    while counter <= POINTS_DESIRED:
        print("Gamer number: " + str(game_no))
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
            game_no += 1
            gameOvered = True
    if LOADING_BAR:
        pbar.close()

if __name__ == '__main__':
    # True here to display TomBot, false to just be speedy
    main(True)