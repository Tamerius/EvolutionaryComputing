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

def calculateError (parent1, parent2, winner1, winner2): 
        if len(parent1) != len(parent2):
                print("parents not of same size!")
                return
        error = 0
        corr = 0
        for index in range(0, len(parent1)):
                if parent1[index]=="1" or parent2[index]=="1":
                        if winner1[index]=="0" and winner2[index]=="0":
                                error+=1
                        elif winner1[index]=="1" and winner2[index]=="1":
                                corr+=1
        return error, corr

def checkAverageSchemata (population):
        zeroSchemata = []
        oneSchemata = []
        zeroFitness = 0
        oneFitness = 0 
        for individual in population:
                if individual[0] == "0":
                        zeroSchemata.append(individual)
                else:
                        oneSchemata.append(individual)
        for individual in zeroSchemata:
                zeroFitness += optimizedCountOnes(individual)
        if (len(zeroSchemata) != 0):
                zeroFitness = zeroFitness/len(zeroSchemata)
        for individual in oneSchemata:
                oneFitness += optimizedCountOnes(individual)
        if (len(oneSchemata) != 0): 
                oneFitness = oneFitness/len(oneSchemata) 
        return zeroFitness, oneFitness

def checkSchemata (population):
        zeroSchemata = []
        oneSchemata = []
        zeroFitness = 0
        oneFitness = 0 
        for individual in population:
                if individual[0] == "0":
                        zeroSchemata.append(individual)
                else:
                        oneSchemata.append(individual)
        for individual in zeroSchemata:
                zeroFitness += optimizedCountOnes(individual)
        for individual in oneSchemata:
                oneFitness += optimizedCountOnes(individual)
        return zeroFitness, oneFitness 

