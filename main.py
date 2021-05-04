import sys
import os

from fredapi import Fred
from pandas_datareader import data

import folium
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime
import scipy.stats as stats

from PyQt5 import *
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import*

import warnings
warnings.filterwarnings('ignore')

from fredapi import Fred

from chloroplethwidget import chloroplethWidget
from foliumwidget import foliumWidget
#from pairplotwidget import pairplotWidget

# initial directory 
cwd = os.getcwd()
os.chdir(cwd)


def show_exception_and_exit(exc_type,exc_value,tb):
    import traceback
    traceback.print_exception(exc_type,exc_value,tb)
    print("Invalid Input")
    sys.exit(-1)

sys.excepthook=show_exception_and_exit


class AppMain(QMainWindow):

    def __init__(self):
        
        QMainWindow.__init__(self)

        loadUi(r'main.ui',self)

        

        self.setWindowTitle("Housing Sector Market Performance Analysis")
        #self.setWindowIcon(QtGui.QIcon('C:\logo.jpg'))

        self.calculateButton.clicked.connect(self.correlate)
   #     
        self.exitButton.clicked.connect(self.close)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
       
        #initialize FRED data sets
        self.combo_FRED_1.addItem("CASE-SHILLER")
        self.combo_FRED_1.addItem("CPI") #M1 Stock
        self.combo_FRED_1.addItem("M2") #S&P/Case-Shiller U.S. National Home Price Index
        self.combo_FRED_1.addItem("EFFR") #Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
        self.combo_FRED_1.addItem("10YR") #M2 Money Stock
        self.combo_FRED_1.addItem("30YR_MORT") #Effective Federal Funds Rate
        self.combo_FRED_1.addItem("PERS_SAV") #10-Year Treasury Constant Maturity Rate
        self.combo_FRED_1.addItem("WTI_OIL") #Unemployment Rate maybe look at CA?
        self.combo_FRED_1.addItem("BUSLOANS") #30-Year Fixed Rate Mortgage Average in the United States
        self.combo_FRED_1.addItem("CORP_BOND") #3-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar

        #initialize FRED data sets
        self.combo_FRED_2.addItem("CASE-SHILLER")
        self.combo_FRED_2.addItem("CPI") #M1 Stock
        self.combo_FRED_2.addItem("M2") #S&P/Case-Shiller U.S. National Home Price Index
        self.combo_FRED_2.addItem("EFFR") #Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
        self.combo_FRED_2.addItem("10YR") #M2 Money Stock
        self.combo_FRED_2.addItem("30YR_MORT") #Effective Federal Funds Rate
        self.combo_FRED_2.addItem("PERS_SAV") #10-Year Treasury Constant Maturity Rate
        self.combo_FRED_2.addItem("WTI_OIL") #Unemployment Rate maybe look at CA?
        self.combo_FRED_2.addItem("BUSLOANS") #30-Year Fixed Rate Mortgage Average in the United States
        self.combo_FRED_2.addItem("CORP_BOND") #3-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar

        year=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']

        self.comboYearStart.addItems(year)
        self.comboYearEnd.addItems(year)

        #self.start_dateEdit.date()
        #self.end_dateEdit.date()



        



        #initialize FRED data
        fred = Fred(api_key='d7f545fe7858da4279909dd26a7b28cc')
        df = {}

        df['CASE-SHILLER'] = fred.get_series('CSUSHPISA', observation_start='1/31/1996') #S&P/Case-Shiller U.S. National Home Price Index
        df['CPI'] = fred.get_series('CPIAUCSL', observation_start='1/31/1996') #Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
        df['M2'] = fred.get_series('WM2NS', observation_start='1/31/1996')#M2 Money Stock
        df['EFFR'] = fred.get_series('EFFR', observation_start='1/31/1996')#Effective Federal Funds Rate
        df['10YR'] = fred.get_series('DGS10', observation_start='1/31/1996') #10-Year Treasury Constant Maturity Rate
        df['30YR_MORT'] = fred.get_series('MORTGAGE30US', observation_start='1/31/1996') #30-Year Fixed Rate Mortgage Average in the United States
        df['PERS_SAV'] = fred.get_series('PSAVERT', observation_start='1/31/1996') #Personal Saving Rate
        df['WTI_OIL'] = fred.get_series('DCOILWTICO', observation_start='1/31/1996') #Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma
        df['BUSLOANS'] = fred.get_series('BUSLOANS', observation_start='1/31/1996')#Commercial and Industrial Loans, All Commercial Banks
        df['CORP_BOND'] = fred.get_series('DAAA', observation_start='1/31/1996')#Moody's Seasoned Aaa Corporate Bond Yield
        df = pd.DataFrame(df).resample('M').mean()
        #df=df.dropna()

        #import SPY data 
        start_date = pd.to_datetime('2010-01-31')
        end_date = pd.to_datetime('2021-04-30')

        #load SPY data
        panel_data = data.DataReader('SPY','yahoo', start_date, end_date)
        spy=panel_data['Adj Close'].to_frame().resample('M').mean()

        self.fred_df = df.merge(spy, left_index=True, right_index=True)
        del df, panel_data, spy

        ############INITIALIZE 1 BEDROOM DF###########################################################
        #read zip data
        zip_df=pd.read_csv(r'data\ZIP-COUNTY-FIPS_2017-06.csv')
        zip_df.rename({'STCOUNTYFP': 'GEO_ID'}, axis=1, inplace=True)
        zip_df["GEO_ID"] = zip_df["GEO_ID"].astype(str)

        #read bedroom data and melt
        df1=pd.read_csv(r'data\Zip_zhvi_bdrmcnt_1_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv')
        df1['Bedrooms'] = '1'
        df1 = pd.melt(df1, id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName','State', 'City', 'Metro', 'CountyName', 'Bedrooms'], var_name='Date', value_name='price_index')#.set_index('Date')
        df1.rename({'RegionName': 'ZIP'}, axis=1, inplace=True)
        df1['Date']=pd.to_datetime(df1['Date'])

        #merge zip data
        df1=df1.merge(zip_df, how='left')
        df1=df1.set_index('Date')

        #merge FRED dataset
        self.df1 = df1.merge(self.fred_df, left_index=True, right_index=True)

        #unique names for list
        county_list=self.df1['CountyName'].unique()
        state_list=self.df1['State'].unique()

        #pairplot button
        self.pairplotButton.clicked.connect(self.pairplot)

        #initialize pairplot combo boxes
        self.pair_countyBox.addItems(county_list)
        self.pair_stateBox.addItems(state_list)



    def __del__(self):
        sys.stdout = sys.__stdout__

      
    def normalOutputWritten(self,text):
        cursor=self.printOutput.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.printOutput.setTextCursor(cursor)
        self.printOutput.ensureCursorVisible()


    def correlate(self):


        #sequentialfeatureselector
        # #plotlly express

        #convert text input times to numeric
        #year_start = datetime.strptime(self.comboYearStart.currentText(), '%Y')
        #year_end = datetime.strptime(self.comboYearEnd.currentText(), '%Y')

        
        data_1 = self.fred_df[''+ str(self.comboYearStart.currentText()) +'-01-01':''+ str(self.comboYearEnd.currentText()) +'-01-01'][''+ str(self.combo_FRED_1.currentText()) +'']
        data_2 = self.fred_df[''+ str(self.comboYearStart.currentText()) +'-01-01':''+ str(self.comboYearEnd.currentText()) +'-01-01'][''+ str(self.combo_FRED_2.currentText()) +'']
    
        
      

    def pairplot(self):

        
        ############PAIRPLOT FUNCTION
        #time slice
        #start_date = pd.to_datetime(''+ str(self.start_dateEdit.date() ) + '')
        #end_date = pd.to_datetime(''+ str(self.end_dateEdit.date() ) + '')
        #start_date = pd.to_datetime('1/1/2016')
        #end_date = pd.to_datetime('1/1/2020')
        #self.df1=self.df1[start_date:end_date]
        #filter down to Bedroom##############
        #self.df1=self.df1[(self.df1['CountyName']==''+ str(self.pair_countyBox.currentText()) + '') & (self.df1['State']==''+ str(self.pair_stateBox.currentText()) + '')].groupby(['CountyName','State','Bedrooms'])['price_index','CASE-SHILLER','CPI','M2','EFFR','30YR_MORT','PERS_SAV','10YR','Adj Close','WTI_OIL','BUSLOANS','CORP_BOND'].resample('M').mean().dropna()
        #print(self.df1)
        df_pp=self.df1[(self.df1['CountyName']=="Cook County") & (self.df1['State']=="IL")].groupby(['CountyName','State','Bedrooms'])['price_index','CASE-SHILLER','CPI','M2','EFFR','30YR_MORT','PERS_SAV','10YR','Adj Close','WTI_OIL','BUSLOANS','CORP_BOND'].resample('M').mean().dropna()
        self.pairplotWidget.canvas.axes.cla()
        #self.pairplotWidget.canvas.axes.draw()
        pd.plotting.scatter_matrix(df_pp, figsize=(5,5), marker = '.', hist_kwds = {'bins': 10}, s = 60, alpha = 0.6, ax=self.pairplotWidget.canvas.axes)
        self.pairplotWidget.canvas.draw()
        




class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


app=QApplication(sys.argv)
#app.setStyle('Fusion')
window=AppMain()
window.show()
sys.exit(app.exec_())