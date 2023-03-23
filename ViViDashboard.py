import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import * 
from PyQt5.QtWidgets import *


class ViviDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        self.last_update = time.time()
        
        self.population = 0
        self.genesis_name = ["Doo Pond", "Khor Pond"]
        self.genesis_value = ["10", "5"]
        self.genesis_percent = []
        self.pheromone = 0

        self.initUI()

    def


    def update(self):
        self.label_population.setText(str(self.population))  
        self.label_pheromone.setText(str(self.pheromone))

        all_genesis = ""
        for i in range(len(self.genesis_name)):
            all_genesis += self.genesis_name[i] + "   " + self.genesis_value[i] + "\n"

        self.label_genesis.setText(all_genesis)

    def initUI(self):
        self.setWindowTitle('Vivi System Dashboard')
        
        self.setGeometry(100, 100, 583, 554)

        self.widget = QWidget()
        self.widget.setGeometry(10, 20, 583, 554)

        self.verticalLayout = QVBoxLayout()
        self.horizontalLayout = QHBoxLayout()
        
        self.label = QLabel()
        self.label.setText("Population")
        self.horizontalLayout.addWidget(self.label)
        self.label_population = QLabel()
        self.horizontalLayout.addWidget(self.label_population)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.label_genesis = QLabel()
        self.verticalLayout.addWidget(self.label_genesis)

        self.graphicsView = PlotWidget()
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        

        self.verticalLayout_2 = QVBoxLayout()
        self.horizontalLayout_2 = QHBoxLayout()

        self.label_3 = QLabel()
        self.label_3.setText("Pheromone")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.label_pheromone = QLabel()
        self.horizontalLayout_2.addWidget(self.label_pheromone)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.label_6 = QLabel()
        self.label_6.setText("Constants\n"
"     Population       100000\n"
"     Display Limit   300\n"
"     Birth Rate        1x")
        self.verticalLayout_2.addWidget(self.label_6)

        self.graphicsView_2 = PlotWidget()
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.verticalLayout_2.addWidget(self.graphicsView_2)

        self.verticalLayout_2.setStretch(1, 1)
        self.verticalLayout_2.setStretch(2, 5)

        self.layout = QHBoxLayout()
        self.layout.addLayout(self.verticalLayout)
        self.layout.addLayout(self.verticalLayout_2)
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)
        
        self.show()   

        return

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ViviDashboard()
    window.update()
    sys.exit(app.exec())