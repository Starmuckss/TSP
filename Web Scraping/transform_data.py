# -*- coding: utf-8 -*-
"""
Created on Sun Mar  6 22:39:01 2022

@author: HP
"""
import pandas as pd
import os
import regex as re

def travel_time_to_hours(column): # Use regex
    travel_time_in_hours = []
    for s in column:
        
        time_in_hours = 0
        if pd.notna(s):
            gun_index = s.find('Gün')
            if gun_index != -1:

                if gun_index>2:
                    gun_part = s[gun_index-3:gun_index-1]
                else:
                    gun_part = s[gun_index-2:gun_index-1]
                time_in_hours += int(gun_part)*24
                    
        
            saat_index = s.find('Saat')
            if saat_index != -1:
                if saat_index>2:
                    saat_part = s[saat_index-3:saat_index-1]
                else:
                    saat_part = s[saat_index-2:saat_index-1]
                time_in_hours += int(saat_part)

        
            dakika_index = s.find('Dakika')
            if dakika_index != -1:
                if dakika_index>2:
                    dakika_part = s[dakika_index-3:dakika_index-1]
                else:
                    dakika_part = s[dakika_index-2:dakika_index-1]
                
                time_in_hours += float(dakika_part)/60
        
        travel_time_in_hours.append(time_in_hours)    
    return travel_time_in_hours
dir_path = os.path.dirname(os.path.realpath(__file__))
input_directory = dir_path + "\\data" # Data will be printed out here

main_dataframe = pd.read_excel(input_directory+"\\ALL_bus_journey"+".xlsx")    

#Price Column
main_dataframe.price = main_dataframe["price"].str.replace("₺", "", case=False, regex=True) # remove TL symbol from column
main_dataframe.price = main_dataframe["price"].str.replace(",", ".", case=False, regex=True) # change "," to "." for numeric
main_dataframe.price = pd.to_numeric(main_dataframe.price,errors='coerce')

main_dataframe.travel_time = main_dataframe['travel_time'].str.replace("[()*]","",regex = True) # Remove parantheses and * 
main_dataframe["travel_time_in_hours"] = travel_time_to_hours(main_dataframe.travel_time)

main_dataframe.departure_time = pd.to_datetime(main_dataframe['date'],format ="%Y-%m-%d" )+pd.to_timedelta(main_dataframe['departure_time']+":00")
main_dataframe["arrival_time"] = main_dataframe.departure_time + pd.to_timedelta(main_dataframe["travel_time_in_hours"],unit="h")

#main_dataframe.drop(labels = ["date","Unnamed: 0","travel_time_in_hours","travel_time"],axis=1,inplace=True)
return_dataframe = main_dataframe[['from', 'destination', 'price','company','departure_time','arrival_time','data_collected_at']]
return_dataframe['journey_type'] = "bus"
return_dataframe.to_excel("otobus_data.xlsx")
