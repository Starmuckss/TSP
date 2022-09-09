import numpy as np
from Journey import Journey

class City:
    def __init__(self, city_name):
        self.city_name = city_name
        self.journey_options = list()
        self.adjacent_nodes = list()
        self.city_lat = 0 
        self.city_lng = 0
    def assing_journey_to_a_node(self,journey):
        self.journey_options.append(journey)
        
    def build_adjacent_node_list(self):
        for journey in self.journey_options:
            if journey.destination.city_name not in self.adjacent_nodes:
                self.adjacent_nodes.append(journey.destination.city_name)
    
    def assign_city_location(self,lat,lng):
        self.city_lat = lat
        self.city_lng = lng
        
        
    def __str__(self):
        return self.city_name          
        