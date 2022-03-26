# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:33:34 2022

@author: HP
"""
# Assume time limit is endless for now 
#imports and Data loading

from datetime import datetime
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
from City import City
from CityManager import CityManager
    
otobus_data = pd.read_excel('otobus_data.xlsx')
plane_data = pd.read_excel('plane_data.xlsx')

main_data = pd.concat([otobus_data,plane_data])
main_data = main_data.dropna() # Drop empty rows: no travel option between 2 cities. 

#%%
tour_start_date_string = '22/03/22 00:00:00'
tour_start_date = datetime.strptime(tour_start_date_string, '%d/%m/%y %H:%M:%S')

cm = CityManager()
cm.build_country(main_data)
source_node = cm.city_list[0]

# cities_to_visit = cm.build_to_be_visited(cm.city_list, 5)
cities_to_visit = cm.to_be_visited_by_name(["adana","bursa","ankara"])

class Fitness:
    def __init__(self,route):
        self.route = route
        self.distance = 0 
        self.fitness = 0.0
        self.route_current_time = tour_start_date
    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for city_index in range(len(self.route)):
                #least_cost_journey = self.route[city_index].journey_options[0]
                least_cost = 99999
                for journey in self.route[city_index].journey_options:
                    try:
                        if (journey.destination.city_name == self.route[city_index + 1].city_name and journey.travel_cost < least_cost 
                            and journey.start_time > self.route_current_time):
                            least_cost_journey = journey
                            least_cost = journey.travel_cost
                            self.route_current_time = journey.arrival_time
                    except IndexError:
                        break
                   
                #pathDistance += least_cost_journey.travel_cost
                pathDistance += least_cost # 9999 is a large number, the route will be automatically rejected
            self.distance = pathDistance
        return self.distance
                
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
    def checkRouteIsValid(self):
        pass # check if route is valid, it is valid if finishing time < travel limit
def createRoute(cities_to_visit,source_node): 
    
    route = random.sample(cities_to_visit, len(cities_to_visit))
    route.insert(0, source_node)
    route.append(source_node)
    # Instead of checking with for loop,make a destinations list for each node
    #Check if route is possible!!
    
    for city_index in range(len(route)):
        if city_index < len(route) -1:
            if route[city_index+1].city_name not in route[city_index].adjacent_nodes:
                #deny route
                route = None
                break
    return route

def initialPopulation(popSize, cities_to_visit):
    population = []
    size = 0
    try_count = 0
    while try_count < 1000 and size <= popSize:
        candidate_route = createRoute(cities_to_visit,source_node)
        if isinstance(candidate_route, list):
            population.append(createRoute(cities_to_visit,source_node))
            size += 1
        try_count += 1    
    print(size)
    print_population(population)
    return population
        
def rankRoutes(population):
    fitnessResults = {}
    for i in range(0,len(population)):
        fitnessResults[i] = Fitness(population[i]).routeFitness()
    return sorted(fitnessResults.items(), key = operator.itemgetter(1), reverse = True)
        
def selection(popRanked, eliteSize):
    selectionResults = []
    df = pd.DataFrame(np.array(popRanked), columns=["Index","Fitness"])
    df['cum_sum'] = df.Fitness.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Fitness.sum()
    
    for i in range(0, eliteSize):
        selectionResults.append(popRanked[i][0])
    for i in range(0, len(popRanked) - eliteSize):
        pick = 100*random.random()
        for i in range(0, len(popRanked)):
            if pick <= df.iat[i,3]:
                selectionResults.append(popRanked[i][0])
                break
    return selectionResults   

def matingPool(population, selectionResults):
    matingpool = []
    for i in range(0, len(selectionResults)):
        index = selectionResults[i]
        matingpool.append(population[index])
    return matingpool

def breed(parent1, parent2):
    child = []
    childP1 = []
    childP2 = []
    
    geneA = int(random.random() * len(parent1)-1) + 1
    geneB = int(random.random() * len(parent1)-1) + 1 # +1's are from me. Don't touch the starting node
    
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
        
    childP2 = [item for item in parent2 if item not in childP1]

    child = childP1 + childP2
    
    return child    

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        child = breed(pool[i], pool[len(matingpool)-i-1])
        children.append(child)
    return children

def mutate(individual, mutationRate):
    for swapped in range(len(individual)):
        if(random.random() < mutationRate):
            swapWith = int(random.random() * len(individual))
            
            city1 = individual[swapped]
            city2 = individual[swapWith]
            
            individual[swapped] = city2
            individual[swapWith] = city1
    return individual

def mutatePopulation(population, mutationRate):
    mutatedPop = []
    
    for ind in range(0, len(population)):
        mutatedInd = mutate(population[ind], mutationRate)
        mutatedPop.append(mutatedInd)
    return mutatedPop

def nextGeneration(currentGen, eliteSize, mutationRate):
    popRanked = rankRoutes(currentGen)
    selectionResults = selection(popRanked, eliteSize)
    matingpool = matingPool(currentGen, selectionResults)
    children = breedPopulation(matingpool, eliteSize)
    nextGeneration = mutatePopulation(children, mutationRate)
    return nextGeneration

def geneticAlgorithm(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    print("Initial distance: " + str(1 / rankRoutes(pop)[0][1]))
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
    
    print("Final distance: " + str(1 / rankRoutes(pop)[0][1]))
    bestRouteIndex = rankRoutes(pop)[0][0]
    bestRoute = pop[bestRouteIndex]
    return bestRoute

def geneticAlgorithmPlot(population, popSize, eliteSize, mutationRate, generations):
    pop = initialPopulation(popSize, population)
    progress = []
    progress.append(1 / rankRoutes(pop)[0][1])
    
    for i in range(0, generations):
        pop = nextGeneration(pop, eliteSize, mutationRate)
        progress.append(1 / rankRoutes(pop)[0][1])
    
    plt.plot(progress)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.show()

def print_population(pop):
    for route in pop:
        for city in route:
            print(city.city_name, end = "-> " )
        
#geneticAlgorithm(population=cm.city_list, popSize=100, eliteSize=20, mutationRate=0.01, generations=500)
geneticAlgorithmPlot(population = cities_to_visit, popSize=30, eliteSize=20, mutationRate=0.01, generations=20)