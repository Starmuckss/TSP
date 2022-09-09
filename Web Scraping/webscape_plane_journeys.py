# -*- coding: utf-8 -*-
"""
Created on Tue Mar  8 19:01:54 2022

@author: HP
"""
from selenium import webdriver
import pandas as pd
import time
from selenium.common.exceptions import ElementClickInterceptedException,ElementNotInteractableException,NoSuchElementException
import os 
from selenium.webdriver.support import expected_conditions as EC
import datetime 
from itertools import permutations
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

dir_path = os.path.dirname(os.path.realpath(__file__))
output_directory = dir_path + "\\data" # Data will be printed out here
if not os.path.exists(output_directory): # create the folder if not exists already
    os.mkdir(output_directory)

datelist = pd.date_range(datetime.datetime.today() + datetime.timedelta(days=1), periods=1).tolist() # 7 days forward
datelist_as_strings = [x.strftime("%Y%m%d") for x in datelist]

main_dataframe = pd.DataFrame()
ucus_noktaları = pd.read_excel("ucus_noktaları.xlsx")
ucus_noktaları.drop("Unnamed: 0",axis=1,inplace = True)    
options = webdriver.FirefoxOptions()
#options.headless = True
import timeit
browser = webdriver.Firefox(options=options)

for comb in permutations(ucus_noktaları["city_code"][0:81], 2): # dont use combination, think of istanbul-siirt, siirt-istanbul routes
    start=datetime.datetime.now()
    
    data_collected_at = datetime.datetime.now()
    empty_page = False
    partner_column = []
    price_column = []
    departure_column = []
    travel_time_column = []
    date_column = []
    
    for date in datelist_as_strings:            
        urlpage = "https://www.obilet.com/ucuslar/" + str(comb[0]) + "-" + str(comb[1]) + "/" + date+ "/1a/economy/all"
        # Go to page and wait loading
        browser.get(urlpage)    
        browser.maximize_window()
        
        try:
            element = WebDriverWait(browser, 8).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/div[6]/ul/li/div[1]/ul/li/div[1]/div/span"))
        )
        except TimeoutException:
            empty_page = True                                       
            
        table_list = []                             
        partners =  browser.find_elements_by_xpath("/html/body/main/div[6]/ul/li/div[1]/ul/li/div[1]/div/span")
        travel_times = browser.find_elements_by_xpath("/html/body/main/div[6]/ul/li/div[1]/ul/li/div[3]/div[2]/div[1]/span")
        prices =  browser.find_elements_by_xpath("/html/body/main/div[6]/ul/li/div[1]/div[1]/div[2]")
        departures =  browser.find_elements_by_xpath("/html/body/main/div[6]/ul/li/div[1]/ul/li/div[3]/div[1]/div[1]")
        
        min_size = min([len(partners),len(prices),len(departures),len(travel_times)])


        for i in range(min_size):
            partner = partners[i].text
            departure_time = departures[i].text
            price = prices[i].text
            travel_time = travel_times[i].text
        
            partner_column.append(partner)
            price_column.append(price)
            departure_column.append(departure_time)
            travel_time_column.append(travel_time)
            date_column.append(date)

           
    city_name_0 = ucus_noktaları.loc[ucus_noktaları['city_code'] == comb[0], 'city_name'].reset_index(drop=True)[0]
    city_name_1 = ucus_noktaları.loc[ucus_noktaları['city_code'] == comb[1], 'city_name'].reset_index(drop=True)[0]        
    
    if empty_page:        
        print("No journey in " + city_name_0,city_name_1)        
        dataframe = pd.DataFrame(data = {"company":["null"],"price":["null"],"departure_time":["null"],"travel_time":["null"],"date":["null"]})
        dataframe["data_collected_at"] = data_collected_at
        dataframe["from"] = city_name_0
        dataframe["destination"] = city_name_1
        
    else:    
        dataframe = pd.DataFrame(data = {"company":partner_column,"price":price_column,"departure_time":departure_column,"travel_time":travel_time_column,"date":date_column})
        dataframe["data_collected_at"] = data_collected_at
        
        dataframe["from"] = city_name_0
        dataframe["destination"] = city_name_1
        
    main_dataframe = main_dataframe.append(dataframe)
        #dataframe.to_excel(output_directory+"\\"+city_name_0+"_"+city_name_1+".xlsx")
    stop = datetime.datetime.now()

    print(city_name_0+"_"+city_name_1, "completed in", str(stop - start), "seconds")
browser.close()    
main_dataframe.to_excel(output_directory+"\\ALL_flight_journey"+".xlsx")    
