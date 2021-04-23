from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWebEngineWidgets import QWebEngineView
import folium
import io
import json

import os
cwd = os.getcwd()
os.chdir(cwd)

class foliumWidget(QWidget):

    def __init__(self, parent = None):
        #super().__init__()
        QWidget.__init__(self, parent)
        
        layout = QVBoxLayout()
        self.setLayout(layout)

        county_map=r'shapefiles/gz_2010_us_050_00_500k.json'

        

        #coordinate = (37.8199286, -122.4782551)
        m = folium.Map(
            tiles='CartoDB positron',
            location=[48, -102],
            zoom_start=3,            
        )

        #folium.GeoJson(county_map, name="geojson").add_to(m)

        #folium.Choropleth(
         #   geo_data=county_map,
          #  name="choropleth",
           # data=state_data,
           # columns=["State", "Unemployment"],
           # key_on="feature.id",
          #  fill_color="YlGn",
            #fill_opacity=0.7,
           # line_opacity=0.2,
            #legend_name="Median Housing Price Correlations",
        #).add_to(m)

        #folium.TopoJson(
        #    json.loads(requests.get(county_map).text)
        #).add_to(m)

        #folium.LayerControl().add_to(m)

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)