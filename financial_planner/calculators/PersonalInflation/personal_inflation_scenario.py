"""
Created on 2020/5/13 13:12
Author: Xinyu Guo
Email: xyguo@bu.edu
IDE: PyCharm
"""
import requests
import json
import pandas as pd
from datetime import datetime
import numpy as np
import time


class Cpi_Data:
    def __init__(self, test=False):
        '''
        Getting CPI and basket data through API of Bureau of Labour

        Warning: There is a limit of daily data volume getting from the api.
            When the limit is reached, you can set test as True to load data from local json file.(containing 2019-2020 data)
        '''
        self.basket = {
            'API_code':{
                'Food': 'CUUR0000SAF',
                'Education': 'CUUR0000SAE',
                'Recreation': 'CUUR0000SAR',
                'Medical':'CUUR0000SAM',
                'Transportation':'CUUR0000SAT',
                'Apparel': 'CUUR0000SAA',
                'Housing': 'CUUR0000SAH',
                'Others': 'CUUR0000SAG'},
            'item_chg': {},
            'weights': {
                'Food': 0.153,
                'Education': 0.068,
                'Recreation': 0.06,
                'Medical': 0.072,
                'Transportation': 0.168,
                'Apparel': 0.036,
                'Housing': 0.41,
                'Others': 0.034}}
        self.time = datetime.fromtimestamp(time.time())
        self.year = self.time.year
        self.category = list(self.basket['API_code'].keys())
        self.get_cpi_data()
        self.test=test


    def get_cpi_data(self):
        '''
        Get monthly CPI data from API of US bureau of Labor
        '''
        if not self.test:
            code_list = list(self.basket['API_code'].values())
            headers = {'Content-type': 'application/json'}
            data = json.dumps({"seriesid": code_list, "startyear": str(self.year-1), "endyear": str(self.year)})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/', data=data, headers=headers)
            json_data = json.loads(p.text)

            assert json_data['status'] == 'REQUEST_SUCCEEDED', 'Get Data through API Failed !!'
        else:
            file = open('data.json', 'r', encoding='utf-8')
            json_data = json.load(file)

        for i in range(0,8):
            item_data = json_data['Results']['series'][i]['data']
            incrs = float(item_data[0]['value'])/float(item_data[1]['value'])-1
            self.basket['item_chg'][self.category[i]]=incrs


class PersonalInflationScenario:
    def __init__(self, expense, Name='Scenario1'):
        '''
        Args:
            expense: dict
                The monthly expenditure for each category corresponding to the CPI basket

        Returns:
            df: dataframe
        '''
        self.Scenario_name = Name
        self.expense = expense
        self.cpi = Cpi_Data()
        self.basket = self.cpi.basket

    def run(self):
        expense_weights = list(self.expense.values())/np.sum(list(self.expense.values()))

        df = pd.DataFrame.from_dict(self.basket)
        df.drop('API_code',axis=1,inplace=True)
        df['personal'] = expense_weights

        cpi_inflation = np.sum(df['item_chg']*df['weights'])
        self_inflation = np.sum(df['item_chg']*df['personal'])

        df.loc['Inflation Rate'] = [None, cpi_inflation, self_inflation]
        df.columns = ['Price_change','CPI_weights','Personal_weights']

        return df


