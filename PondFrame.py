from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize


class PondFrame(QGroupBox):

    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.name = QLabel()
        self.totalFishes = QLabel()
        self.pheromone = QLabel()
        self.name.setStyleSheet(
            "color: white; font-size: 16px; font-weight: 700;")
        self.totalFishes.setStyleSheet(
            "color: white; font-size: 16px; font-weight: 700;")
        self.pheromone.setStyleSheet(
            "color: white; font-size: 16px; font-weight: 700;")
        self.setLayout(self.vbox)
        self.addInfo(info)

    def addInfo(self, info):
        label = QLabel(self)
        self.addLabel(label)
        self.name.setText("Pond Name: " + info[0])
        self.totalFishes.setText("Fishes in the pond: " + str(info[1]))
        self.pheromone.setText("Pheromone: " + str(info[2]))
        self.addLabel(self.name)
        self.addLabel(self.totalFishes)
        self.addLabel(self.pheromone)

    def addLabel(self, widget):
        self.vbox.addWidget(widget)

    def updateInfo(self, info):
        self.totalFishes.setText("Fishes in the pond: " + str(info[1]))
        self.pheromone.setText("Pheromone: " + str(info[2]))
