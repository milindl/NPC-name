
'''
This is a genetic algorithm to generate names _close_ to the given name
But sufficiently different to be used as NPC names :)
'''

import name_matcher as nm
import numpy as np

# Configuration
SEED_NAME = ['au', 'l', 'i','v','^', 'r']
CROSSOVER_RATE = 0.7
MUTATION_RATE = 0.05
POPULATION_SIZE = 400
GAP_PENALTY = 0.15

class GeneticAlgorithm:
    '''
    GeneticAlgorithm is a class for a non-binary genetic algorithm to find names similar to the SEED_NAME
    '''
    def __init__(self, crossover_rate, mutation_rate, population_size, chromosome_size_range, fitness, rank_selection=True):
        '''
        __init__(crossover_rate, mutation_rate, population_size, chromosome_size_range, fitness)
        
        crossover_rate: a float [0,1] denoting the chance of a crossover
        mutation_rate: a float [0,1] denoting the chance of a mutation
        population_size: the size of the chromosome population; keep large for a larger variety of names, decrease the mutation rate etc accordingly
        chromosome_size_range: [] containing integers denoting possible sizes of the output
        fitness: a function that, when given a chromosome as input, returns its fitness(an arbitrary number denoting how suitable a chromosome is for the task at hand)
        '''
        self.fitness = fitness
        self.cr = crossover_rate
        self.mr = mutation_rate
        self.population = []
        self.fitnesses = []

        self.selection = self.__weighted_random_choice
        if rank_selection:
            self.selection = self.__rank_selection

        # Initialize initial random pool of chromosomes
        for i in range(population_size):
            size = chromosome_size_range[np.random.randint(len(chromosome_size_range))]
            chromo = []
            for j in range(size):
                g = np.random.randint(0,44)
                chromo.append(g)
            self.population.append(chromo)
            self.fitnesses.append(0)
        self.evaluate_fitness()
        # print(self.population)

    # To move a generation ahead, the following steps need to be performed:
    # Generate new chromosomes based on roulette wheel selection
    ## This is dealt with by mate() and __weighted_random_choice()
    # Mutate said chromosomes
    ## This is dealt with by mutate()
    # Evaluate fitnesses
    ## This is dealt with by evaluate_fitness()
    # Terminate if fitness over threshold, else continue the cycle
    # The main_loop is responsible for looping thru generations and termination

    def main_loop(self, generations = 1000000, fitness_thresh = 99):
        '''
        main_loop(generation = 1000000, fitness_thresh = 99)
        generation: maximum generation to go up till
        fitness_thresh: if max {fitnesses} is over this, terminate

        Main loop goes about incrementing generations until atleast one of the above conditions is met.
        '''
        
        gencount = 0
        fitness_max = 0
        while gencount<generations and fitness_max<fitness_thresh:
            gencount += 1
            print(gencount)
            self.mate()
            self.mutate()
            self.evaluate_fitness()
            fitness_max = max(self.fitnesses)
            print(fitness_max)

        
    def __weighted_random_choice(self):
        '''
        __weighted_random_choice() -> chromosome []
        Implement roulette wheel selection.
        From stackoverflow, almost word to word
        '''
        max = sum(self.fitnesses)
        pick = np.random.uniform(0, max)
        current = 0
        for i in range(len(self.population)):
            current += self.fitnesses[i]
            if current > pick:
                return self.population[i]

    def __rank_selection(self):
        '''
        __rank_selection() -> chromosome []
        Implement rank selection
        '''
        n = len(self.population)
        sumn = (n * (n + 1)) / 2
        arr = np.arange(1, n + 1) / sumn
        ind = np.argmax(np.random.multinomial(1, arr))
        pop = np.partition(self.fitnesses, ind)[ind]
        return self.population[np.where(self.fitnesses == pop)[0][0]]

    def mutate(self):
        '''
        mutate()
        This method mutates EACH IPA in the chromosome with an equal probability given by the mutation_rate
        '''
        for chromo in self.population:
            for i in range(len(chromo)):
                if(np.random.uniform(0,1) < self.mr):
                    chromo[i] = np.random.randint(0,44)

    def mate(self):
        '''
        mate()
        This makes the generation move forward, by generating N daughter chromosomes from N mother chromosomes.
        Crossing over is done depending on the crossover rate
        '''
        new_pop = []
        for i in range(len(self.population)):
            chromo = self.selection()
            chromo2 = chromo
            if np.random.uniform(0,1) < self.cr:
                chromo2 = self.selection()
            new_chromo = []
            crossover = np.random.randint(min(len(chromo), len(chromo2)))
            new_chromo_length = len(chromo[:crossover]) + len(chromo2[crossover:])
            for x in range(new_chromo_length):
                if x<crossover:
                    new_chromo.append(chromo[x])
                else:
                    new_chromo.append(chromo2[x])

            new_pop.append(new_chromo)
        self.population = new_pop
        
    
    def evaluate_fitness(self):
        '''
        evaluate_fitness()
        Set the values in fitnesses to the correct values computed by the fitness function
        '''
        for i in range(len(self.population)):
            self.fitnesses[i] = self.fitness(self.population[i])




# Testing/running code starts here

n_m = nm.NameMatcher('comparison_matrix', GAP_PENALTY)
def fn(string):
    converted_string = [nm.symlist[i] for i in string]
    return n_m.match(SEED_NAME, converted_string)*2/(len(converted_string) + len(SEED_NAME))
                
    

def gaTest():
    s_len = len(SEED_NAME)
    ga = GeneticAlgorithm(CROSSOVER_RATE, MUTATION_RATE, POPULATION_SIZE, [s_len-1, s_len, s_len+1], fn, rank_selection=True)
    ga.main_loop(fitness_thresh = 0.90)
    for i in range(len(ga.population)):
        converted_string = [nm.symlist[j] for j in ga.population[i]]
        if ga.fitnesses[i] >= 0.8:
            print(ga.fitnesses[i], end = ' : ')
            print(' '.join(converted_string))


if __name__ == '__main__':
    gaTest()

