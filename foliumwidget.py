from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout
from PyQt5 import QtCore, QtWidgets, QtWebEngineWidgets
import folium
import io
import pandas as pd
import os


class foliumWidget(QWidget):

    def __init__(self, parent = None):
        #super().__init__()
        QWidget.__init__(self, parent)

        layout = QVBoxLayout()
        self.setLayout(layout)

                  
        state_data = r'shapefiles/us_county_data.csv'
        us_geo = r'shapefiles/us-states.json'
        
        df = pd.read_csv(state_data, na_values=[" "])

        df_min=pd.DataFrame()
        df_min=df.groupby('State', as_index=False)['Unemployment_rate_2011'].mean()
        


        m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

       # bins = list(df_min["Unemployment_rate_2011"].quantile([0, 0.25, 0.5, 0.75, 1]))

        choropleth = folium.Choropleth(
            geo_data= us_geo,
            name="choropleth",
            data=df_min,
            columns=["State","Unemployment_rate_2011"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.1,
            legend_name="Unemployment_rate_2011",
         #   bins=bins,
            reset=True,
        ).add_to(m)

     #   choropleth.geojson.add_child(
      #      folium.features.GeoJsonTooltip(['State'])
       #     )


        #folium.LayerControl().add_to(m)
        data = io.BytesIO()
        m.save(data, close_file=False)


        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)
