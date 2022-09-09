# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 15:22:12 2022

@author: HP
"""

from selenium import webdriver
import pandas as pd
import os 
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime as dt
from itertools import permutations
from selenium.common.exceptions import TimeoutException

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time
from fake_useragent import UserAgent


# from selenium import webdriver
# import chromedriver_autoinstaller


# chromedriver_autoinstaller.install()  # Check if the current version of chromedriver exists
#                                       # and if it doesn't exist, download it automatically,
#                                       # then add chromedriver to path

# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# assert "Python" in driver.title



dir_path = os.path.dirname(os.path.realpath(__file__))
output_directory = dir_path + "\\data" # Data will be printed out here
if not os.path.exists(output_directory): # create the folder if not exists already
    os.mkdir(output_directory)

datelist = pd.date_range(dt.today(), periods=1).tolist() # 7 days forward
datelist_as_strings = [x.strftime("%Y-%m-%d") for x in datelist]

main_dataframe = pd.DataFrame()
city_codes = pd.read_excel("city_codes.xlsx")
city_codes.drop("Unnamed: 0",axis=1,inplace = True)    
options = webdriver.ChromeOptions()
# options.headless = True
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument("--disable-extensions")
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_argument(f'user-agent={userAgent}')

chrome_driver = webdriver.Chrome(options=options)
browser = webdriver.Chrome(options=options)


#%%
for comb in permutations(city_codes["city_code"], 2): # dont use combination, think of istanbul-siirt, siirt-istanbul routes
    start=dt.now()
    
    data_collected_at = dt.now()
    empty_page = False
    partner_column = []
    price_column = []
    departure_column = []
    travel_time_column = []
    date_column = []
    
    for date in datelist_as_strings:            
        urlpage = "https://www.obilet.com/seferler/"+ str(comb[0])+"-"+str(comb[1]) +"/" + date 
        
        # Go to page and wait loading
        browser.get(urlpage)    
        #browser.maximize_window()
        time.sleep(2)
            
        error_pop_up_xpath = '/html/body/main/div[9]/div/div[2]/div/button[1]'
        
        # CHANGE THIS TO : Cant find data i want, restart the progress
        if len(browser.find_elements(By.XPATH, error_pop_up_xpath)) > 0: # if Error pop up shows up, then wait, restrart
            print('ERROR')    
            time.sleep(60)
            browser.close()
            browser = webdriver.Chrome(options=options)
          
        
        try:
            element = WebDriverWait(browser, 8).until(
        EC.presence_of_element_located((By.XPATH, "/html/body/main/ul/li/div[1]/div[1]/div"))
        )
        except TimeoutException:
            empty_page = True 
        
        if empty_page:
            continue
        
        table_list = []
        
        #elements = browser.find_elements_by_xpath("//*[@class='main row']")
        partners =  browser.find_elements_by_xpath("/html/body/main/ul/li/div[1]/div[1]/div")
        prices =  browser.find_elements_by_xpath("/html/body/main/ul/li/div[1]/div[4]/div[1]/span")
        departures =  browser.find_elements_by_xpath("/html/body/main/ul/li/div[1]/div[2]/div[1]")
        travel_times = browser.find_elements_by_xpath("/html/body/main/ul/li/div[1]/div[2]/div[2]")
        min_size = min([len(partners),len(prices),len(departures),len(travel_times)])

        
        for i in range(min_size):
            partner = partners[i].get_attribute("data-name")
            departure_time = departures[i].text
            price = prices[i].text
            travel_time = travel_times[i].text
        
            partner_column.append(partner)
            price_column.append(price)
            departure_column.append(departure_time)
            travel_time_column.append(travel_time)
            date_column.append(date)
       
           
    city_name_0 = city_codes.loc[city_codes['city_code'] == comb[0], 'city_name'].reset_index(drop=True)[0]
    city_name_1 = city_codes.loc[city_codes['city_code'] == comb[1], 'city_name'].reset_index(drop=True)[0]        
   
    
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
    stop = dt.now()

    print(city_name_0+"_"+city_name_1, "completed in", stop - start, "seconds")
browser.close()    
main_dataframe.to_excel(output_directory+"\\ALL_bus_journey"+".xlsx")    

