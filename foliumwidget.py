from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class foliumWidget(QWidget):

    def __init__(self):
        #super().__init__()
        QWidget.__init__(self, parent)
        
        #self.window_width, self.window_height = 1600, 1200
        #self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        coordinate = (37.8199286, -122.4782551)
        m = folium.Map(
            tiles='Stamen Terrain',
            zoom_start=13,
            location=coordinate
        )

        # save map data to data object
        data = io.BytesIO()
        m.save(data, close_file=False)

        webView = QWebEngineView()
        webView.setHtml(data.getvalue().decode())
        layout.addWidget(webView)
