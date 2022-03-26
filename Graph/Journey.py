# -*- coding: utf-8 -*-
"""
Created on Tue Mar 15 11:06:33 2022

@author: HP
"""
class Journey:
    def __init__(self, start, destination):
        self.start = start
        self.destination = destination
        
    def define_edge(self,start_time,arrival_time,travel_cost,travel_company,travel_type):
        self.start_time = start_time
        self.arrival_time = arrival_time
        self.travel_cost = travel_cost
        self.travel_company = travel_company
        self.travel_type = travel_type

        

    
                     