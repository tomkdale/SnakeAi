from constants import *
import numpy as np
import Snake
from tqdm import tqdm
import random


# Default tuning parameters
POP_SIZE = 10000
NUM_GENS = 1000
CROSS_RATE = 50 / 100 # Keep this at 50 to perform uniform crossover
MUTATE_RATE = 4 / 100 # This seems reasonable (4%)
TOURNAMENT_PERCENT = 20 / 100   # Percent of the population in each tournament


SHOW_NEW_BEST = False

class VectorGenome(object):
    def __init__(self, dVector=None, fitness=None):
        self.decisionVector = None
        if dVector is None:
            self.decisionVector = (np.random.randint(-1,2, size = MAX_MOVES)).tolist()
        else:
            self.decisionVector = dVector

        self.fitness = fitness
        self.counter = 0

    def copy(self):
        return VectorGenome(self.decisionVector, self.fitness)

    def get_fitness(self):
        if self.fitness is None:
            self.recalculate_fitness()
        return self.fitness

    def recalculate_fitness(self):
        self.fitness = Snake.vectorFitness(self)

    def __str__(self):
        return self.decisionVector

    def __gt__(self, other):
        return self.get_fitness() > other.get_fitness()
    """
    returns: the next direction that the GA is meant to have
    gets: the current direction
    format: "UP", "DOWN", "LEFT" or "RIGHT"
    """
    def getDirection(self, currentDir):
        currentIndex = DIRECTIONS.index(currentDir)
        currentIndex = (currentIndex + self.decisionVector[self.counter]) % 4
        self.counter += 1
        return DIRECTIONS[currentIndex]

class vectorGA(object):
    def __init__(self, pop_size=POP_SIZE, num_gens=NUM_GENS, mut_rate=MUTATE_RATE, cross_rate=CROSS_RATE):
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.mut_rate = mut_rate
        self.cross_rate = cross_rate

        self.total_fitness = 0
        self.best_fitness = 0
        self.avg_fitness = 0
        self.worst_fitness = 0
        self.best_genome = None

    def mutate(self, genome):
        new_vectorGenome = genome.copy()
        dVector = new_vectorGenome.decisionVector
        for x in dVector:
            if self.mut_rate >= random.random():
                choices = [-1,0,1]
                choices.remove(x)
                x = random.choice(choices)
        new_vectorGenome.decisionVector = dVector
        return new_vectorGenome

    def crossover(self, g1, g2):
        c = g1.copy()

        for i in range(len(c.decisionVector)):
            if self.cross_rate >= random.random():
                c.decisionVector[i] = g2.decisionVector[i]

        return c

    def epoch(self, old_population):
        random.shuffle(old_population)
        competitors = old_population[0:int(TOURNAMENT_PERCENT * POP_SIZE)]
        old_population.sort()

        winners = []
        losers = []

        for i in range(0, len(competitors), 2):
            if competitors[i].get_fitness() > competitors[i+1].get_fitness():
                winners.append(competitors[i])
                losers.append(competitors[i+1])
            else:
                winners.append(competitors[i+1])
                losers.append(competitors[i])

        for i in tqdm(range(len(winners)), ascii = True, desc = "BREEDING", leave = False):
            temp = self.crossover(winners[i], random.choice(winners))
            if temp.get_fitness() > losers[i].get_fitness():
                old_population[0] = temp
                old_population.sort()
            temp = self.mutate(winners[i])
            if temp.get_fitness() > winners[i].get_fitness():
                if winners[i] in old_population:
                    index = old_population.index(winners[i])
                    old_population[index] = temp
                old_population.sort()
            
   
        self.total_fitness = 0  # Reset old total fitness
        
        # Identify current most fit individual and perform fitness calculations
        for genome in old_population:
            self.total_fitness += genome.get_fitness()
            if self.best_genome is None or genome.get_fitness() > self.best_genome.get_fitness():
                fitness = genome.get_fitness()
                self.best_genome = genome.copy()
                self.best_genome.fitness = fitness
                if (SHOW_NEW_BEST):
                    Snake.vectorFitness(self.best_genome, 0)

        displayGenome = self.best_genome.copy()

        Snake.vectorFitness(displayGenome, 0)

        # Record fitness value parameters
        self.avg_fitness = self.total_fitness / len(old_population)
        self.best_fitness = self.best_genome.get_fitness()

        return old_population


def main():
    # Calculate number of weights
    ga = vectorGA()

    population = ga.pop_size * [None]
    
    for i in tqdm(range(0, ga.pop_size), ascii = True, desc = "GENERATING INITIAL POPULATION"):
        population[i] = VectorGenome()
        population[i].get_fitness()

    # Store best genome for each generation
    best_genomes = []


    for i in range(ga.num_gens):
        # Call epoch at each step
        population = list(ga.epoch(population))
        best_genomes.append(ga.best_genome.decisionVector)

        # Print population characteristics
        print("Gen " + str(i) + ": " + "best: " + str(ga.best_fitness) + \
              ", avg: " + str(ga.avg_fitness))

    # Output structure of fittest individual
    print(best_genomes[-1])


# Run the GA
if __name__ == '__main__':
    while True:
        main()