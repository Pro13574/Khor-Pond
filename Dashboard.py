from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QGroupBox, QGridLayout, QVBoxLayout, QMainWindow, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QColor, QFont
import sys

from FishFrame import FishFrame


class Dashboard(QMainWindow):

    def __init__(self, myPond: str = None):
        super().__init__()
        self.myPond = myPond
        self.fishes = myPond.fishes
        self.allPondsFishes = 0
        # print(self.fishes[0].getId())
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePopulation)
        self.timer.start(500)

    def updateAllFishes(self):
        self.allPondsFishes = 0
        self.allPondsFishes += len(self.myPond.fishes)
        for pond in self.myPond.connectedPonds:
            self.allPondsFishes += pond.total_fishes

    def updatePopulation(self):
        self.updateAllFishes()
        num = len(self.fishes)
        i = 0
        temp = 0
        j = 0

        newPopulationLabel = "Khor-Pond Population : " + str(len(self.fishes)) + "/" + str(
            self.allPondsFishes) + " (" + str(len(self.fishes)/self.allPondsFishes * 100) + "%)"
        self.label.setText(newPopulationLabel)
        # Clear the grid layout before adding the updated fish frames
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            widget.setParent(None)
            self.grid.removeItem(self.grid.itemAt(i))

        for r in range(0, num):
            while j < 4 and i < num:
                info = [self.fishes[i].getFishData().getId(), self.fishes[i].getFishData().getState(),
                        self.fishes[i].getFishData().getStatus(), self.fishes[i].getFishData().getGenesis(), str(self.fishes[i].getFishData().lifetime)]
                self.grid.addWidget(FishFrame(info, self.widget), temp, j)
                i += 1
                j += 1
            j = 0
            temp += 1

    def initUI(self):

        # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll = QScrollArea()
        self.widget = QWidget()         # Widget that contains the collection of Vertical Box
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()
        self.series = QPieSeries()

        self.updateAllFishes()

        fishPercentage = len(self.myPond.fishes) / self.allPondsFishes * 100
        slice = QPieSlice(self.myPond.name +
                          str(fishPercentage) + "%", fishPercentage)
        self.series.append(slice)
        for pond in self.myPond.connectedPonds:
            fishPercentage = len(
                self.myPond.fishes)/self.allPondsFishes * 100
            slice = QPieSlice(
                pond + str(fishPercentage) + "%", fishPercentage)
            self.series.append(slice)

        self.series.setLabelsVisible(True)

        chart = QChart()
        chart.addSeries(self.series)
        chart.setTitle("Pond Distribution")

        chartView = QChartView(chart)
        chartView.setRenderHint(QPainter.Antialiasing)
        chartView.setFixedSize(1000, 400)

        # temp = ["Fish ID: 123", "State: In Pond", "Status: alive", "Genesis: Sick-Salmon", "Crowd Threshold: 5/10", "Pheromone Level: 4/5", "Lifetime: 30/60"]
        # print(self.fishes[0].getFishData().getGenesis())
        num = len(self.fishes)
        j = 0
        temp = 0
        i = 0
        self.label = QLabel("Khor-Pond Population : " + str(len(self.fishes)) + "/" + str(
            self.allPondsFishes) + " (" + str(len(self.fishes)/self.allPondsFishes * 100) + "%)", self)
        font = self.label.font()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet("padding-left: 20px; color: white;")

        for r in range(0, num):
            # print("out", i, temp, j)
            while j < 4 and i < num:
                # print("here", i, temp, j)
                info = [self.fishes[i].getFishData().getId(), self.fishes[i].getFishData().getState(),
                        self.fishes[i].getFishData().getStatus(), self.fishes[i].getFishData().getGenesis(), str(self.fishes[i].getFishData().lifetime)]
                self.grid.addWidget(FishFrame(info, self.widget), temp, j)
                i += 1
                j += 1
            j = 0
            temp += 1

        self.vbox.addWidget(self.label)
        self.vbox.addWidget(chartView)
        self.vbox.addLayout(self.grid)
        self.updatePopulation()

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        self.setStyleSheet("background-color: #344A94;")
        self.setGeometry(0, 290, 1040, 700)
        self.setWindowTitle('Dashboard')
        self.show()

        return
