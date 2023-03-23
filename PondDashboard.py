# import random
# import time
# from typing import DefaultDict, Dict

# from PyQt5.QtCore import Qt

# import sys
# from PyQt5 import QtGui, QtWidgets, uic
# from PyQt5.QtCore import QSize, Qt
# from PyQt5.QtGui import * 
# from PyQt5.QtWidgets import * 

# from fish import FishGroup
# from FishFrame import FishFrame
# from collections import namedtuple


# class Dashboard(QMainWindow):
#     def __init__(self, fishes: FishGroup):
#         super().__init__()
#         self.fishes: FishGroup = fishes
#         self.last_updated = time.time()
#         self.label = QLabel(self)
#         self.label.setFont(QFont('Arial',12))

#         self.sliceColors = ["#82d3e5", "#cfeef5", "#fd635c", "#fdc4c1",
#                             "#feb543", "#ffe3b8", "#CCCCFF", "#40E0D0", "#9FE2BF", "#FFA07A"]
#         self.PieData = namedtuple(
#             'Data', ['name', 'value', 'primary_color', 'secondary_color'])
#         percentages = self.fishes.get_percentages()
#         self.create_piechart(percentages)

#         self.colors = [
#             (255, 0, 0),
#             (0, 255, 0),
#             (0, 0, 255),
#         ]
#         self.lines = {}
#         self.initUI()

#     def update_dashboard(self, pheromone: int):
#         current_time = time.time()
#         if current_time - self.last_updated < 2:
#             return
#         self.last_updated = current_time

#         percentages = self.fishes.get_percentages()
#         percentages_str = ""
#         for genesis, p in percentages.items():
#             percentages_str += f"{genesis}: {p * 100:.2f}%\n"

#         label_str = (
#             "Pond Population : " +
#             str(self.fishes.get_total()) + "\n" + percentages_str + "\n"
#         )
#         label_str += f"Pond Pheremone: {pheromone}\n"

#         label_str += f"\nConstants:\n \tPopulation Limit: {consts.FISHES_POND_LIMIT}\n"
#         label_str += f"\tDisplay Limit: {consts.FISHES_DISPLAY_LIMIT}\n"
#         label_str += f"\tBirth Rate: {consts.BIRTH_RATE}x\n"

#         fish_list = self.fishes.getFishes()

#         self.label.setText(label_str)
#         self.update_history_graph()
#         self.create_piechart(percentages)
#         self.createFishFrame(fish_list)
    
#     def createFishFrame(self,fish_list):
#         #delete old frames
#         for i in reversed(range(self.grid.count())):
#             widget = self.grid.itemAt(i).widget()
#             self.grid.removeWidget(widget)
#             widget.setParent(None)

#         temp = 3
#         j = 0
#         for i in range(len(fish_list)):
#             fish_list[i].updateLifeTime()
#             info = [
#                 fish_list[i].getFishData().getId(),
#                 fish_list[i].getFishData().getState(),
#                 fish_list[i].getFishData().getStatus(),
#                 fish_list[i].getFishData().getGenesis(),
#                 fish_list[i].getFishData().getLifeTimeLeft()
#             ]
#             self.grid.addWidget(FishFrame(info, self.widget), temp, j)
#             # temp +=1
#             j+=1
#             if j>3:
#                 j = 0
#                 temp+=1


#     def initUI(self):

#         self.scroll = (
#             QScrollArea()
#         )  # Scroll Area which contains the widgets, set as the centralWidget

#         self.widget = QWidget()  # Widget that contains the collection of Vertical Box

#         self.vbox = QVBoxLayout()
#         self.h_layout1 = QHBoxLayout()
#         self.grid = QGridLayout()

#         # temp = ["Fish ID: 123", "State: In Pond", "Status: alive", "Genesis: matrix-fish", "Crowd Threshold: 5/10", "Pheromone Level: 4/5", "Lifetime: 30/60"]

#         # print(self.fished[0].getFishData().getGenesis())

#         num = len(self.fishes)

#         font = self.label.font()

#         font.setPointSize(14)

#         font.setBold(True)

#         self.label.setFont(font)

#         self.graphWidget = pg.PlotWidget()
#         self.setCentralWidget(self.graphWidget)

#         # Add Background colour to white
#         self.graphWidget.setBackground("w")
#         # Add Title
#         self.graphWidget.setTitle("Pond Population", color="b", size="12pt")
#         # Add Axis Labels
#         styles = {"color": "#f00", "font-size": "12px"}
#         self.graphWidget.setLabel("left", "Population", **styles)
#         self.graphWidget.setLabel("bottom", "Time", **styles)
#         # Add legend
#         self.graphWidget.addLegend()
#         # Add grid
#         self.graphWidget.showGrid(x=True, y=True)
#         # Set Range

#         self.h_layout1.addWidget(self.graphWidget)
#         self.h_layout1.addWidget(self.chart_view)

#         #Add components to QVBoxLayout
#         self.vbox.addWidget(self.label)
#         self.vbox.addLayout(self.h_layout1)
#         self.vbox.addLayout(self.grid)

#         self.widget.setLayout(self.vbox)

#         # Scroll Area Properties

#         self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)

#         self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

#         self.scroll.setWidgetResizable(True)

#         self.scroll.setWidget(self.widget)

#         # self.scroll.setWidget(self.graphWidget)

#         self.setCentralWidget(self.scroll)

#         self.setGeometry(0, 290, 600, 800)

#         self.setWindowTitle("Dashboard")

#         self.show()

#         return

#     def update(fishes):

#         pass