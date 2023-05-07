# from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
#                              QHBoxLayout, QGroupBox, QGridLayout, QVBoxLayout, QMainWindow, QFrame)
# from PyQt5.QtCore import Qt, QSize
# from PyQt5 import QtWidgets, uic, QtGui
# import sys

# from FishFrame import FishFrame


# class Dashboard(QMainWindow):

#     def __init__(self, allFish=None, allPondsNum=None):
#         super().__init__()
#         self.fished = allFish
#         self.allPondsNum = allPondsNum
#         # print(self.fished[0].getId())
#         self.initUI()

#     def initUI(self):

#         # Scroll Area which contains the widgets, set as the centralWidget
#         self.scroll = QScrollArea()
#         self.widget = QWidget()         # Widget that contains the collection of Vertical Box
#         # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
#         self.vbox = QVBoxLayout()
#         self.grid = QGridLayout()

#         # temp = ["Fish ID: 123", "State: In Pond", "Status: alive", "Genesis: Sick-Salmon", "Crowd Threshold: 5/10", "Pheromone Level: 4/5", "Lifetime: 30/60"]
#         # print(self.fished[0].getFishData().getGenesis())
#         num = len(self.fished)
#         j = 0
#         temp = 0
#         i = 0
#         label = QLabel("Pond Population : " + str(len(self.fished)) + "/" + str(self.allPondsNum) +
#                        " (" + str(int((len(self.fished)/self.allPondsNum) * 100)) + "%)", self)
#         font = label.font()
#         font.setPointSize(30)
#         font.setBold(True)
#         label.setFont(font)
#         for r in range(0, num):
#             # print("out", i, temp, j)
#             while j < 2 and i < num:
#                 # print("here", i, temp, j)
#                 info = [self.fished[i].getFishData().getId(), self.fished[i].getFishData().getState(),
#                         self.fished[i].getFishData().getStatus(), self.fished[i].getFishData().getGenesis(), str(self.fished[i].getFishData().lifetime)]
#                 self.grid.addWidget(FishFrame(info, self.widget), temp, j)
#                 i += 1
#                 j += 1
#             j = 0
#             temp += 1

#         self.vbox.addWidget(label)
#         self.vbox.addLayout(self.grid)

#         self.widget.setLayout(self.vbox)

#         # Scroll Area Properties
#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
#         self.scroll.setWidgetResizable(True)
#         self.scroll.setWidget(self.widget)

#         self.setCentralWidget(self.scroll)

#         self.setGeometry(0, 290, 500, 700)
#         self.setWindowTitle('Dashboard')
#         self.show()

#         return

from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QGroupBox, QGridLayout, QVBoxLayout, QMainWindow, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, uic, QtGui
import sys

from FishFrame import FishFrame


class Dashboard(QMainWindow):

    def __init__(self, myPond=None, allPondsNum=None):
        super().__init__()
        self.fished = myPond.fishes
        self.allPondsNum = allPondsNum
        # print(self.fished[0].getId())
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePopulation)
        self.timer.start(500)

    def updatePopulation(self):
        num = len(self.fished)
        i = 0
        temp = 0
        j = 0

        newPopulationLabel = "Population : " + str(len(self.fished)) + "/" + str(
            len(self.fished)) + " (" + str(int((len(self.fished)/len(self.fished)) * 100)) + "%)"
        self.label.setText(newPopulationLabel)
        # Clear the grid layout before adding the updated fish frames
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            widget.setParent(None)
            self.grid.removeItem(self.grid.itemAt(i))

        for r in range(0, num):
            while j < 2 and i < num:
                info = [self.fished[i].getFishData().getId(), self.fished[i].getFishData().getState(),
                        self.fished[i].getFishData().getStatus(), self.fished[i].getFishData().getGenesis(), str(self.fished[i].getFishData().lifetime)]
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

        # temp = ["Fish ID: 123", "State: In Pond", "Status: alive", "Genesis: Sick-Salmon", "Crowd Threshold: 5/10", "Pheromone Level: 4/5", "Lifetime: 30/60"]
        # print(self.fished[0].getFishData().getGenesis())
        num = len(self.fished)
        j = 0
        temp = 0
        i = 0
        self.label = QLabel("Population : " + str(len(self.fished)) + "/" + str(self.allPondsNum) +
                            " (" + str(int((len(self.fished)/self.allPondsNum) * 100)) + "%)", self)
        font = self.label.font()
        font.setPointSize(20)
        font.setBold(True)
        self.label.setFont(font)
        for r in range(0, num):
            # print("out", i, temp, j)
            while j < 2 and i < num:
                # print("here", i, temp, j)
                info = [self.fished[i].getFishData().getId(), self.fished[i].getFishData().getState(),
                        self.fished[i].getFishData().getStatus(), self.fished[i].getFishData().getGenesis(), str(self.fished[i].getFishData().lifetime)]
                self.grid.addWidget(FishFrame(info, self.widget), temp, j)
                i += 1
                j += 1
            j = 0
            temp += 1

        self.vbox.addWidget(self.label)
        self.vbox.addLayout(self.grid)
        self.updatePopulation()

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(0, 290, 500, 700)
        self.setWindowTitle('Dashboard')
        self.show()

        return
