from City import City
from Journey import Journey
import random
class CityManager:
    def __init__(self):
        self.city_list = list()
        self.city_names = list()
        self.all_journeys = list()
    def add(self, city):
        self.city_list.append(city)


    def __getitem__(self, index):
        return self.city_list[index]

    def __len__(self):
        return len(self.city_list)
    
    
        
    def build_country(self,dataframe):
        for _,row in dataframe.iterrows():
            # Add Cities to the city_list
            city_1 = City(row['from'])
            if row['from'] not in self.city_names:
                
                self.city_list.append(city_1)
                self.city_names.append(row['from'])
                
            city_2 = City(row['destination'])
            if row['destination'] not in self.city_names:
                
                self.city_list.append(city_2)
                self.city_names.append(row['destination'])
            
            journey = Journey(city_1,city_2)
            journey.define_edge(row['departure_time'], row['arrival_time'], row['price'], row['company'], row['journey_type'])
            self.all_journeys.append(journey)
        
        for city in self.city_list:
            for journey in self.all_journeys:
                if journey.start.city_name == city.city_name:
                    city.assing_journey_to_a_node(journey)
        for city in self.city_list:
            city.build_adjacent_node_list()
    def build_to_be_visited(self,city_list,number_of_cities):
        random.seed(42)        
        cities_to_visit = random.sample(city_list[1:], number_of_cities)
        return cities_to_visit
    
    def to_be_visited_by_name(self,city_list):
        cities_to_visit= list()
        for city_name in city_list:
            for city in self.city_list:
                if city_name == city.city_name:
                    cities_to_visit.append(city)
        return cities_to_visit            