import io
import os
from pathlib import Path

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

import folium
import pandas as pd

class foliumWidget(QWidget):

    def __init__(self, parent = None):
        #super().__init__()
        QWidget.__init__(self, parent)

        layout = QVBoxLayout(self)

                  
        state_data = r'UserInterface/shapefiles/US_Unemployment_Oct2012.csv'
        us_geo = r'UserInterface/shapefiles/us-states.json'
        
        df = pd.read_csv(state_data, na_values=[" "])
      

        m = folium.Map(location=[48, -102], tiles="cartodbpositron", zoom_start=3)

        bins = list(df["Unemployment"].quantile([0, 0.25, 0.5, 0.75, 1]))

        choropleth = folium.Choropleth(
            geo_data= us_geo,
            name="choropleth",
            data=df,
            columns=["State","Unemployment"],
            key_on="feature.id",
            fill_color="PuRd",
            fill_opacity=0.7,
            line_opacity=0.1,
            legend_name="Unemployment",
            bins=bins,
            reset=True,
        ).add_to(m)

        choropleth.geojson.add_child(folium.features.GeoJsonTooltip(["name"]))

        #folium.LayerControl().add_to(m)
        webView = QWebEngineView()
        layout.addWidget(webView)

        data = io.BytesIO()
        m.save(data, close_file=False)
        webView.setHtml(data.getvalue().decode())
