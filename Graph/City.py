import numpy as np
from Journey import Journey

class City:
    def __init__(self, city_name):
        self.city_name = city_name
        self.journey_options = list()
        self.adjacent_nodes = list()
    
    def assing_journey_to_a_node(self,journey):
        self.journey_options.append(journey)
        
    def build_adjacent_node_list(self):
        for journey in self.journey_options:
            if journey.destination.city_name not in self.adjacent_nodes:
                self.adjacent_nodes.append(journey.destination.city_name)
                
      # self.y = y
        
    #def calc_distance(self, other_city):
    #    return np.sqrt(np.square(np.abs(self.x - other_city.x)) + np.square(np.abs(self.y - other_city.y)))

    # def set_uid(self, uid):
    #     self.UID = uid

    # def __str__(self):
    #     return "City_{}({}, {})".format(self.UID, self.x, self.y)
    
        