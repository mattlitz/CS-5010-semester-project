import pandas as pd

"""
title: "CS5010 Project"
author: "Abhijeet Chawhan"
date: "5/9/2021"
output: Correlation calculations and Plots
"""


# This Class reads SP500 and CSPDS datasets and generates the respective dataframe.
# SP500 dataset contains S & P value of a particuler month of a year.
# CSPDS dataset contains unemployment and crime rates of city / state / county for a particular year.

class Sp500CspdsData:
    def __init__(self):
        self.df_sp500 = pd.read_csv("/Users/abhijeet/Desktop/MSDS/CSSemProject/SP500.csv")
        self.df_sp500 = self.df_sp500[self.df_sp500['SP500'] != '.']
        self.df_sp500['SP500'] = self.df_sp500.SP500.astype(float)
        self.df_sp500['DATE'] = pd.to_datetime(self.df_sp500['DATE'])
        self.df_sp500['DATE_YEAR'] = pd.DatetimeIndex(self.df_sp500['DATE']).year
        self.df_sp500['DATE_MONTH'] = pd.DatetimeIndex(self.df_sp500['DATE']).month
        self.df_sp500['YearMonth'] = pd.to_datetime(self.df_sp500['DATE']).dt.strftime('%Y-%m')
        self.df_cspds = pd.read_csv("/Users/abhijeet/Desktop/MSDS/CSSemProject/CSPDS.csv")

# This method gives sp500 dataframe and pandas aggregate is applied on the dataframe.
# When only start_year is provided and end_year is None, the Dataframe is grouped using 'DATE_YEAR'.
# The mean of the group with value start_year which is again grouped by 'DATE_MONTH'
# is calculated and the resulting dataframe is returned.
    def get_sp_data(self, start_year, end_year=None):
        if int(start_year) > 2021 or int(start_year) < 2011:
            print("Date is out of range. Please provide Date between 2011 3 and 2021 4")
        else:
            df = self.df_sp500[self.df_sp500['SP500'] != '.']
            if end_year is None:
                df_tmp = df.groupby('DATE_YEAR').get_group(int(start_year))
                result = df_tmp.groupby('DATE_MONTH').mean()
            else:
                df = df[(df['DATE_YEAR'] >= int(start_year)) & (df['DATE_YEAR'] <= int(end_year))]
                result = df.groupby('DATE_YEAR').mean()
            return result

# This method gives dataframe containing unemployment rate and crime rate of
# states / counties / cities and pandas aggregate is applied on the dataframe.
# Dataframe is cleaned and filtered based on 'Year' column with the start_year and end_year inputs.
# Then aggregate is applied to the Datafrane using groupby on
# column with name provided as data_grp_id (eg. 'State', 'County').
# Group with value data_grp_val ('New York', 'Virginia') is retrieved from the resulting dataframe.
# Mean is applied on the resulting dataframe using groupby on 'Year' column
# and the final resulting dataframe is returned.
    def get_unemp_crime_data(self, data_grp_id, data_grp_val, start_year, end_year=None):
        df = self.df_cspds[self.df_cspds['State'].notnull()]
        df = df[(df['Year'] >= int(start_year)) & (df['Year'] <= int(end_year))]
        df_grp_tmp = df.groupby(data_grp_id).get_group(data_grp_val)
        df_grp = df_grp_tmp.groupby('Year').mean()
        return df_grp
