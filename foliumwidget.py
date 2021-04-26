from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog, QHBoxLayout, QVBoxLayout
import folium
from folium.plugins.draw import Draw
import io

class foliumWidget(QWidget):

    def __init__(self, parent = None):
        #super().__init__()
        QWidget.__init__(self, parent)


        layout = QVBoxLayout()
        self.setLayout(layout)

        county_map=r'shapefiles/cb_2017_us_county_20m.json'
        #county_map=r'shapefiles/gz_2010_us_050_00_500k.json'
       

        

        #coordinate = (37.8199286, -122.4782551)
        m = folium.Map(
            tiles='CartoDB positron',
            location=[48, -102],
            zoom_start=2,            
        )

        #folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)

        geo_json = folium.GeoJson(county_map, name="geojson")#.add_to(m)
        

        #folium.GeoJson(open(county_map).read()).add_to(m)
        #layer=folium.GeoJson(county_map, name="geojson").add_to(m)

        #layer = folium.GeoJson(
        #    data=(open(county_map, "r").read()),
        #    name='geojson',
        #).add_to(m) # 1. keep a reference to GeoJSON layer

       # folium.TopoJson(
        #    open(county_map)).add_to(m)

        #folium.Choropleth(open(county_map)).add_to(m)

        #folium.Choropleth(geo_data=county_map).add_to(m)

      #  folium.Choropleth(
          #  geo_data=county_map,
           # name="choropleth",
           # data=state_data,
           # columns=["State", "Unemployment"],
           # key_on="feature.id",
            #fill_color="YlGn",
            #fill_opacity=0.7,
           # line_opacity=0.2,
            #legend_name="Median Housing Price Correlations",
       # ).add_to(m)

      #  folium.TopoJson(
          #  json.loads(requests.get(county_map).text),
         #   "objects.cb_2018_us_county_20m",
        #).add_to(m)

        #m.add_child(c)
        #m.keep_in_front(c)

        #m.add_child(folium.GeoJson(data = open(county_map)))

        #geojson_layer = folium.GeoJson(county_map,
                        #       name='geojson')

        #geojson_layer.add_to(m)

        

        # save map data to data object

        #m.fit_bounds(layer.get_bounds())

        geo_json.add_to(m)
        #m.add_child(geo_json)

        m.add_child(folium.LayerControl())#.add_to(m)
        data = io.BytesIO()
        m.save(data, close_file=False)

  
        

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())

        
        layout.addWidget(webView)

        #self.interceptor = Interceptor()
        #webView.page().profile().setUrlRequestInterceptor(self.interceptor)


