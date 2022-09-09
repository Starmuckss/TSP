# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 17:33:34 2022

@author: HP
"""
"""
TODO
best route u biliyoruz fakat bu rotada hangi yolculukları yaptığımızı bilmiyoruz, bunu bul // Sonda bakmak daha mantıklı, bunu yapmanın doğru yolu bu gibi
-- Sıfırdan her route un yaptığı journey'leri tutmak hem maliyetli, hem de şu an için bu kodda mümkün gözükmüyor. En son en iyi route u bulduktan sonra cost u minimize eden ve time limit'e
uyan bir çözümü return etmek mantıklı
time limit koymadım, time limit eklemem gerekli, time limit varken nasıl rota seçeceğiz?
#milad.elyasi@ozu.edu.tr #milad.elyasi@ozyegin.edu.tr
Matematik modeli yaz Network olarak ya da integer olarak
Bundan sonra machine learning ve birden fazla gezgin
"""
##ÇALIŞMIYOR ŞU AN, BEST ROUTE YANLIŞ!!!!

from datetime import datetime,timedelta
import numpy as np, random, operator, pandas as pd, matplotlib.pyplot as plt
from City import City
from CityManager import CityManager

dir_path = os.path.dirname(os.path.realpath(__file__))
output_directory = dir_path + "\\data"  # Data will be printed out here

otobus_data = pd.read_excel(output_directory+'\\otobus_data.xlsx')
plane_data = pd.read_excel(output_directory+'\\plane_data.xlsx')

# Concat the 2 datas, bus and plane travel datas
main_data = pd.concat([otobus_data,plane_data])

# Drop empty rows: no travel option between 2 cities. ,
main_data = main_data.dropna()

# Start the tour on this date 
tour_start_date_string = '22/03/22 00:00:00' 
tour_start_date = datetime.strptime(tour_start_date_string, '%d/%m/%y %H:%M:%S') 

tour_time_limit = 7 # Days 
tour_end_date_limit = tour_start_date + timedelta(days=tour_time_limit)

#Build the country
cm = CityManager()
cm.build_country(main_data)

source_node = cm.city_list[0] # Select source node, the first one on the city list taken here

# cities_to_visit = cm.build_to_be_visited(cm.city_list, 5)
cities_to_visit = cm.to_be_visited_by_name(["adana","bursa","ankara","antalya","balikesir"]) # cities to be visited in tour

class Fitness:
    def __init__(self,route):
        self.route = route
        self.distance = 0 
        self.fitness = 0.0
        self.route_current_time = tour_start_date
        self.route_finish_time = tour_start_date
    def routeDistance(self):
        if self.distance == 0:
            pathDistance = 0
            for city_index in range(len(self.route) - 1):
                least_cost_journey = None
                least_cost = 9999
                for journey in self.route[city_index].journey_options:
                    if (journey.destination.city_name == self.route[city_index + 1].city_name and journey.travel_cost < least_cost 
                        and journey.start_time > self.route_current_time):
                        least_cost_journey = journey
                        least_cost = journey.travel_cost
                        self.route_current_time = journey.arrival_time
                            
                #pathDistance += least_cost_journey.travel_cost
                pathDistance += least_cost # 9999 is a large number, the route will be automatically rejected
            self.distance = pathDistance
        self.route_finish_time = self.route_current_time
        return self.distance
                
    def routeFitness(self):
        if self.fitness == 0:
            self.fitness = 1 / float(self.routeDistance())
        return self.fitness
    
    def getFinishTime(self):
        return self.route_finish_time        

def checkRouteIsValid(route):
    # check if route is valid, ##it is valid if finishing time < travel limit
    # and if it is possible to follow this route 
    isValid = True
    
    if route[0].city_name != source_node.city_name and route[-1].city_name != source_node.city_name:
        isValid = False
    
    if isValid:
        for city_index in range(len(route)):
            if city_index < len(route) -1:
                if route[city_index+1].city_name not in route[city_index].adjacent_nodes:
                    #deny route
                    isValid = False
                    break           
    
    if Fitness(route).getFinishTime() > tour_end_date_limit :
        isValid = False
    
    return isValid

def createRoute(cities_to_visit,source_node): 
    route = random.sample(cities_to_visit, len(cities_to_visit))
    route.insert(0, source_node)
    route.append(source_node)
    return route

def initialPopulation(popSize, cities_to_visit):
    population = []
    size = 0
    try_count = 0
    while try_count < 1000 and size <= popSize:
        candidate_route = createRoute(cities_to_visit,source_node)
        if checkRouteIsValid(candidate_route):
            population.append(candidate_route)
            size += 1
        try_count += 1    
    print(size) ## !!!! 
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

    child = childP2[:startGene] + childP1 + childP2[startGene:]

    # for i in child:
    #     print(i.city_name,end= "->")
    #     if i == child[-1]:
    #         print("")
    return child    

def breedPopulation(matingpool, eliteSize):
    children = []
    length = len(matingpool) - eliteSize
    pool = random.sample(matingpool, len(matingpool))

    for i in range(0,eliteSize):
        children.append(matingpool[i])
    
    for i in range(0, length):
        while True:
            child = breed(pool[i], pool[len(matingpool)-i-1])
            if checkRouteIsValid(child):
                children.append(child)
                break    
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
        if checkRouteIsValid(mutatedInd):

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
    ranked_routes = rankRoutes(pop)
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
        print(route)
def print_route(route):                                  
    for city_index in range(len(route)):
        print(route[city_index].city_name, end = "-> " )
        if city_index == len(route) - 1:
            print("")                                                                                                    #500
best_route = geneticAlgorithm(population=cities_to_visit, popSize=30, eliteSize=20, mutationRate=0.01, generations=20)
#geneticAlgorithmPlot(population = cities_to_visit, popSize=30, eliteSize=20, mutationRate=0.01, generations=20)

#%%


#GEÇİCİ
best_route_journeys = []
pathDistance = 0
best_route_current_time = tour_start_date
for city_index in range(len(best_route) - 1):
    least_cost_journey = None
    least_cost = 9999
    for journey in best_route[city_index].journey_options:
        if (journey.destination.city_name == best_route[city_index + 1].city_name and journey.travel_cost < least_cost 
            and journey.start_time > best_route_current_time):
            least_cost_journey = journey
            least_cost = journey.travel_cost
            best_route_current_time = journey.arrival_time
                
    #pathDistance += least_cost_journey.travel_cost
    pathDistance += least_cost # 9999 is a large number, the route will be automatically rejected
    best_route_journeys.append(least_cost_journey)

for journey in best_route_journeys:
    print(journey.start.city_name)

import networkx as nx

G = nx.Graph()


for city in cm.city_list:
    G.add_node(city.city_name)

for edge in best_route_journeys:
    G.add_edge(edge.start.city_name,edge.destination.city_name)
    
nx.draw(G, with_labels=True, font_weight='bold')


