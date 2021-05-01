from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import folium
from folium.plugins.draw import Draw
import io
import pandas as pd
import branca
import json
import requests
import os


class foliumWidget(QWidget):

    def __init__(self, parent = None):
        #super().__init__()
        QWidget.__init__(self, parent)


        #layout = QVBoxLayout()
        #self.setLayout(layout)

        self.view = QtWebEngineWidgets.QWebEngineView()

        county_map=r'shapefiles/new.geojson'
        #county_map=r'shapefiles/gz_2010_us_050_00_500k.json'
        
       
        county_data = r'shapefiles/us_county_data.csv'
        #county_geo = r'shapefiles/gz_2010_us_outline_500k.json'
        county_geo = r'shapefiles/cb_2018_us_county_20m.geojson'
        
        
        df = pd.read_csv(county_data, na_values=[" "])
        df["FIPS_Code"] = df["FIPS_Code"].astype(str)

        m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

        bins = list(df["Median_Household_Income_2011"].quantile([0, 0.25, 0.5, 0.75, 1]))

        folium.Choropleth(
            geo_data= county_geo,
            name="choropleth",
            data=df,
            columns=["FIPS_Code","Median_Household_Income_2011"],
            key_on="properties.GEOID",
            fill_color="YlGnBu",
            fill_opacity=0.7,
            line_opacity=0.5,
            legend_name="Unemployment Rate (%)",
            bins=bins,
            #reset=True,
        ).add_to(m)
        





        tmp_file = QtCore.QTemporaryFile("XXXXXX.html", self)
        if tmp_file.open():
            m.save(tmp_file.fileName())
            url = QtCore.QUrl.fromLocalFile(tmp_file.fileName())
            self.view.load(url)

        lay = QtWidgets.QVBoxLayout(self)
        lay.addWidget(self.view)
        




  

        #m.add_child(folium.LayerControl())#.add_to(m)
        #data = io.BytesIO()
        #m.save(data, close_file=False)

  
        

        #webView = QWebEngineView()
        #webView.setHtml(data.getvalue().decode())
        
        #layout.addWidget(webView)
