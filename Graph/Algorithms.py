# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 14:42:20 2022

@author: HP
"""
from City import City
from Journey import Journey
from Route import Route
from itertools import permutations
from datetime import datetime, timedelta

def enumeration(cm,source_node,locations_to_travel):

    # Start the tour on this date 
    tour_start_date_string = '22/03/22 00:00:00' 
    tour_start_date = datetime.strptime(tour_start_date_string, '%d/%m/%y %H:%M:%S') 
    
    day_limit = 7 # Days     # Build candidate routes
    permutate_cities_to_visit = [list(r) for r in permutations(locations_to_travel)]
    candidate_routes = list()
    
    for perm in permutate_cities_to_visit:
        candidate_route = Route(source_node = source_node,cities_to_visit=locations_to_travel,tour_start_date=tour_start_date,day_limit=day_limit)
        candidate_route.generate_route_from_list(perm)
        if candidate_route.check_route_is_valid():    
            candidate_routes.append(candidate_route)
        
    total_costs = []
    best_cost = candidate_routes[0].calc_route_cost()
    best_route = candidate_routes[0]
    
    for route in candidate_routes:
        route_cost = route.calc_route_cost()
       
        
        # BU INFEASIBLE SENARYOLARI INCELE, SIKINTI NEREDE ACABA, BİR ŞEYİ YANLIŞ YAPTIN MI KONTROL ET!!!       
        if route.feasible:
            print(str(route),route_cost)
            
        else:
            print(str(route) + " is infeasible")
        
        if route_cost < best_cost and route.feasible:
            best_cost = route_cost
            best_route = route
             
            #print(route_cost,route)
            
    print("Best route is ",str(best_route),"with cost", str(best_cost))        
    return best_route          
        
# TODO: GENETIC ALGORITHM (Heuristic) Build one 