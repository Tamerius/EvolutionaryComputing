import main 
import random 
import time 
from settings import settings 

def mainExperiment(N):
	population = main.generatePopulation(N=N, length=100)
	for generation in range(0, settings["generations"]):
		if main.isGlobalOptimum(population):
			print("Optimum found at generation: ", generation, population)
			return 

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
					fitness[individual] = main.linkedDonDeceptiveTF(individual)
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

#With N, we want to: 
# 1. Experiment 1: Counting Ones Function. Run 2 experiments each with a diﬀerent crossover operator: 2X and UX.
# 2. Experiment 2: Deceptive Trap Function (tightly linked). Run 2 experiments each with a diﬀerent crossover operator: 2X and UX.
# 3. Experiment 3: Non-deceptive Trap Function (tightly linked). Run 2 experiments each with a diﬀerent crossover operator: 2X and UX.
# 4. Experiment 4: Deceptive Trap Function (not linked). Run 2 experiments each with a diﬀerent crossover operator: 2X and UX.
# 5. Experiment 5: Non-deceptive Trap Function (not linked). Run 2 experiments each with a diﬀerent crossover operator: 2X and UX.
N = main.findN() 
start_time = time.time() 
mainExperiment(N) 
elapsed_time = time.time() - start_time 
print ("Finished in ", elapsed_time, " seconds.") 
