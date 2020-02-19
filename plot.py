import random 
import time 
from settings import settings 
import numpy as np
import matplotlib.pyplot as plt

N = 250

#Still no idea :^) 
def optimizedCountOnes(string):
        oneCounter = 0
        for char in string:
                oneCounter += char == "1"
        return oneCounter

def generateString(length):
        string = ""
        for index in range(0, length):
                string += "1" if random.random() < .5 else "0"
        return string

def generatePopulation(N, length):
        population = []
        for i in range(0, N):
                population.append(generateString(length))
        return population

def uniformCrossover(parent1, parent2):
        if len(parent1) != len(parent2):
                print("parents not of same size!")
                return
        child1 = ""
        child2 = ""
        for index in range(0, len(parent1)):
                if random.random() < .5:
                        child1 += parent1[index]
                        child2 += parent2[index]
                else:
                        child1 += parent2[index]
                        child2 += parent1[index]
        return child1, child2

def twoPointCrossover(parent1, parent2):
        if len(parent1) != len(parent2):
                print("parents not of same size!")
                return
        cutoffPoint1 = 0
        cutoffPoint2 = 0
        while cutoffPoint1 == cutoffPoint2:
                cutoffPoint1 = int(random.random() * len(parent1))
                cutoffPoint2 = int(random.random() * len(parent1))
        leftCutoffPoint = min(cutoffPoint1, cutoffPoint2)
        rightCutoffPoint = max(cutoffPoint1, cutoffPoint2)
        child1 = ""
        child2 = ""
        segment1 = range(0, leftCutoffPoint)
        segment2 = range(leftCutoffPoint, rightCutoffPoint)
        segment3 = range(rightCutoffPoint, len(parent1))
        for index in segment1:
                child1 += parent1[index]
                child2 += parent2[index]
        for index in segment2:
                child2 += parent1[index]
                child1 += parent2[index]
        for index in segment3:
                child1 += parent1[index]
                child2 += parent2[index]
        return child1, child2

def isGlobalOptimum(population):
        for individual in population:
                if "0" not in individual:
                        return True
        return False 

def plotExperiment(N):
        population = generatePopulation(N=N, length=100) 
        oneCount = []
        generationCount = [] 

        for generation in range(0, settings["generations"]):
                if isGlobalOptimum(population):
                        print("Optimum found at generation: ", generation)
                        print (generationCount) 
                        for item in oneCount:
                                oneCount[oneCount.index(item)] = item / oneCount[len(oneCount) - 1]
                        print (oneCount)
                        y = np.asarray(oneCount)
                        x = np.asarray(generationCount)

                        plt.ylabel('Average fitness')
                        plt.xlabel('Generation')
                        
                        plt.plot(x, y) 
                        plt.show() 
                        return 

                totalOnes = 0 
                for individual in population: 
                        totalOnes += optimizedCountOnes(individual) 
                oneCount.append(totalOnes)
                generationCount.append(generation) 

                # 1. Randomly shuffle the population P(t).
                random.shuffle(population)

                # 2. Pair solution 1 with solution 2, solution 3 with solution 4, etc. ...
                winners = []
                for parentIndex in range(0, len(population)):
                        if parentIndex % 2 == 0:
                                continue
                        parent1 = population[parentIndex - 1]
                        parent2 = population[parentIndex]

                        # 3. Each parent pair creates 2 offspring solutions using crossover.
                        if settings["uniformCrossover"]:
                                child1, child2 = uniformCrossover(parent1, parent2)
                        else:
                                child1, child2 = twoPointCrossover(parent1, parent2)
                        
                        # 4. Family competition: the best 2 solutions of each family of 4 are copied to the next population P(t + 1).
                        fitness = {
                                parent1: None,
                                parent2: None,
                                child1: None,
                                child2: None
                        }
                        for individual in fitness.keys():
                                fitness[individual] = optimizedCountOnes(individual)
                        # Find key (the individual) of the highest fitness
                        winner = max(fitness, key=fitness.get)
                        # iff the winner is a parent: check if there exists a child with the same fitness (to use this instead)
                        if winner in [parent1, parent2]:
                                if fitness[child1] == fitness[winner]:
                                        winner = child1
                                elif fitness[child2] == fitness[winner]:
                                        winner = child2
                        fitness[winner] = 0 # set to zero so we skip this for the second winner
                        secondWinner = max(fitness, key=fitness.get)
                        if secondWinner in [parent1, parent2]:
                                if fitness[child1] == fitness[secondWinner]:
                                        secondWinner = child1
                                elif fitness[child2] == fitness[secondWinner]:
                                        secondWinner = child2
                        winners += [winner, secondWinner]
                population = winners
        print(population) 


plotExperiment(N)
