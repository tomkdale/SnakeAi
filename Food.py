import random
import math
from Board import *
types = int, int


# FOOD DEFINITION
class Food:
    def __init__(self, number = 0):

        if NO_RANDOM == True:
            self.locations = []
            self.count = 0
            with open("Foodpositions.txt", 'r') as f:
                for line in f:
                    elements = tuple(t(e) for t,e in zip(types, line.split()))
                    self.locations.append(elements)
            self.position = self.locations[0]

        elif number == 0:
            self.position = 5,5
        elif number == 1:
            self.position = NUM_COLS - 5, 5
        elif number == 2:
            self.position = NUM_COLS - 5, NUM_ROWS - 5
        else:
            self.position = 5, NUM_ROWS - 5

        """
        self.position = self.next_indices()
        while (self.position[0] == NUM_ROWS // 2 or self.position[1] == NUM_COLS // 2) \
        or (abs(self.position[0] - (NUM_ROWS // 2)) < 5 and abs(self.position[1] - (NUM_COLS // 2)) < 5):
            self.position = self.next_indices()
        """
        self.old_center = None
        self.center = Board.get_center(self.position[0], self.position[1])
        self.radius = CELL_SIDE // 2 - 1
        self.score = 10
        self.color = YELLOW

    @staticmethod
    def next_indices():
        """
        Calculate next index randomly for a food item to appear.
        :return: row and column position
        """
        row = random.randint(0, NUM_ROWS - 1)
        column = random.randint(0, NUM_COLS - 1)
        return row, column

    def move(self):
        """
        Moves the food to a new location and saves its old location.
        Also, updates its center.
        """
        self.old_center = self.center
        if NO_RANDOM == True:
            self.count += 1
            self.position = self.locations[self.count]
        else:
            self.position = Food.next_indices()
        self.center = Board.get_center(self.position[0], self.position[1])


if __name__ == '__main__':
    dataFood = Food()
    with open("FoodPositions.txt",'w') as f:
        for i in range(300):
            f.write(str(dataFood.position[0]) + ' ' + str(dataFood.position[1]) + '\n')
            dataFood.move()
            print(dataFood.position)
