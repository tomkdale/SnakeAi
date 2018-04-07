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
    
    
    def checkOK(self, currentDir, desiredDir, left, straight, right):
        """
        Determines if the block is free in the direction we want to go in
        takes: currentDir, desiredDir, left, straight, right
        returns: if the desired direction is safe
        """
        # if we are trying to move in the opposite direction...
        if DIRECTIONS[(DIRECTIONS.index(currentDir) + 2) % 4] == desiredDir:
            return False
        if currentDir == desiredDir:
            return straight != -1
        elif DIRECTIONS[(DIRECTIONS.index(currentDir) + 1) % 4] == desiredDir: # if we want to turn right
            return right != -1
        else:
            return left != -1

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

        relX = ann_inputs[0]
        relY = ann_inputs[1]

        leftCollision = ann_inputs[2]
        straightCollision = ann_inputs[3]
        rightCollision = ann_inputs[4]
        x_vel = ann_inputs[5]
        y_vel = ann_inputs[6]

        currentIndex, currentDirection = self.getIndex(x_vel,y_vel)

        temp = DIRECTIONS.copy()

        if (abs(relX) >= abs(relY)): # If we want to move closer in the x direction
            if relX > 0:
                if self.checkOK(currentDirection,"RIGHT",leftCollision,straightCollision,rightCollision):
                    return "RIGHT"
                temp.remove("RIGHT")
            elif relX < 0:
                if  self.checkOK(currentDirection,"LEFT",leftCollision,straightCollision,rightCollision):
                    return "LEFT"
                temp.remove("LEFT")
            else:
                print(relX)
        else:   # If we want to move closer in the y direction
            if relY > 0:
                if  self.checkOK(currentDirection,"UP",leftCollision,straightCollision,rightCollision):
                    return "UP"
                temp.remove("UP")
            elif relY < 0:
                if  self.checkOK(currentDirection,"DOWN",leftCollision,straightCollision,rightCollision):
                    return "DOWN"
                temp.remove("DOWN")
            else:
                print("Yok")

        # So we tried the easy things, and they did not work
        # The possibilities are:
        #   - The way was blocked
        #   - The direction was invalid

        # Now we are going to try and minimize the other coordinate, removing it from temp if it failed

        if "DOWN" in temp and "UP" in temp:
            if relY > 0:
                if self.checkOK(currentDirection,"UP",leftCollision,straightCollision,rightCollision):
                    return "UP"
                temp.remove("UP")

            elif relY < 0:
                if self.checkOK(currentDirection,"DOWN",leftCollision,straightCollision,rightCollision):
                    return "DOWN"
                temp.remove("DOWN")

  
        else:
            if relX > 0:
                if self.checkOK(currentDirection,"RIGHT",leftCollision,straightCollision,rightCollision):
                    return "RIGHT"
                temp.remove("RIGHT")
            elif relX < 0:
                if self.checkOK(currentDirection,"LEFT",leftCollision,straightCollision,rightCollision):
                    return "LEFT"
                temp.remove("LEFT")

        # Now all that is left is random selection(?)
        random.shuffle(temp)
        for i in range(len(temp) - 1):
            if self.checkOK(currentDirection,temp[0],leftCollision,straightCollision,rightCollision):
                return temp[0]
            temp.pop(0)
        if self.checkOK(currentDirection,temp[0],leftCollision,straightCollision,rightCollision):
            print("forced crash :(")
        return temp[0]



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