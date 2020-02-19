import main 
import random 
import time 
from settings import settings 
import numpy as np
import matplotlib.pyplot as plt

N = 250
def plotExperiment(N):
	population = main.generatePopulation(N=N, length=100) 
	oneCount = []
	generationCount = [] 

	for generation in range(0, settings["generations"]):
		if main.isGlobalOptimum(population):
			print("Optimum found at generation: ", generation)
			plt.plot(oneCount, generationCount) 
			plt.show 
			return

		totalOnes = 0 
		for individual in population: 
			totalOnes += main.countOnes(individual) 
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
				child1, child2 = main.uniformCrossover(parent1, parent2)
			else:
				child1, child2 = main.twoPointCrossover(parent1, parent2)
			
			# 4. Family competition: the best 2 solutions of each family of 4 are copied to the next population P(t + 1).
			fitness = {
				parent1: None,
				parent2: None,
				child1: None,
				child2: None
			}
			for individual in fitness.keys():
				if settings["fitnessFunction"] == "countOnes":
					fitness[individual] = main.countOnes(individual)
				elif settings["fitnessFunction"] == "linkedDeceptiveTF":
					fitness[individual] = main.linkedDeceptiveTF(individual)
				elif settings["fitnessFunction"] == "linkedDonDeceptiveTF":
					fitness[individual] = main.linkedNonDeceptiveTF(individual)
				elif settings["fitnessFunction"] == "deceptiveNonlinkedTF":
					fitness[individual] = main.deceptiveNonlinkedTF(individual)
				elif settings["fitnessFunction"] == "nonDeceptiveNonlinkedTF":
					fitness[individual] = main.nonDeceptiveNonlinkedTF(individual)
				else:
					print("No fitness function found!")
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
