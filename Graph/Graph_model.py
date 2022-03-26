# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 13:09:55 2022

@author: HP
"""
import networkx as nx
import pandas as pd
from itertools import permutations

otobus_data = pd.read_excel('otobus_data.xlsx')
plane_data = pd.read_excel('plane_data.xlsx')
main_data = pd.concat([otobus_data,plane_data])

G = nx.from_pandas_edgelist(main_data,
                            source = 'from',
                            target = 'destination',
                            edge_attr = ['price','company',"departure_time","arrival_time","journey_type"])
nx.draw(G)


# put a time limit for travel.
time_limit = None


        
        
