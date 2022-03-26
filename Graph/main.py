from City import City
from CityManager import CityManager
from RouteManager import RouteManager
from GeneticAlgorithmSolver import GeneticAlgorithmSolver
import pandas as pd
import os
from itertools import permutations
from Algorithms import enumeration

# ENUMERATION APPROACH



# if __name__ == '__main__':
    
#     otobus_data = pd.read_excel('otobus_data.xlsx')
#     plane_data = pd.read_excel('plane_data.xlsx')
    
    
#     main_data = pd.concat([otobus_data,plane_data])
    
#     cm = CityManager()
#     cm.build_country(main_data)
    
#     # Define source node
#     source_node = list(cm.city_list)[0]
    
#     # Define locations the salesman will go (improvement: Do this Randomly)
#     locations_to_travel = list(cm.city_list)[1:9]
    
#     enumeration(cm,source_node,locations_to_travel)
    
    
#     # rm = RouteManager(cm, 50)

#     # print(rm.find_best_route().calc_route_distance())

#     # gas = GeneticAlgorithmSolver(cm, 50)
#     # rm = gas.solve(rm)

#     # print(rm.find_best_route().calc_route_distance())
#     # print(rm.find_best_route())
