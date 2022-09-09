from City import City
from CityManager import CityManager
import pandas as pd
import os
from Algorithms import enumeration
from scipy.spatial.distance import cdist
import numpy as np


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from tqdm import tqdm_notebook


from delivery import *

if __name__ == '__main__':
    
    otobus_data = pd.read_excel('otobus_data.xlsx')
    plane_data = pd.read_excel('plane_data.xlsx')
    
    main_data = pd.concat([otobus_data,plane_data])
    main_data = main_data.replace('antakya_hatay', 'hatay')

    
    cm = CityManager()
    cm.build_country(main_data)
    
    # Define source node
    source_node = list(cm.city_list)[0]
    
    # Define locations the salesman will go (improvement: Do this Randomly)
    locations_to_travel = list(cm.city_list)[1:4]
    

    #Reinforcement Learning
    #env = DeliveryEnvironment(n_stops = 10)
    
    env = DeliveryEnvironment(cities = cm.city_list,method = "cost",main_data = main_data , max_box = 10)
    env.render()
    
    
    
        