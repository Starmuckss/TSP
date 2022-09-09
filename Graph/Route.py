import numpy as np
import random
from datetime import datetime, timedelta
class Route:
    
    def __init__(self,source_node,cities_to_visit,tour_start_date,day_limit): # day limit, in what time the tour must be completed
        self.fitness = 0.0
        self.route_cost = 0.0
        self.source_node = source_node
        self.cities_to_visit = cities_to_visit
        self.route = list()
        self.route_current_time = tour_start_date
        self.route_finish_time = tour_start_date
        self.tour_deadline = tour_start_date + timedelta(days=day_limit)
        self.feasible = True
    
    def __str__(self):
        _str = "Route: "
        for i, v in enumerate(self.route):
            if i == len(self.route) - 1:
                _str += str(v)
            else:
                _str += str(v) + " --> "
        return _str    
    
    def generate_random_route(self):
        # Create a random route with the cities
        for city in self.cities_to_visit:
            self.route.append(city)
        random.shuffle(self.route)
        self.route.insert(0, self.source_node)
        self.route.append( self.source_node)
            
    def generate_route_from_list(self,cities_to_visit):
        for city in cities_to_visit:
            self.route.append(city)
        self.route.insert(0, self.source_node)
        self.route.append( self.source_node)

    def calc_route_cost(self): 
        if self.route_cost == 0:
            route_cost = 0
            for city_index in range(len(self.route) - 1):
                least_cost_journey = None
                least_cost = 99999
                for journey in self.route[city_index].journey_options:
                    if (journey.destination.city_name == self.route[city_index + 1].city_name and journey.travel_cost < least_cost 
                        and journey.start_time > self.route_current_time):
                        least_cost_journey = journey
                        least_cost = journey.travel_cost
                        self.route_current_time = journey.arrival_time
                        
                route_cost += least_cost # 99999 is a large number, the route will be automatically rejected
                if least_cost == 99999 or self.route_current_time > self.tour_deadline:
                    
                    self.feasible = False
            self.cost = route_cost
        self.route_finish_time = self.route_current_time
        
        return self.cost
    
    def calc_fitness(self):
        if self.fitness == 0:
            self.fitness = 1.0 / self.calc_route_cost()
        return self.fitness

    def get_city(self, idx):
        return self.route[idx]

    def assign_city(self, index, city):
        return None
    
    def __len__(self):
        return len(self.route)

    def __contains__(self, city):
        return city in self.route
    
    def check_route_is_valid(self): # A problem: What if I can reach next city in the route, but the I can't use the journey I use to reach there???
                                    # Current solution: If the cost of the journey is bigM, that means this happened. So, reject that route 
        # check if route is valid, ##it is valid if finishing time < travel limit
        # and if it is possible to follow this route 
        is_valid = True
        
        if self.route[0].city_name != self.source_node.city_name and self.route[-1].city_name != self.source_node.city_name:
            is_valid = False
        
        if is_valid:
            for city_index in range(len(self.route)):
                if city_index < len(self.route)-1:
                    if self.route[city_index+1].city_name not in self.route[city_index].adjacent_nodes:
                        #deny route
                        is_valid = False
                        break           
        
        # if self.route_finish_time > self.tour_deadline: 
        #     is_valid = False
        
        return is_valid
        
