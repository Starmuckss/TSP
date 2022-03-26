# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 14:42:20 2022

@author: HP
"""
from City import City
from Journey import Journey
from itertools import permutations
def enumeration(cm,source_node,locations_to_travel):

    # Build candidate routes
    candidate_routes = [list(r) for r in permutations(locations_to_travel)]
    for i in candidate_routes:
        i.insert(0,source_node)
        i.append(source_node)
    best_route_cost = 99999
    best_route = None
    for route in candidate_routes:
        route_cost = 0
        for city_index in range(len(route)):
            
            least_cost = 9999
            for journey in route[city_index].journey_options:
                try:
                    if (journey.destination == route[city_index + 1] and journey.travel_cost < least_cost):
                        least_cost_journey = journey
                        least_cost = journey.travel_cost
                except IndexError:
                    break
                    
            route_cost += least_cost_journey.travel_cost        
            

        if(route_cost < best_route_cost):
            best_route_cost = route_cost
            best_route = route             
    
    for city in best_route:
        print(city.city_name, end = "-> ")
    print(best_route_cost)    