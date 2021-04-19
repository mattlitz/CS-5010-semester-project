import sys
import os

#os.environ['QT_QPA_PLATFORM']='offscreen'
#os.environ['QT_STYLE_OVERRIDE']='0'

import numpy as np
import pandas as pd
import seaborn as sns
import geopandas as gpd
import matplotlib.pyplot as plt
import folium

from PyQt5 import *
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import*
from PyQt5 import QtCore,QtGui,QtWidgets, QtWebEngineWidgets
#from PyQt5.QtGui import QPixmap


from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures #OneHotEncoder #categorical data
from sklearn.metrics import mean_squared_error, make_scorer, accuracy_score

import warnings
warnings.filterwarnings('ignore')

from chloroplethwidget import chloroplethWidget

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
        self.exitButton.clicked.connect(self.close)

        #sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
       
        #initialize data sets
        #self.alloy_comboBox.addItem("Ti-6Al-4V")
        #self.alloy_comboBox.addItem("Mg AZ80A")


    def correlate(self):

              
        #code for calculating chloropleth
        csa = gpd.read_file('shapefiles/cb_2018_us_csa_20m.shp')
        states = gpd.read_file('shapefiles/cb_2018_us_state_20m.shp')

        csa = csa.to_crs("EPSG:3395")
        states = states.to_crs("EPSG:3395")
        

        #Alaska and Hawaii excluded due to lack of CSA
        states=states[states['NAME'] != 'Alaska']
        states=states[states['NAME'] != 'Hawaii']

        us_boundary_map = states.boundary.plot(figsize=(5, 5),color="Black", linewidth=.1)


        self.chloroplethWidget.canvas.axes.cla()
        
        #self.chloroplethWidget.canvas.axes.us_boundary_map
        #self.chloroplethWidget.canvas.axes.states.boundary.plot(color="Black", linewidth=.1)
        self.chloroplethWidget.canvas.axes.plot(ax=us_boundary_map, cmap='magma', data=csa)
        self.chloroplethWidget.canvas.axes.toolbar = NavigationToolbar(self.chloroplethWidget.canvas, self)
        self.chloroplethWidget.canvas.draw()
        
        #Merge the cases data to the spatial data
        #new_df=data.merge(states, how='left', on='MSA')

        #Plot metrics on map
        #ax = new_df.dropna().plot(column='cases', cmap='coolwarm', figsize=(15,9), k=3, legend=True)

        #print(cbsa)
        #csa[csa['NAME'] == 'Des Moines-Ames-West Des Moines, IA'].plot(figsize=(12, 12))



app=QApplication([])
window=AppMain()
window.show()
app.exec()