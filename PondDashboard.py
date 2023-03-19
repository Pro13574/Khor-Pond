from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QGroupBox, QGridLayout, QVBoxLayout, QMainWindow, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic, QtGui
import sys

from PondFrame import PondFrame


class PondDashboard(QMainWindow):

    def __init__(self, allPond=None):
        super().__init__()
        self.ponds = allPond
        self.initUI()

    def initUI(self):

        # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll = QScrollArea()
        self.widget = QWidget()         # Widget that contains the collection of Vertical Box
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox = QVBoxLayout()
        self.grid = QGridLayout()

        # temp = ["Fish ID: 123", "State: In Pond", "Status: alive", "Genesis: Sick-Salmon", "Crowd Threshold: 5/10", "Pheromone Level: 4/5", "Lifetime: 30/60"]
        # print(self.fishe[0].getFishData().getGenesis())
        # num = len(self.fished)
        num = len(self.ponds)

        i, j, temp = 0, 0, 0
        for r in range(0, num):
            # print("out", i, temp, j)
            while j < 2 and i < num:
                # print("here", i, temp, j)
                info = [self.ponds[i].getPondName(
                ), self.ponds[i].getPopulation(), self.ponds[i].fishes]
                self.grid.addWidget(PondFrame(info, self.widget), temp, j)
                i += 1
                j += 1
            j = 0
            temp += 1

        self.widget.setLayout(self.grid)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)

        self.setGeometry(0, 20, 800, 200)
        self.setWindowTitle('Pond Dashboard')
        self.show()

        return