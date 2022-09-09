# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 22:37:09 2022

@author: HP
"""
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import pandas as pd
import time
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import ElementClickInterceptedException,ElementNotInteractableException,NoSuchElementException
import os 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from datetime import datetime as dt
import datetime
from selenium.webdriver.common.by import By
from itertools import combinations

# Yurtdisi sehirleri var, onları elemeliyim, ama nasil?


if True: # not os.path.exists("city_codes.xlsx")
    all_city_codes = []
    #Get the all destinations from this page:https://www.obilet.com/duraklar
    
    options = webdriver.FirefoxOptions()
    options.headless = False
    browser = webdriver.Firefox(options=options)
    url = "https://www.obilet.com/duraklar"    
    browser.get(url)    
    
    destinations = browser.find_elements_by_xpath("/html/body/main/div[3]/div[1]/ul/li/a")
    all_destinations_urls = [x.get_attribute("href") for x in destinations]
    
    for destination_url in all_destinations_urls[0:80]:
        browser.get(destination_url)
        time.sleep(1)
        city_code=browser.find_element(By.XPATH,"/html/body/main/div[1]/div[2]/form/div[2]/div/ob-select/div/ul/li").get_attribute('data-value')                                       
        city_name = destination_url.split("/")[-1]
        #city_code = browser.find_element_by_class_name("item").get_attribute('data-value')
        #city_plaka = browser.find_element(By.XPATH,"/html/body/main/div[2]/div[1]/div/div[4]/div/span[2]").text
        elements = browser.find_elements(By.CLASS_NAME,"info-box")
        
        for elem in elements:
            if  elem.find_element(By.CLASS_NAME,"title").text == "PLAKA KODU":
                city_plaka = elem.find_element(By.CLASS_NAME,"info").text
        
        print(city_name,city_code,city_plaka)
        all_city_codes.append((city_name,city_code,city_plaka))
   
    
df = pd.DataFrame(all_city_codes)    
df = df.rename(columns = {0:"city_name",1:"city_code",2:"plaka"})
df.to_excel("city_codes.xlsx")

