#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 28 10:21:04 2021

@author: abhishekbada
"""
import glob as glob
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn import linear_model
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression



#USER WILL NEED TO SET THE CORRECT FILEPATHS FOR EACH OF THE PD.READ_CSV THEY CAN THEN COPY THESE ACROSS EACH FUNCTION 


def AddBedroom():
    
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/1_Bedroom.csv')
    df["Bedrooms"] = 1
    df.to_csv('/Users/abhishekbada/Desktop/CS Project/1_Bedroom.csv')
    
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/2_Bedroom.csv')
    df["Bedrooms"] = 2
    df.to_csv('/Users/abhishekbada/Desktop/CS Project/2_Bedroom.csv')
    
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/3_Bedroom.csv')
    df["Bedrooms"] = 3
    df.to_csv('/Users/abhishekbada/Desktop/CS Project/3_Bedroom.csv')
    
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/4_Bedroom.csv')
    df["Bedrooms"] = 4
    df.to_csv('/Users/abhishekbada/Desktop/CS Project/4_Bedroom.csv')
    
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/5_Bedroom.csv')
    df["Bedrooms"] = 5
    df.to_csv('/Users/abhishekbada/Desktop/CS Project/5_Bedroom.csv')

def AggBedrooms():
    files = glob.glob('/Users/abhishekbada/Desktop/CS Project/*Bedroom.csv')
    df = pd.concat(((pd.read_csv(file)) for file in files), ignore_index = True)
    
    
    df = df.drop(["RegionID","SizeRank", "RegionType", "StateName", "Metro" ], axis = 1)
    
    df1 = pd.melt(df, id_vars=['CountyName', 'State', 'City', "RegionName", "Bedrooms"], var_name = "Date", value_name = "Price")
    
    print(df1.isna().sum())
    df1.dropna(subset = ["Price"], inplace = True)
    
    df2 = df1.groupby(['CountyName', 'State', 'City', 'Date', "Bedrooms", "RegionName"], as_index= False).Price.mean()
    
    df2['Date'] = pd.to_datetime(df2["Date"], errors = "coerce") 
    df2['Year'] = df2["Date"].dt.year # applying dt.year to extract year and creating a year column with that value
    df2['Month'] = df2["Date"].dt.month # applying dt.month to extract month and creating a month column with that value
    df2 = df2.set_index('Date')
    
    df2.to_csv('/Users/abhishekbada/Desktop/CS Project/AllBedrooms.csv')
    


def MergeVariables():
    
    dfMain = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/AllBedrooms.csv')
    dfRate = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/30 Year Rate.csv')
    dfSP = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/S&P 500.csv')
    dfOther = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/CSPDSV2.csv', error_bad_lines=False)
    
    dfOther[['CountyName', 'State']] = dfOther['Region Name'].str.split(", ", expand = True)
    
    dfMain = pd.merge(dfMain, dfOther, on = ['CountyName', "State", "Year"] , how = "left" )
    dfMain = pd.merge(dfMain, dfRate, on=['Year', 'Month'] ,how = "left") 
    dfMain = pd.merge(dfMain, dfSP, on=['Year', 'Month'] ,how = "left")
    dfMain = dfMain.drop(("Date_y"),axis = 1)
    
    dfMain = dfMain.dropna()
    print(dfMain.head(5))
    dfMain.to_csv('/Users/abhishekbada/Desktop/CS Project/Main.csv')

def  minyears():
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main.csv')
    df = df.drop(["S&P 500"], axis = 1)
    dfSP = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/S&P 500.csv')
    df = pd.merge(df, dfSP, on=['Year', 'Month'] ,how = "left")
    print(df.head(5))
    df = df.rename(columns = {'Date_x':'Date'})
    df['Date'] = pd.to_datetime(df["Date"], errors = "coerce") 
    df = df[df['Date'].dt.year >= 2010]

    df[["Unemployment Rate", "Crime Rate", "Rate", "S&P 500"]] = df[["Unemployment Rate", "Crime Rate", "Rate","S&P 500"]].apply(pd.to_numeric, errors = 'coerce')
    df = df[df.Price != 0]
    #df = df.dropna()
    print(df.head(15))
    df.to_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
    

    
# MUST RUN ALL FUNCTIONS ABOVE TO GE THE APPROPRIATE DATE SET TO BE USED FOR THE BELOW FUNCTIONS

def linearRegression():
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
    reg = linear_model.LinearRegression()
    predictors = ['Bedrooms',"S&P 500", "Rate", "Unemployment Rate", "Crime Rate"]
    for predictor in predictors:
        reg.fit(df[[predictor]], df['Price'])

        print(reg.coef_)
        print(reg.intercept_)
        print(reg.score(df[[predictor]], df['Price']))
        print('The linear regression model for ' + predictor + ' is: y=' + str(int(reg.coef_)) + "x+" + str(int(reg.intercept_)))

def multilinearRegression(CountyName,NBedrooms,SP,MR,UR,CR):        
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
    df = df[df['CountyName'] == CountyName]
    reg = linear_model.LinearRegression()    
    reg.fit(df[['Bedrooms',"S&P 500", "Rate", "Unemployment Rate", "Crime Rate"]], df['Price'])
    print(reg.coef_)
    print(reg.intercept_)
    print(reg.predict([[NBedrooms,SP,MR,UR,CR]]))

def machinelearningmodel(CountyName):
    df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
    df = df[df['CountyName'] == CountyName]
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(df[['Bedrooms',"S&P 500", "Rate","Unemployment Rate","Crime Rate"]],df['Price'],test_size = 0.2)
    from sklearn.linear_model import LinearRegression
    clf = LinearRegression()
    clf.fit(X_train,y_train)
    print(clf.score(X_test,y_test))
    
    
#UNCOMMENT THE BELOW FUNCTIONS AND ENTER THE APPRORPIATE INPUTS TO SEE YOUR RESULTS
  
#multilinearRegression()
#linearRegression()
#machinelearningmodel()  



import unittest

class gradesTestCases(unittest.TestCase): 
    
    def test_columns_have_no_null_values(self): 
            df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
            predictors = ['Bedrooms',"S&P 500", "Rate","Unemployment Rate","Crime Rate"]
            for pred in predictors:
                for boolean in df[pred].isna():
                    self.assertTrue(boolean == False)
            
    def test_dataset_has_no_duplicates(self): 
            df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
            for boolean in df.duplicated():
                self.assertTrue(boolean == False)
            
    def test_price_column_has_no_zeros(self): 
        df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
        for boolean in df['Price'].isin([0]):
                self.assertTrue(boolean == False)
            
    def test_that_unemployment_has_no_zeros(self): 
        df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
        for boolean in df['Unemployment Rate'].isin([0]):
            self.assertTrue(boolean == False)
     
    def test_all_values_greater_than_zero(self): 
          df = pd.read_csv('/Users/abhishekbada/Desktop/CS Project/Main1.csv')
          for boolean in df['S&P 500'].isin([0]):
              self.assertTrue(boolean == False)
            

         
if __name__ == '__main__':
    unittest.main()  

