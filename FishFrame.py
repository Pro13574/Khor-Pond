from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QSize


class FishFrame(QGroupBox):

    def __init__(self, info, parent=None):
        super().__init__(parent)
        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.vbox.addLayout(self.hbox)
        self.info = []
        self.setLayout(self.vbox)
        self.addInfo(info)

    def addInfo(self, info):
        low_rez = QSize(100, 100)
        pixmap = QPixmap('./assets/images/sprites/local-pond/1.png')
        label = QLabel(self)

        if info[3].lower() == "khor-pond":
            pixmap = QPixmap('./assets/images/sprites/local-pond/1.png')
        elif info[3].lower() == "peem":
            pixmap = QPixmap('./assets/images/sprites/foreign-pond/1.png')
        elif info[3].lower() == "dang":
            pixmap = QPixmap('./assets/images/sprites/dang.png')
        elif info[3].lower() == "pla":
            pixmap = QPixmap('./assets/images/sprites/plafish.png')

        pixmap = pixmap.scaled(low_rez)
        label.setPixmap(pixmap)
        self.addLabel(label)
        self.info.append(QLabel("ID: " + str(info[0])))
        self.info.append(QLabel("State: " + str(info[1])))
        self.info.append(QLabel("Status: " + str(info[2])))
        self.info.append(QLabel("Genesis: " + str(info[3])))
        self.info.append(QLabel("Lifetime: " + str(info[4])))

        for label in self.info:
            label.setStyleSheet("color: white; font-weight: 700;")
            self.addLabel(label)

    def addLabel(self, widget):
        self.vbox.addWidget(widget)
