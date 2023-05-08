from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea, QApplication,
                             QHBoxLayout, QGroupBox, QGridLayout, QVBoxLayout, QMainWindow, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets, uic, QtGui
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QPainter, QColor, QFont
import sys

from FishFrame import FishFrame
from PondFrame import PondFrame


class ViviDashboard(QMainWindow):

    def __init__(self, connectedPonds, myPond=None):
        super().__init__()
        self.connectedPonds = connectedPonds
        self.myPond = myPond
        self.listedPonds = []
        # print(self.fishes[0].getId())
        self.initUI()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updatePond)
        self.timer.start(500)

    def updatePond(self):
        for pondFrame in self.widget.findChildren(PondFrame):
            pondName = pondFrame.name.text().split(": ")[1]
            if self.myPond.name == pondName:
                info = [self.myPond.name, len(
                    self.myPond.fishes), self.myPond.pheromone]
                pondFrame.updateInfo(info)
                continue
            for pond in self.connectedPonds:
                if pond.name == pondName:
                    info = [pond.name, pond.total_fishes, pond.pheromone]
                    pondFrame.updateInfo(info)
                    break

    def initUI(self):

        # Scroll Area which contains the widgets, set as the centralWidget
        self.scroll = QScrollArea()
        self.widget = QWidget()         # Widget that contains the collection of Vertical Box
        # The Vertical Box that contains the Horizontal Boxes of  labels and buttons
        self.vbox = QVBoxLayout()

        label = QLabel("Vividashboard", self)
        font = label.font()
        font.setPointSize(20)
        font.setBold(True)
        label.setFont(font)
        label.setStyleSheet("padding-left: 20px; color: white;")
        self.vbox.addWidget(label)

        if self.myPond:
            info = [self.myPond.name, len(
                self.myPond.fishes), self.myPond.pheromone]
            self.listedPonds.append(self.myPond.name)
            self.vbox.addWidget(PondFrame(info, self.widget))

        for pond in self.connectedPonds:
            info = [pond.name, pond.total_fishes, pond.pheromone]
            self.listedPonds.append(pond.name)
            self.vbox.addWidget(PondFrame(info, self.widget))

        self.updatePond()

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.scroll)
        self.setStyleSheet("background-color: #2A9A5D;")
        self.setGeometry(0, 290, 400, 300)
        self.setWindowTitle('ViviDashboard')
        self.show()

        return
