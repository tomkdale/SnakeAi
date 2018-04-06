__author__ = 'Aaron'

from constants import *
from NeuralNet import *
import Snake
import time
from tqdm import tqdm

# Default tuning parameters
POP_SIZE = 5000
NUM_GENS = 1000
CROSS_RATE = 50 / 100 # Keep this at 50 to perform uniform crossover
MUTATE_RATE = 4 / 100 # This seems reasonable (4%)
FITNESS_ATTEMPTS = 16 # This should be kept at 16 for the time being unless you want to re arrange how fitness is calculated
TOURNAMENT_PERCENT = 20 / 100   # Percent of the population in each tournament

# Make this true to show the best snake each time there is a new best!
SHOW_NEW_BEST = True
# Make this true to show the best each time the generation is finished
SHOW_BEST = False

# 1 means the genetic learning snakes will be displayed, a 0 means they won't be
HEADLESS = 1
NUM_WEIGHTS = NeuralNet(NUM_INPUTS, NUM_OUTPUTS,
                        NUM_HIDDEN, NUM_PER_HIDDEN).num_weights

class Genome:
    """
    Represents an individual in a population.
    In this case, the weights representing an individual neural net.
    """

    def __init__(self, weights=None, fitness=None):
        # Set weights
        if weights is None:
            self.weights = [(random.uniform(0, 1) * 2) -
                            1 for _ in range(NUM_WEIGHTS)]
        else:
            self.weights = weights

        self.fitness = fitness

    def copy(self):
        """
        Return deep copy of an individual.
        :return: a deep copy
        """
        copy = Genome(self.weights, None)
        return copy

    def get_fitness(self):
        """
        Returns the fitness of an individual genome. Calculates it once, then returns it when prompted again.
        :return: the genome's fitness
        """
        if self.fitness is None:
            self.recalculate_fitness()
        return self.fitness

    def recalculate_fitness(self):
        """
        Calculates the fitness  of an individual genome.
        """
        temp = []
        if DEBUGGING_FITNESS:
            print("NEW SNAKE")
        for i in range(FITNESS_ATTEMPTS):
            temp.append(Snake.fitness(self.weights, HEADLESS))
        self.fitness = sum(temp) / FITNESS_ATTEMPTS

    def __str__(self):
        """
        Pretty print the weights of the neural network.
        output = ""
        for i in range(len(self.ann.layers)):
            output += "Layer " + i + ": "
            for neuron in self.ann.layers[i].neurons:
                weights += neuron.weights
        """
        return self.weights

    def __gt__(self, other):
        return self.get_fitness() > other.get_fitness()

