from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QWidget
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtCore import Qt

class BarChart(QMainWindow):
    def __init__(self):
        super().__init__()

        self.chart = QWidget()

        # Create a pie series and add slices
        series = QPieSeries()
        series.append("Doo Pond", 20)
        series.append("Khor Pond", 30)
        series.append("Matrix Pond", 10)

        # Create a chart and set the series
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Pond")

        # Create a chart view and set the chart
        chart_view = QChartView(chart)

        # Set the central widget of the main window to the chart view
        self.setCentralWidget(chart_view)


if __name__ == "__main__":
    app = QApplication([])
    window = BarChart()
    app.exec_()
