import sys
import os
import numpy as np
import pandas as pd
import seaborn as sns
import geopandas
import matplotlib.pyplot as plt

from PyQt5 import*
from PyQt5.uic import loadUi
from PyQt5.QtWidgets import*
from PyQt5 import QtCore,QtGui,QtWidgets
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from sklearn.linear_model import LassoCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, PolynomialFeatures #OneHotEncoder #categorical data
from sklearn.metrics import mean_squared_error, make_scorer, accuracy_score

import warnings
warnings.filterwarnings('ignore')

from chloroplethwidget import ChloroplethWidget
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure

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

        self.calculateButton.clicked.connect(self.calculate)
        self.exitButton.clicked.connect(self.close)

        #sys.stdout = EmittingStream(textWritten=self.normalOutputWritten)
       
        #initialize data sets
        #self.alloy_comboBox.addItem("Ti-6Al-4V")
        #self.alloy_comboBox.addItem("Mg AZ80A")


    def calculate(self):
        
        #code for calculating chloropleth
        csa = geopandas.read_file('shapefiles/cb_2018_us_csa_20m.shp')
        states = geopandas.read_file('shapefiles/cb_2018_us_state_20m.shp')

        csa = csa.to_crs("EPSG:3395")
        states = states.to_crs("EPSG:3395")
        

        #Alaska and Hawaii excluded due to lack of CSA
        states=states[states['NAME'] != 'Alaska']
        states=states[states['NAME'] != 'Hawaii']

        us_boundary_map = states.boundary.plot(figsize=(18, 12),color="Black", linewidth=.1)


        self.ChloroplethWidget.canvas.axes.cla()
        self.ChloroplethWidget.canvas.axes.states.boundary.plot(figsize=(18, 12),color="Black", linewidth=.1)
        self.ChloroplethWidget.canvas.axes.csa.plot(ax=us_boundary_map, cmap='magma')
        self.ChloroplethWidget.canvas.draw()
        
        #Merge the cases data to the spatial data
        #new_df=data.merge(states, how='left', on='MSA')

        #Plot metrics on map
        #ax = new_df.dropna().plot(column='cases', cmap='coolwarm', figsize=(15,9), k=3, legend=True)

        #print(cbsa)
        #csa[csa['NAME'] == 'Des Moines-Ames-West Des Moines, IA'].plot(figsize=(12, 12))


class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))


app=QApplication([])
window=AppMain()
window.show()
app.exec()