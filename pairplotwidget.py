from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import FigureCanvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

class pairplothWidget(QWidget):

    def __init__(self, parent = None):

        QWidget.__init__(self, parent)

        self.canvas = FigureCanvas(Figure())
        self.toolbar = NavigationToolbar(self.canvas,self)

        vertical_layout = QVBoxLayout()
        vertical_layout.addWidget(self.canvas)
        vertical_layout.addWidget(self.toolbar)


        self.canvas.axes= self.canvas.figure.add_subplot(111)
        self.canvas.ax2= self.canvas.axes.twinx()
        #self.canvas.figure.subplots_adjust(left=0.18, right=0.9, bottom=0.16, top=0.9)
        self.setLayout(vertical_layout)