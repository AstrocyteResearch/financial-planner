# -*- coding: utf-8 -*-
"""
Discreption : Data crawler, automatically get treasury rates and interpolate

Created on Tue May 12 14:07:21 2020

@author : Jincheng Dan 
email   : jcdan@bu.edu

"""

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from scipy.interpolate import interp1d

def term_structure(chromdriver_path):
    '''Get the treasury rate data from the U.S Department of The Treasury,
       do interpolation to get annual rate of 60 years.
       Chrome browser and chrome driver are needed.
       chromdriver_path is the local path to chromedriver.
    '''
    
    url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yield'
    chrome_options = Options()
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920x1080")
    chrome_options.add_argument('headless')

    # initialize chrome driver
    driver = webdriver.Chrome(chromdriver_path, options = chrome_options)
    driver.get(url)
    
    # xml style data
    interest_xml = driver.find_elements_by_xpath('//*[@id="t-content-main-content"]/\
                                                 div/table/tbody/tr/td/div/table/tbody')
    # list of strings style data
    interest_text = interest_xml[0].text.split('\n')
    
    # get the dataframe of the treasury rates
    nrow = len(interest_text)-1
    ncol = len(interest_text[1].split(' '))
    col_names = [interest_text[0][i*5:(i*5+5)] for i in range(ncol)]
    interests = pd.DataFrame(np.zeros([nrow,ncol]), columns = col_names )
    for row in range(nrow):
        interests.iloc[row,:] = interest_text[row+1].split(' ')
    interests.iloc[:,1:] = interests.iloc[:,1:].astype(float)
    
    # use interpolation to get discount rate every year
    interpolation = interp1d([1,2,3,5,7,10,20,30],interests.iloc[-1,5:])
    term_structure = interpolation(range(1,31))/100
    
    # extend term structure to 60 years,
    # for terms that are longer than 30 years use the rate of 30 years.
    term_structure = np.concatenate((np.array(term_structure),
                                     np.repeat(interests.iloc[-1,-1]/100,30)))
    print('interestes data successfully collected')
    return term_structure

# test and exemple
if __name__ == '__main__':    
    chromdriver_path = 'D:\\chromedriver\\chromedriver_win32\\chromedriver.exe'
    interests = term_structure(chromdriver_path)