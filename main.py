import random
from settings import settings

def countOnes(string):
	oneCounter = 0
	for char in string:
		oneCounter += char == "1"
	return oneCounter

def linkedDeceptiveTF(string):
	def B(substring):
		ones = countOnes(substring)
		if ones == len(substring):
			return len(substring)
		else:
			return len(substring) - (ones + 1)

	# split up string into four parts
	results = 0
	for index in range(0, int(len(string) / 4)):
		substring = string[index * 4 : (index * 4) + 4]
		results += B(substring)
	return results

def linkedNonDeceptiveTF(string):
	def B(substring):
		ones = countOnes(substring)
		if ones == len(substring):
			return len(substring)
		else:
			return (len(substring) - (ones + 1)) / 2

	# split up string into four parts
	results = 0
	for index in range(0, int(len(string) / 4)):
		substring = string[index * 4 : (index * 4) + 4]
		results += B(substring)
	return results

def deceptiveNonlinkedTF(string):
	results = []
	for offset in range(0, int(len(string) / 4)):
		cutoffIndices = [
			0 + offset,
			int(len(string) / 4 + offset),
			int(len(string) / 2 + offset),
			int((len(string) / 4) * 3 + offset)]
		newString = []
		for cutoffIndex in cutoffIndices:
			newString += string[cutoffIndex]
		results.append(linkedDeceptiveTF(newString))
	return results

def nonDeceptiveNonlinkedTF(string):
	results = []
	for offset in range(0, int(len(string) / 4)):
		cutoffIndices = [
			0 + offset,
			int(len(string) / 4 + offset),
			int(len(string) / 2 + offset),
			int((len(string) / 4) * 3 + offset)]
		newString = []
		for cutoffIndex in cutoffIndices:
			newString += string[cutoffIndex]
		results.append(linkedNonDeceptiveTF(newString))
	return results

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
		if "0" in individual:
			return False
	return True

def findN():
	Ns = [10]

	# search until 1280
	while Ns[len(Ns) - 1] < 1280:
		print(Ns[len(Ns) - 1])
		# double after every unreliable result
		while not checkReliability(Ns=Ns):
			Ns.append(Ns[len(Ns) - 1] * 2)
		else:
			# only take steps of 10
			while Ns[len(Ns) - 1] % 10 == 0:
				if checkReliability(Ns=Ns):
					if Ns[len(Ns) - 1] < Ns[len(Ns) - 2]:
						Ns.append((Ns[len(Ns) - 1] + Ns[len(Ns) - 3]) / 2)
					else:
						Ns.append((Ns[len(Ns) - 1] + Ns[len(Ns) - 2]) / 2)
				else:
					if Ns[len(Ns) - 1] < Ns[len(Ns) - 2]:
						Ns.append((Ns[len(Ns) - 1] + Ns[len(Ns) - 2]) / 2)
					else:
						Ns.append((Ns[len(Ns) - 1] + Ns[len(Ns) - 3]) / 2)
			print("Stopped at N=", Ns[len(Ns) - 1])
			return Ns[len(Ns) - 1]
	else:
		print("Report FAIL. Global optimum not found with size 1280.")
		return "Fail"


def checkReliability(Ns):
	N = Ns[len(Ns) - 1]
	optima = 0
	for iteration in range(0, 25):
		population = evolve(N=N)
		if isGlobalOptimum(population):
			optima += 1
	print(Ns)
	return optima >= 24

# Generate a population of size N and evolve it.
def evolve(N):
	population = generatePopulation(N=N, length=100)
	for generation in range(0, settings["generations"]):
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
				if settings["fitnessFunction"] == "countOnes":
					fitness[individual] = countOnes(individual)
				elif settings["fitnessFunction"] == "linkedDeceptiveTF":
					fitness[individual] = linkedDeceptiveTF(individual)
				elif settings["fitnessFunction"] == "linkedDonDeceptiveTF":
					fitness[individual] = linkedDonDeceptiveTF(individual)
				elif settings["fitnessFunction"] == "deceptiveNonlinkedTF":
					fitness[individual] = deceptiveNonlinkedTF(individual)
				elif settings["fitnessFunction"] == "nonDeceptiveNonlinkedTF":
					fitness[individual] = nonDeceptiveNonlinkedTF(individual)
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
		# print(generation, "/", settings["generations"])
		population = winners
	# print("\n Final population with N=", str(N), ":")
	# print(population)
	return population

findN()