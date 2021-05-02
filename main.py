import sys
import os


#os.environ['QT_QPA_PLATFORM']='offscreen'
#os.environ['QT_STYLE_OVERRIDE']='0'

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
   #     self.pairplotButton.clicked.connect(self.pairplot)
        self.exitButton.clicked.connect(self.close)

        sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
       
        #initialize FRED data sets
        self.combo_FRED_1.addItem("SP500")
        self.combo_FRED_1.addItem("WM1NS") #M1 Stock
        self.combo_FRED_1.addItem("CSUSHPISA") #S&P/Case-Shiller U.S. National Home Price Index
        self.combo_FRED_1.addItem("CPIAUCSL") #Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
        self.combo_FRED_1.addItem("WM2NS") #M2 Money Stock
        self.combo_FRED_1.addItem("EFFR") #Effective Federal Funds Rate
        self.combo_FRED_1.addItem("DGS10") #10-Year Treasury Constant Maturity Rate
        self.combo_FRED_1.addItem("UNRATE") #Unemployment Rate maybe look at CA?
        self.combo_FRED_1.addItem("MORTGAGE30US") #30-Year Fixed Rate Mortgage Average in the United States
        self.combo_FRED_1.addItem("USD3MTD156N") #3-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar
        self.combo_FRED_1.addItem("MEHOINUSA672N") #Real Median Household Income in the United States
        self.combo_FRED_1.addItem("PSAVERT") #Personal Saving Rate
        self.combo_FRED_1.addItem("DCOILWTICO") #Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma
        self.combo_FRED_1.addItem("GFDEBTN") #Federal Debt: Total Public Debt
        self.combo_FRED_1.addItem("BUSLOANS") #Commercial and Industrial Loans, All Commercial Banks
        self.combo_FRED_1.addItem("DAAA") #Moody's Seasoned Aaa Corporate Bond Yield

        #initialize FRED data sets
        self.combo_FRED_2.addItem("SP500")
        self.combo_FRED_2.addItem("WM1NS") #M1 Stock
        self.combo_FRED_2.addItem("CSUSHPISA") #S&P/Case-Shiller U.S. National Home Price Index
        self.combo_FRED_2.addItem("CPIAUCSL") #Consumer Price Index for All Urban Consumers: All Items in U.S. City Average
        self.combo_FRED_2.addItem("WM2NS") #M2 Money Stock
        self.combo_FRED_2.addItem("EFFR") #Effective Federal Funds Rate
        self.combo_FRED_2.addItem("DGS10") #10-Year Treasury Constant Maturity Rate
        self.combo_FRED_2.addItem("UNRATE") #Unemployment Rate maybe look at CA?
        self.combo_FRED_2.addItem("MORTGAGE30US") #30-Year Fixed Rate Mortgage Average in the United States
        self.combo_FRED_2.addItem("USD3MTD156N") #3-Month London Interbank Offered Rate (LIBOR), based on U.S. Dollar
        self.combo_FRED_2.addItem("MEHOINUSA672N") #Real Median Household Income in the United States
        self.combo_FRED_2.addItem("PSAVERT") #Personal Saving Rate
        self.combo_FRED_2.addItem("DCOILWTICO") #Crude Oil Prices: West Texas Intermediate (WTI) - Cushing, Oklahoma
        self.combo_FRED_2.addItem("GFDEBTN") #Federal Debt: Total Public Debt
        self.combo_FRED_2.addItem("BUSLOANS") #Commercial and Industrial Loans, All Commercial Banks
        self.combo_FRED_2.addItem("DAAA") #Moody's Seasoned Aaa Corporate Bond Yield

        year=['2010','2011','2012','2013','2014','2015','2016','2017','2018','2019','2020','2021']

        self.comboYearStart.addItems(year)
        self.comboYearEnd.addItems(year)



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
        year_start = datetime.strptime(self.comboYearStart.currentText(), '%Y')
        year_end = datetime.strptime(self.comboYearEnd.currentText(), '%Y')

        fred_1 = Fred(api_key='d7f545fe7858da4279909dd26a7b28cc')
        fred_2 = Fred(api_key='d7f545fe7858da4279909dd26a7b28cc')

        
        data_1 = fred_1.get_series(''+ str(self.combo_FRED_1.currentText()) +'', observation_start=''+ str(year_start.date()) +'', observation_end=''+ str(year_end.date()) +'')
        data_2 = fred_2.get_series(''+ str(self.combo_FRED_2.currentText()) +'', observation_start=''+ str(year_start.date()) +'', observation_end=''+ str(year_end.date()) +'')
        
        df=pd.concat([data_1,data_2], axis=1).resample('M').mean().dropna()
        r, p = stats.pearsonr(df.iloc[:,0],df.iloc[:,1])
        print(r)
        print(p)
           

        self.chloroplethWidget.canvas.axes.cla()
        self.chloroplethWidget.canvas.ax2.cla()
        self.chloroplethWidget.canvas.axes.plot(data_1, marker='.')
        self.chloroplethWidget.canvas.ax2.plot(data_2, marker='.', color = 'green')
        self.chloroplethWidget.canvas.axes.set(title=f"Correlation (Pearson) r = {r}")
        self.chloroplethWidget.canvas.draw()
        
        #Merge the cases data to the spatial data
        #new_df=data.merge(states, how='left', on='MSA')

        #Plot metrics on map
        #ax = new_df.dropna().plot(column='cases', cmap='coolwarm', figsize=(15,9), k=3, legend=True)

        #print(cbsa)
        #csa[csa['NAME'] == 'Des Moines-Ames-West Des Moines, IA'].plot(figsize=(12, 12))


  #   def pairplot(self):



class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


app=QApplication(sys.argv)
#app.setStyle('Fusion')
window=AppMain()
window.show()
sys.exit(app.exec_())