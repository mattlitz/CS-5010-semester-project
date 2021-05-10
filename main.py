import sys
import os

# initial directory 
cwd = os.getcwd()
os.chdir(cwd)

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
from pairplotwidget import pairplotWidget
#from heatmapwidget import heatmapWidget



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

        
        self.setWindowTitle("Housing Sector Exploratory Data Analysis")
        #self.setWindowIcon(QtGui.QIcon('C:\logo.jpg'))

        self.calculateButton.clicked.connect(self.correlate)
   #     
        self.exitButton.clicked.connect(self.close)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
       

        #self.comboYearStart.addItems(year)
        #self.comboYearEnd.addItems(year)

        self.start_dateEdit.date()
        self.end_dateEdit.date()


        #initialize FRED data
        fred = Fred(api_key='d7f545fe7858da4279909dd26a7b28cc')
        df = {}

        df['CASE-SHILLER'] = fred.get_series('CSUSHPISA', observation_start='1/31/1996') #S&P/Case-Shiller U.S. National Home Price Index
        df['UNRATE'] = fred.get_series('UNRATE', observation_start='1/31/1996') #Unemployment Rate
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
        spy.rename({'Adj Close': 'SP500'}, axis=1, inplace=True)

        self.fred_df = df.merge(spy, left_index=True, right_index=True)
        del df, panel_data, spy

        ############INITIALIZE 1 BEDROOM DF###########################################################
        #read zip data
        zip_df=pd.read_csv(r'data\ZIP-COUNTY-FIPS_2017-06.csv')
        zip_df.rename({'STCOUNTYFP': 'GEO_ID'}, axis=1, inplace=True)
        zip_df["GEO_ID"] = zip_df["GEO_ID"].astype(str)

        #read bedroom data and melt
        df1=pd.read_csv(r'data\Zip_zhvi_bdrmcnt_4_uc_sfrcondo_tier_0.33_0.67_sm_sa_mon.csv')
        df1['Bedrooms'] = '1'
        df1 = pd.melt(df1, id_vars=['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName','State', 'City', 'Metro', 'CountyName', 'Bedrooms'], var_name='Date', value_name='price_index')#.set_index('Date')
        df1.rename({'RegionName': 'ZIP'}, axis=1, inplace=True)
        df1.rename({'price_index': 'House Price Index'}, axis=1, inplace=True)
        df1['Date']=pd.to_datetime(df1['Date'])

        #merge zip data
        df1=df1.merge(zip_df, how='left')
        df1=df1.set_index('Date')

        #merge FRED dataset
        self.df1 = df1.merge(self.fred_df, left_index=True, right_index=True)

        #unique names for list
        county_list=sorted(self.df1['CountyName'].unique(), key=str.lower)
        state_list=sorted(self.df1['State'].unique(), key=str.lower)

        bedroom_list=['1','2','3','4','5']

        #pairplot button
        self.pairplotButton.clicked.connect(self.pairplot)

        #initialize pairplot combo boxes
        self.countyBox.addItems(county_list)
        self.stateBox.addItems(state_list)

        self.bedroomBox.addItems(bedroom_list)

        #pairplot button
        #self.heatmapButton.clicked.connect(self.heatmap)

        #initialize correlate line chart combo boxes
        metrics=['House Price Index','CASE-SHILLER','CPI','M2','EFFR','30YR_MORT','PERS_SAV','10YR','SP500','WTI_OIL','BUSLOANS','CORP_BOND','UNRATE']
        self.series_1_Box.addItems(metrics)
        self.series_2_Box.addItems(metrics)




    def __del__(self):
        sys.stdout = sys.__stdout__

      
    def normalOutputWritten(self,text):
        cursor=self.printOutput.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.printOutput.setTextCursor(cursor)
        self.printOutput.ensureCursorVisible()


    def correlate(self):

        ############PAIRPLOT FUNCTION
        #time slice
        df_slice=self.df1[self.start_dateEdit.date().toPyDate():self.end_dateEdit.date().toPyDate()]
        #filter down to Bedroom##############
        df_pp=df_slice[(df_slice['CountyName']==''+ str(self.countyBox.currentText()) + '') & (df_slice['State']==''+ str(self.stateBox.currentText()) + '')].groupby(['CountyName','State','Bedrooms'])['House Price Index','CASE-SHILLER','CPI','M2','EFFR','30YR_MORT','PERS_SAV','10YR','SP500','WTI_OIL','BUSLOANS','CORP_BOND','UNRATE'].resample('M').mean().dropna()
        #df_pp=df_pp.reset_index(level=-1, drop=True)
        #print(df_pp)

        data_1 = df_pp[''+ str(self.series_1_Box.currentText()) +'']
        data_2 = df_pp[''+ str(self.series_2_Box.currentText()) +'']
        data_1=data_1.reset_index(level=2, drop=True)
        data_1=data_1.reset_index(level=1, drop=True)
        data_1=data_1.reset_index(level=0, drop=True)

        data_2=data_2.reset_index(level=2, drop=True)
        data_2=data_2.reset_index(level=1, drop=True)
        data_2=data_2.reset_index(level=0, drop=True)
        

        df_corr=pd.concat([data_1,data_2], axis=1)
        r, p = stats.pearsonr(df_corr.iloc[:,0],df_corr.iloc[:,1])
        print('Correlation (Pearson) r = ', r)
        #print('P-Value p = ', p)

        self.chloroplethWidget.canvas.axes.cla()
        self.chloroplethWidget.canvas.ax2.cla()
        self.chloroplethWidget.canvas.axes.plot(data_1, marker='o',label=''+ str(self.series_1_Box.currentText()) +'')
        self.chloroplethWidget.canvas.ax2.plot(data_2, marker='.', color = 'green',label=''+ str(self.series_2_Box.currentText()) +'')
        self.chloroplethWidget.canvas.axes.legend()
        self.chloroplethWidget.canvas.ax2.legend()
        #data_1.plot(marker='.', ax=self.chloroplethWidget.canvas.axes)
        #data_2.plot(marker='.', color = 'green',ax=self.chloroplethWidget.canvas.ax2)
        self.chloroplethWidget.canvas.draw()
    
        
      

    def pairplot(self):
       
        ############PAIRPLOT FUNCTION
        #time slice
        df_slice=self.df1[self.start_dateEdit.date().toPyDate():self.end_dateEdit.date().toPyDate()]
        #filter down to Bedroom##############
        df_pp=df_slice[(df_slice['CountyName']==''+ str(self.countyBox.currentText()) + '') & (df_slice['State']==''+ str(self.stateBox.currentText()) + '')].groupby(['CountyName','State','Bedrooms'])['House Price Index','CASE-SHILLER','CPI','M2','EFFR','30YR_MORT','PERS_SAV','10YR','SP500','WTI_OIL','BUSLOANS','CORP_BOND','UNRATE'].resample('M').mean().dropna()
        self.pairplotWidget.canvas.axes.cla()
        pd.plotting.scatter_matrix(df_pp, figsize=(5,5), marker = '.', hist_kwds = {'bins': 20}, s = 60, alpha = 0.6, ax=self.pairplotWidget.canvas.axes)
        self.pairplotWidget.canvas.draw()


    #def heatmap(self):
       
        ############HEATMAP FUNCTION
        #time slice
       # df_slice=self.df1[self.start_dateEdit.date().toPyDate():self.end_dateEdit.date().toPyDate()]
        #filter down to Bedroom##############
      #  df_pp=df_slice[(df_slice['CountyName']==''+ str(self.countyBox.currentText()) + '') & (df_slice['State']==''+ str(self.stateBox.currentText()) + '')].groupby(['CountyName','State','Bedrooms'])['price_index','CASE-SHILLER','CPI','M2','EFFR','30YR_MORT','PERS_SAV','10YR','Adj Close','WTI_OIL','BUSLOANS','CORP_BOND','UNRATE'].resample('M').mean().dropna()
        
                
       # self.heatmapWidget.canvas.axes.cla()
       # img=self.heatmapWidget.canvas.axes.matshow(df_pp.corr())
        #self.heatmapWidget.canvas.axes.set_xticks(range(df_pp.select_dtypes(['number']).shape[1]), df_pp.select_dtypes(['number']).columns)
        #self.heatmapWidget.canvas.axes.set_yticks(range(df_pp.select_dtypes(['number']).shape[1]), df_pp.select_dtypes(['number']).columns)
        #cb=self.heatmapWidget.canvas.axes.colorbar()
        #cb=plt.colorbar(img, ax=self.pairplotWidget.canvas.axes)
        #self.heatmapWidget.canvas.axes.tick_params(labelsize=14)
        #self.heatmapWidget.canvas.axes.title('Correlation Matrix', fontsize=16)
        #self.heatmapWidget.canvas.draw()
        #plt.show()
        
        #f = plt.figure(figsize=(19, 15))
        #plt.matshow(df.corr(), fignum=f.number)
        #plt.xticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14, rotation=45)
        #plt.yticks(range(df.select_dtypes(['number']).shape[1]), df.select_dtypes(['number']).columns, fontsize=14)
        #cb = plt.colorbar()
        #cb.ax.tick_params(labelsize=14)
        #plt.title('Correlation Matrix', fontsize=16);




class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


app=QApplication(sys.argv)
#app.setStyle('Fusion')
window=AppMain()
window.show()
sys.exit(app.exec_())