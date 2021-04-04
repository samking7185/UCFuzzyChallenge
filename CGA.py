import numpy as np
import random

from fuzzy_asteroids.fuzzy_asteroids import TrainerEnvironment
from controller import FuzzyController
from score import SampleScore


def processfitness(self, fitness):

    hits = fitness.asteroids_hit
    fired = fitness.bullets_fired
    time = fitness.time
    if fired == 0:
        fired = 1
    fitness_calc = hits * time / fired

    return fitness_calc


class CGA:
    def __init__(self, M, MaxGen, Pc, Pm, Er, n, UB, LB, vartype, settings):
        self.M = M
        self.MaxGen = MaxGen
        self.Pc = Pc
        self.Pm = Pm
        self.Er = Er
        self.n = n
        self.UB = UB
        self.LB = LB
        self.type = vartype
        self.BestGene = None
        self.Fitness = []
        self.Chromosome = self.initChromosome()
        game = TrainerEnvironment(settings=settings)
        self.game = game
        self.evolution()

    class initChromosome:
        def __init__(self):
            self.population = []
            self.newPopulation = None
            self.parent1 = None
            self.parent2 = None
            self.child1 = None
            self.child2 = None

    def evolution(self):
        self.initialization()
        # for idx in range(self.M):
        self.fitnessFunc(1)
        stopper = False
        for idxm in range(1, self.MaxGen):
            if stopper:
                break
            self.Chromosome.newPopulation = []
            for k in range(0, self.M, 2):

                self.selection()
                self.crossover()
                self.mutation()
                self.Chromosome.newPopulation.append([self.Chromosome.child1, 0])
                self.Chromosome.newPopulation.append([self.Chromosome.child2, 0])

            self.fitnessFunc(2)
            self.elitism()
            self.Fitness.append(self.Chromosome.population[0][1])

            # fitness_whole = [x[1] for x in self.Chromosome.population]
            print('------------------------------------')
            print('Generation: ' + str(idxm))
            print('------------------------------------')
            print('Fitness: ' + str(self.Chromosome.population[0][1]))
            if idxm % 10 == 0:
                print('------------ Current Best-----------------')
                print(self.Chromosome.population[0])
            # print(fitness_whole)
            # print('BestChrom ')
            # print(self.Chromosome.population[0][0])

            if idxm > 51:
                fit_check = self.Fitness[-50:]
                val_check = self.Fitness[-1:][0]
                stopper = all(x == val_check for x in fit_check)
                if stopper:
                    break

        # for idx in range(self.M):
        # self.Chromosome.population.sort(reverse=True, key=lambda x: x[1])
        # self.fitnessFunc(1)
        self.BestChrom = self.Chromosome.population[0]

    def fitnessFunc(self, fittype):
        game = self.game
        if fittype == 1:
            for idx in range(len(self.Chromosome.population)):
                gene = self.Chromosome.population[idx]
                pop_fitness = game.run(controller=FuzzyController(gene), score=SampleScore())
                fitness_score = processfitness(self, pop_fitness)
                self.Chromosome.population[idx][1] = fitness_score

        elif fittype == 2:
            for idx in range(len(self.Chromosome.newPopulation)):
                gene = self.Chromosome.newPopulation[idx]
                pop_fitness = game.run(controller=FuzzyController(gene), score=SampleScore())
                fitness_score = processfitness(self, pop_fitness)
                self.Chromosome.newPopulation[idx][1] = fitness_score

    def initialization(self):
        self.Chromosome.population = []
        for i in range(self.M):
            chromosome = []
            for idx, val in enumerate(self.n):
                if idx == 0:
                    gene = [-0.016246364446154682, -0.025565952540989922, -0.9539658434541948]
                elif idx == 1:
                    gene = [0.4649000608588642, 0.5085767386066072, 0.2892988027420131]
                elif idx == 4:
                    gene = [-32, -165, -87, -160, -37, -58, -77]
                elif idx == 5:
                    gene = [131, 102, 62, 21, 28, 127, 102]
                else:
                    gene = list(np.random.randint(self.LB[idx], self.UB[idx], size=self.n[idx]))
                # if self.type[idx] == 'int':
                #     gene = list(np.random.randint(self.LB[idx], self.UB[idx], size=self.n[idx]))
                # else:
                #     gene = list(np.random.uniform(self.LB[idx], self.UB[idx], size=self.n[idx]))
                chromosome.append(gene)
            self.Chromosome.population.append([chromosome, 0])
        self.Chromosome.population = self.Chromosome.population

    def selection(self):

        fitness = [x[1] for x in self.Chromosome.population]
        parents = random.choices(self.Chromosome.population, weights=fitness, k=2)
        self.Chromosome.parent1 = parents[0]
        self.Chromosome.parent2 = parents[1]

    def crossover(self):
        temp_parent1 = self.Chromosome.parent1[0]
        temp_parent2 = self.Chromosome.parent2[0]
        temp_child1 = [np.zeros_like(gene).tolist() for gene in temp_parent1]
        temp_child2 = [np.zeros_like(gene).tolist() for gene in temp_parent2]

        # Randomly choose between single point and more aggressive crossover
        # r_select = np.random.rand(1,1)
        # if r_select > 0.5:
        # Single Point Crossover

        idxm = np.random.randint(1, np.sum(self.n)) # Choose random index

        count = []
        flipped = 0
        idx = 0
        for (gene1, gene2) in zip(temp_parent1, temp_parent2):
            # Iterate through the list of genes and find the gene that includes
            # The crossover index

            count.append(len(gene1))
            if np.sum(count) < idxm:
                # List slicing for genes before crossover point
                temp_child1[idx] = gene1
                temp_child2[idx] = gene2

            elif np.sum(count) > idxm and flipped == 0:
                # List slicing for gene that contains crossover point
                temp_child1[idx] = gene1[:idxm] + gene2[idxm:]
                temp_child2[idx] = gene2[:idxm] + gene1[idxm:]
                flipped = 1

            else:
                # List slicing for genes after crossover point
                temp_child1[idx] = gene2
                temp_child2[idx] = gene1
            idx += 1
        # Check against probability of crossover
        r = np.random.rand(1,2)
        r = r[0]

        if r[0] <= self.Pc:
            self.Chromosome.child1 = temp_child1
        else:
            self.Chromosome.child1 = temp_parent1
        if r[1] <= self.Pc:
            self.Chromosome.child2 = temp_child2
        else:
            self.Chromosome.child2 = temp_parent2

        # Aggressive Crossover
        # This portion takes each individual gene and shuffles the values

        # idxm = np.random.randint(1,self.n) # Choose crossover point for each gene

        # for i, idx in enumerate(idxm):
        #     # List slicing for gene crossover
        #     temp_child1[i] = temp_parent1[i][0:idx] + temp_parent2[i][idx:]
        #     temp_child2[i] = temp_parent2[i][0:idx] + temp_parent1[i][idx:]

        # for idx in range(len(temp_parent1)):
        #     temp_child1[idx] = random.sample(temp_parent1[idx], len(temp_parent2[idx]))
        #     temp_child2[idx] = random.sample(temp_parent2[idx], len(temp_parent2[idx]))

        # Check against probability of crossover

        # r = np.random.rand(1, 2)
        # r = r[0]
        #
        # if r[0] <= self.Pc:
        #     self.Chromosome.child1 = temp_child1
        # else:
        #     self.Chromosome.child1 = temp_parent1
        # if r[1] <= self.Pc:
        #     self.Chromosome.child2 = temp_child2
        # else:
        #     self.Chromosome.child2 = temp_parent2

    def mutation(self):

        temp_child1 = self.Chromosome.child1
        temp_child2 = self.Chromosome.child2

        # Choose a random index and probability of mutation
        # For each gene
        r1 = np.random.rand(1, len(self.n))
        r1 = r1[0]
        idxm1 = np.random.randint(1, self.n)

        r2 = np.random.rand(1, len(self.n))
        r2 = r2[0]
        idxm2 = np.random.randint(1, self.n)

        valm1 = []
        valm2 = []

        # Generate an array of random mutations for "ints" and "floats"
        for i in range(len(idxm1)):
            if self.type[i] == 'int':
                valm1temp = np.random.randint(self.LB[i],self.UB[i])
                valm2temp = np.random.randint(self.LB[i],self.UB[i])

            else:
                valm1temp = np.random.uniform(self.LB[i],self.UB[i])
                valm2temp = np.random.uniform(self.LB[i],self.UB[i])
            valm1.append(valm1temp)
            valm2.append(valm2temp)
        idx = 0

        # Check probability of mutation for each gene
        # Mutate with values if lower than probability
        for (m1, m2) in zip(idxm1, idxm2):
            if r1[idx] < self.Pm:
                temp_child1[idx][m1] = valm1[idx]

            if r2[idx] < self.Pm:
                temp_child2[idx][m2] = valm2[idx]
            idx += 1
        self.Chromosome.child1 = temp_child1
        self.Chromosome.child2 = temp_child2

    def elitism(self):
        # This elitism function promotes a percentage of chromosomes based on the Er

        newPopulation2 = [[[],[]] for _ in range(len(self.Chromosome.population))]

        elite_no = round(np.multiply(self.M,self.Er))
        temp_population = self.Chromosome.population
        temp_population.sort(reverse=True, key=lambda x: x[1])
        temp_population2 = self.Chromosome.newPopulation
        temp_population2.sort(reverse=True, key=lambda x: x[1])

        newPopulation2[0:elite_no] = temp_population[0:elite_no]
        newPopulation2[elite_no:] = temp_population2[:-elite_no]

        temp_population3 = newPopulation2
        temp_population3.sort(reverse=True, key=lambda x: x[1])
        self.Chromosome.population = temp_population3