def plotExperiment(N):
        population = generatePopulation(N=N, length=100) 
        oneCount = []
        generationCount = []
        errorCount = []
        correctionCount = []
        oneSchemataFitnessCount = []
        zeroSchemataFitnessCount = []
        relativeOneSchemataFitnessCount = []
        relativeZeroSchemataFitnessCount = []

        for generation in range(0, settings["generations"]):
                if isGlobalOptimum(population):
                        print("Optimum found at generation: ", generation)

                        relOneCount = []
                        for item in oneCount:
                                relOneCount.append(item / oneCount[len(oneCount) - 1]) 
                        y = np.asarray(relOneCount)
                        x = np.asarray(generationCount)

                        plt.ylabel('Relative fitness')
                        plt.xlabel('Generation')
                        plt.plot(x, y, label = 'Relative Fitness')
                        plt.legend() 
                        plt.show()

                        y1 = np.asarray(errorCount)
                        y2 = np.asarray(correctionCount) 

                        plt.xlabel('Generation')
                        plt.ylabel('Error/Correction')
                        label1 = 'Error'
                        label2 = 'Correction'
                        plt.plot(x, y1, '--r', x, y2, 'bs')
                        plt.legend((label1, label2)) 
                        plt.show()

                        meanOne = np.mean(relativeOneSchemataFitnessCount)
                        meanZero = np.mean(relativeZeroSchemataFitnessCount)

                        stdevOne = np.std(relativeOneSchemataFitnessCount)
                        stdevZero = np.std(relativeZeroSchemataFitnessCount)

                        fig = plt.figure(figsize=(10, 8))
                        ax = fig.add_subplot(111)
                        
                        ax.set_xlabel('Generation')
                        ax.set_ylabel('One/Zero Schemata Fitness')
                        
                        y1 = np.asarray(relativeOneSchemataFitnessCount)
                        y2 = np.asarray(relativeZeroSchemataFitnessCount)

                        colorOne = 'green'
                        colorZero = 'red'
                        lineStyleOne = {"linestyle":"--", "linewidth":2, "markeredgewidth":2, "elinewidth":2, "capsize":3}
                        lineStyleZero = {"linestyle":"--", "linewidth":2, "markeredgewidth":2, "elinewidth":2, "capsize":3}
                        lineOnes = ax.errorbar(x, y1, yerr=stdevOne, **lineStyleOne, color=colorOne, label='Relative One Schemata Fitness')
                        lineZeroes = ax.errorbar(x, y2, yerr=stdevZero, **lineStyleZero, color=colorZero, label='Relative Zero Schemata Fitness')

                        #for i, txt in enumerate(y1):   
                        #     ax.annotate(txt, xy=(x[i], y1[i]),
                        #                 xytext=(x[i]+0.03,y1[i]+0.3),
                        #                 color=colorOne) 
                        #for i, txt in enumerate(y2):        
                        #     ax.annotate(txt, xy=(x[i], y2[i]),
                        #                 xytext=(x[i]+0.03, y2[i]+0.3),
                        #                 color=colorZero)
                        
                        plt.legend(handles=[lineOnes, lineZeroes], loc='upper right')
                        plt.show()

                        meanOne = np.mean(oneSchemataFitnessCount)
                        meanZero = np.mean(zeroSchemataFitnessCount)

                        stdevOne = np.std(oneSchemataFitnessCount)
                        stdevZero = np.std(zeroSchemataFitnessCount)

                        fig = plt.figure(figsize=(10, 8))
                        ax = fig.add_subplot(111)
                        
                        ax.set_xlabel('Generation')
                        ax.set_ylabel('One/Zero Schemata Fitness')
                        
                        y1 = np.asarray(oneSchemataFitnessCount)
                        y2 = np.asarray(zeroSchemataFitnessCount)

                        colorOne = 'green'
                        colorZero = 'red'
                        lineStyleOne = {"linestyle":"--", "linewidth":2, "markeredgewidth":2, "elinewidth":2, "capsize":3}
                        lineStyleZero = {"linestyle":"--", "linewidth":2, "markeredgewidth":2, "elinewidth":2, "capsize":3}
                        lineOnes = ax.errorbar(x, y1, yerr=stdevOne, **lineStyleOne, color=colorOne, label='Average One Schemata Fitness')
                        lineZeroes = ax.errorbar(x, y2, yerr=stdevZero, **lineStyleZero, color=colorZero, label='Average Zero Schemata Fitness')

                        #for i, txt in enumerate(y1):   
                        #     ax.annotate(txt, xy=(x[i], y1[i]),
                        #                 xytext=(x[i]+0.03,y1[i]+0.3),
                        #                 color=colorOne) 
                        #for i, txt in enumerate(y2):        
                        #     ax.annotate(txt, xy=(x[i], y2[i]),
                        #                 xytext=(x[i]+0.03, y2[i]+0.3),
                        #                 color=colorZero)
                        
                        plt.legend(handles=[lineOnes, lineZeroes], loc='upper right')
                        plt.show() 
                        
                        return 

                totalOnes = 0
                totalError = 0
                totalCorrection = 0
                
                for individual in population: 
                        totalOnes += optimizedCountOnes(individual) 
                oneCount.append(totalOnes)
                generationCount.append(generation)

                averageZeroSchemataFitness, averageOneSchemataFitness = checkAverageSchemata (population) 
                zeroSchemataFitness, oneSchemataFitness = checkSchemata(population)
                relativeZeroSchemataFitnessCount.append(zeroSchemataFitness/N)
                relativeOneSchemataFitnessCount.append(oneSchemataFitness/N)
                oneSchemataFitnessCount.append(averageOneSchemataFitness)
                zeroSchemataFitnessCount.append(averageZeroSchemataFitness)
                

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

                        err, corr = calculateError(parent1, parent2, winner, secondWinner)

                        totalError += err
                        totalCorrection += corr
                        
                        winners += [winner, secondWinner]
                population = winners

                errorCount.append(totalError)
                correctionCount.append(totalCorrection)

        print(population) 


plotExperiment(N)