class GA:
    """
    Encapsulates the methods needed to solve an optimization problem using a genetic
    algorithm.
    """

    def __init__(self, num_weights, pop_size=POP_SIZE, num_gens=NUM_GENS, mut_rate=MUTATE_RATE, cross_rate=CROSS_RATE):
        """
        Initialize the genetic algorithm to interface to the ANN.
        :param pop_size: number of genomes per generation
        :param mut_rate: probability of mutation
        :param num_gens: number of generations to run
        :param cross_rate: crossover rate
        :param num_weights: the total number of weights in our neural net
        """
        # Problem parameters
        self.pop_size = pop_size
        self.num_gens = num_gens
        self.mut_rate = mut_rate
        self.cross_rate = cross_rate
        self.genome_length = num_weights

        # Current population descriptors
        self.total_fitness = 0
        self.best_fitness = 0
        self.avg_fitness = 0
        self.worst_fitness = 0
        self.best_genome = None


    @staticmethod
    def select(pop_subset, t): # This will not be used anymore
        """
        Implements tournament-style selection of the population.
        :param pop_subset: some subset of the population
        :param t: size of the tournament
        :return: fittest individual from some subset of the population.
        """
        assert t >= 1, "Need at least two individuals"
        """
        This was previously written, and didn't quite seem to do tournament style selection properly...
        At least it just seemed to do it in a weird way...
        best = pop_subset[random.randrange(0, len(pop_subset))]
        for i in range(1, t):
            next_ind = pop_subset[random.randrange(0, len(pop_subset))]
            if next_ind.get_fitness() > best.get_fitness():
                best = next_ind
        return best
        """
        # This instead selects the best individual from a randomly selected subset of the given population

        # Get a random selection...
        testPop = random.sample(pop_subset, t)
        # Return the best two from the random selection
        x1 = max(testPop)
        testPop.remove(x1)
        x2 = max(testPop)
        return x1, x2

    def mutate(self, genome):
        """
        Implements mutation, where weights may be changed.
        :param genome: genome in question
        :return: a reference to a new mutated Genome
        """
        options = [0.5,1,2,4,8,16,32]
        mutate_type = random.choice(options) / 100
        new_genome = genome.copy()
        weights = new_genome.weights
        for i in range(NUM_WEIGHTS):
            if self.mut_rate >= random.random():
                weights[i] += random.randrange(-1,2,2) * mutate_type * weights[i]  # add delta noise in [-1, 1]

        return new_genome

    def crossover(self, g1, g2):
        """
        Implement uniform crossover, given two parent individuals.
        Return two children constructed from the weights.
        :param g1: first parent
        :param g2: second parent
        :return: tuple containing two children sets of weights
        """
        c1 = g1.copy()
        c2 = g2.copy()

        assert (len(c1.weights) == len(c2.weights))

        for i in range(len(c1.weights)):
            if self.cross_rate >= random.random():
                temp = c1.weights[i]
                c1.weights[i] = c2.weights[i]
                c2.weights[i] = temp

        return c1

    def epoch(self, old_population):
        """
        Runs the GA for one generation, updating the population.
        :return: the new population
        """
        
        """
        This was the old algorithm, which didn't really work...

        # Generate next generation of individuals
        population_next = 0 * [None]
        for i in range(self.pop_size // 2):

            
            # Tournament select two parents from a random selection of TOURNAMENT_PERCENT percent of the current population
            p_a ,p_b = self.select(old_population, int(POP_SIZE * TOURNAMENT_PERCENT))

            # Create two children through uniform crossover
            (c_a, c_b) = self.crossover(p_a, p_b)

            # Add children to population pool for next gen
            population_next.append(self.mutate(c_a))
            population_next.append(self.mutate(c_b))
        
        # Override two weights with the current best (elitism)
        population_next[0] = self.best_genome.copy()
        population_next[1] = self.best_genome.copy()
        """

        # Generate new individuals using Kent's tournament algorithm
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
                    #print("The winner that was mutated successfully was found and replaced")
                else:
                    pass
                    #print("The winner that was mutated successfully was not found")
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
                    Snake.fitness(self.best_genome.weights, 0)
                """
                Include this in the if statement to show each of the fitness steps for the new snake.
                for x in range(16):
                     print(Snake.fitness(self.best_genome.weights, 0), end = " ")
                """

        if (SHOW_BEST):
            Snake.fitness(self.best_genome.weights, 0)

        # Record fitness value parameters
        self.avg_fitness = self.total_fitness / len(old_population)
        self.best_fitness = self.best_genome.get_fitness()

        return old_population


# Runs the GA for the ANN Snake problem
def main():
    # Calculate number of weights
    ga = GA(NUM_WEIGHTS)

    print("Number of hidden layers: " + str(NUM_HIDDEN))
    if NUM_HIDDEN > 0:
        print("Number of nodes per hidden layer: " + str(NUM_PER_HIDDEN))

    # Initialize a random population of neural nets
    # TODO: make this so we can seed the initial population with a starting network!
    population = ga.pop_size * [None]
    
    for i in tqdm(range(0, ga.pop_size), ascii = True, desc = "GENERATING INITIAL POPULATION"):
        population[i] = Genome()
        population[i].get_fitness()

    # Store best genome for each generation
    best_genomes = []

    in_a_row = 0
    prev_average = 0
    # Run for num_gens generations
    for i in range(ga.num_gens):
        # Call epoch at each step
        population = list(ga.epoch(population))
        best_genomes.append(ga.best_genome.weights)

        # Print population characteristics
        print("Gen " + str(i) + ": " + "best: " + str(ga.best_fitness) + \
              ", avg: " + str(ga.avg_fitness))
        if ga.avg_fitness == prev_average: # If the snake is just looping forever
           in_a_row += 1
           if in_a_row == 5:
                print(best_genomes[-1])
                main()
        else:
            in_a_row = 0
            prev_average = ga.avg_fitness

    # Output structure of fittest individual
    print(best_genomes[-1])


# Run the GA
if __name__ == '__main__':
    while True:
        main()