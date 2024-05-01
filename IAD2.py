"""
Muon Telescope
Project 2 - Instrumentação e Aquisição de Dados
Group 5
Languages: C and python3

This script communicates with an Arduino to read AnalogIn data, and uses PyQt5 to display
histograms of the data, as well as offering the functionality to save the plotted data.
"""


__author__ = "ist1100286 André Feliciano & ist1103132 Rodrigo Casimiro"
__version__ = "42"

"""Necessary libraries"""
import sys
import serial
import signal
import time
import os
import numpy as np
import pyqtgraph as pg
from pyqtgraph.exporters import ImageExporter
from PyQt5 import QtWidgets, QtGui, QtCore
from collections import deque
from datetime import datetime as date
from PyQt5.QtWidgets import QMessageBox

arduinoPort = "/dev/cu.usbmodemF412FA75E7882"

class SerialHistogram(QtWidgets.QWidget):
    """A widget for displaying histograms of time differences
    and count frequencies from Arduino data."""
    def __init__(self, port, baudrate=9600, parent=None):
        """Initialize the serial port and set up the UI"""
        super(SerialHistogram, self).__init__(parent)
        self.serial_port = serial.Serial(port, baudrate, timeout=1) # Serial
        self.time_differences = deque(maxlen=100000)
        self.timeStamps = deque(maxlen=100000)

        self.maxXRangeExp = 15000  # Default X-axis max Exponential (ms)
        self.maxXRangePoisson = 24 # Default X-axis max Histogram (hours)
        self.numBinsExp = 30       # Default number of bins for Exp
        self.numBinsPoisson = 48   # Default number of bins for Histogram

        self.setupUi()
        self.setupSerial()

        folder_path = "/Users/rodrigocasimiro/Desktop/Data"

        if not os.path.exists(folder_path):
            print("ERROR: Data folder does not exist.")

        # Create the file within the specified folder
        file_path = os.path.join(folder_path, "dataset_" + str(date.today()) + ".txt")
        self.file = open(file_path, "w")


    def setupUi(self):
        """
        Sets up the User Interface for the Muon Telescope application.
        The UI includes:
        - Histogram controls for both exponential and Poisson data:
          * Two plot widgets for displaying histograms.
          * Four buttons for each histogram:
            1. Change X-axis Range
            2. Change Number of Bins
            3. Clear Plot
            4. Save Plot
        - Layouts:
          * Exponential Layout: Controls and plot for the time between detections.
          * Poisson Layout: Controls and plot for the count of detections per hour.
        - Styling:
          * Sets button styles and adds widgets to layouts.
        """
        
        self.setWindowTitle('Muon Telescope')
        self.mainLayout = QtWidgets.QHBoxLayout()
        self.setLayout(self.mainLayout)

        button_style = ("QPushButton {"
                        "background-color: #FFFFFF;"
                        "color: #374c80;"
                        "border-radius: 5px;"
                        "padding: 6px;"
                        "}")

        """Exponential Histogram Controls"""
        # Layout for histogram
        self.exponentialLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.exponentialLayout)

        # Plot for histogram
        self.exponentialPlotWidget = pg.PlotWidget()
        self.exponentialLayout.addWidget(self.exponentialPlotWidget)
        self.exponentialPlotWidget.setTitle("Histogram of Time Between Detections")
        self.exponentialPlotWidget.setLabel('left', 'Absolute frequency')
        self.exponentialPlotWidget.setLabel('bottom', 'Time between counts (ms)')
        self.exponentialPlotWidget.showGrid(x=True, y=True)
        self.exponentialPlotWidget.setBackground('#FFFFFF')

        # Button X-axis range
        self.changeXAxisButtonExp = QtWidgets.QPushButton("Change X-axis Range")
        self.exponentialLayout.addWidget(self.changeXAxisButtonExp)
        self.changeXAxisButtonExp.setStyleSheet(button_style)
        self.changeXAxisButtonExp.clicked.connect(self.changeXAxisRangeExp)

        # Button number of bins
        self.changeBinsButtonExp = QtWidgets.QPushButton("Change Number of Bins")
        self.exponentialLayout.addWidget(self.changeBinsButtonExp)
        self.changeBinsButtonExp.setStyleSheet(button_style)
        self.changeBinsButtonExp.clicked.connect(self.changeNumberOfBinsExp)

        # Button to clear the plot
        self.clearPlotButtonExp = QtWidgets.QPushButton("Clear Plot")
        self.exponentialLayout.addWidget(self.clearPlotButtonExp)
        self.clearPlotButtonExp.setStyleSheet(button_style)
        self.clearPlotButtonExp.clicked.connect(self.clearPlotExp)

        # Button to save the plot
        self.savePlotButtonExp = QtWidgets.QPushButton("Save Plot")
        self.exponentialLayout.addWidget(self.savePlotButtonExp)
        self.savePlotButtonExp.setStyleSheet(button_style)
        self.savePlotButtonExp.clicked.connect(self.savePlotExp)

        """Poisson Histogram Controls"""
        # Layout for the new counts plot
        self.poissonLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.addLayout(self.poissonLayout)

        # Plot for the new counts
        self.poissonPlotWidget = pg.PlotWidget()
        self.poissonLayout.addWidget(self.poissonPlotWidget)
        self.poissonPlotWidget.setTitle("Histogram of number of counts per hour")
        self.poissonPlotWidget.setLabel('left', 'Absolute frequency')
        self.poissonPlotWidget.setLabel('bottom', 'Time', units='h')
        self.poissonPlotWidget.showGrid(x=True, y=True)
        self.poissonPlotWidget.setBackground('#FFFFFF')

        # Button X-axis range
        self.changeXAxisButtonPoisson = QtWidgets.QPushButton("Change X-axis Range")
        self.poissonLayout.addWidget(self.changeXAxisButtonPoisson)
        self.changeXAxisButtonPoisson.setStyleSheet(button_style)
        self.changeXAxisButtonPoisson.clicked.connect(self.changeXAxisRangePoisson)

        # Button number of bins
        self.changeBinsButtonPoisson = QtWidgets.QPushButton("Change Number of Bins")
        self.poissonLayout.addWidget(self.changeBinsButtonPoisson)
        self.changeBinsButtonPoisson.setStyleSheet(button_style)
        self.changeBinsButtonPoisson.clicked.connect(self.changeNumberOfBinsPoisson)

        # Button to clear the plot
        self.clearPlotButtonPoisson = QtWidgets.QPushButton("Clear Plot")
        self.poissonLayout.addWidget(self.clearPlotButtonPoisson)
        self.clearPlotButtonPoisson.setStyleSheet(button_style)
        self.clearPlotButtonPoisson.clicked.connect(self.clearPlotPoisson)

        # Button to save the plot
        self.savePlotButtonPoisson = QtWidgets.QPushButton("Save Plot")
        self.poissonLayout.addWidget(self.savePlotButtonPoisson)
        self.savePlotButtonPoisson.setStyleSheet(button_style)
        self.savePlotButtonPoisson.clicked.connect(self.savePlotPoisson)

    def setupSerial(self):
        """Set up a timer to update the histogram plots periodically."""
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.updateExponential)
        self.timer.timeout.connect(self.updatePoisson)
        self.timer.start(1000)  # Update interval in milliseconds

    def getData(self):
        """Read data from the serial port and process it."""
        try:
            while self.serial_port.inWaiting() > 0:
                line = self.serial_port.readline().decode("utf-8").rstrip()
                if line:
                    peak1, peak2, time_stamp, time_since_last_pulse = map(int, line.split())

                    self.time_differences.append(time_since_last_pulse//1000) # Convert to milliseconds
                    self.timeStamps.append(time_stamp/1000000/3600) # Convert to hours

                    # Write data to file
                    self.writeDataToFile(peak1, peak2, time_stamp, time_since_last_pulse)

        except Exception as e:
            print(f"Error in getData: {e}")

    def writeDataToFile(self, peak1, peak2, time_stamp, time_since_last_pulse):
        """Write acquired data to file."""

        # Unix timestamp in seconds and microseconds
        current_time = time.time()
        unix_time_seconds = int(current_time)

        # Format: count; unix_time_seconds (s); peak1 (mV); peak2(mV); time_stamp(μs); time_since_last_pulse (μs)
        line = f"{len(self.time_differences)} {unix_time_seconds} {peak1} {peak2} {time_stamp} {time_since_last_pulse}\n"
        self.file.write(line)
        self.file.flush() # Ensure data is written to disk

    def closeEvent(self, event):
        """Ensure the file and serial port are closed properly
        when the application is closed."""
        self.file.close()
        self.file.close()
        self.serial_port.close()
        super(SerialHistogram, self).closeEvent(event)

    """Exponential funtions"""
    def updateExponential(self):
        """Updates the exponential plot based on the collected time differences."""
        self.getData()
        if len(self.time_differences) > 0:
            y, x = np.histogram(list(self.time_differences), bins=self.numBinsExp, range=(34, self.maxXRangeExp))
            self.exponentialPlotWidget.clear()
            self.exponentialPlotWidget.plot(x, y, stepMode=True, fillLevel=0, brush=pg.mkBrush('#374c80'))

    def changeXAxisRangeExp(self):
        """Allow the user to change the maximum range of
        the X-axis for the exponential histogram."""
        maxXRange, ok = QtWidgets.QInputDialog.getInt(self, "Change X-axis Range", "Enter new max X-axis value (ms):", value=self.maxXRangeExp, min=100)
        if ok:
            self.maxXRangeExp = maxXRange
            self.updateExponential()  # Update histogram to reflect new X-axis range immediately

    def changeNumberOfBinsExp(self):
        """Allow the user to change the number of bins
        for the exponential histogram."""
        numBins, ok = QtWidgets.QInputDialog.getInt(self, "Change Number of Bins", "Enter new number of bins:", value=self.numBinsExp, min=1)
        if ok:
            self.numBinsExp = numBins
            self.updateExponential()  # Update histogram to reflect new number of bins immediately

    def clearPlotExp(self):
        """Clear the exponential histogram plot and the underlying data."""
        self.exponentialPlotWidget.clear()  # This clears the visual plot
        self.time_differences.clear()


    """Histogram funtions"""
    def updatePoisson(self):
        """Update the histogram plot with new data."""
        self.getData()
        if len(self.timeStamps) > 0:
            y, x = np.histogram(list(self.timeStamps), bins=self.numBinsPoisson, range=(0, self.maxXRangePoisson))
            self.poissonPlotWidget.clear()
            self.poissonPlotWidget.plot(x, y, stepMode=True, fillLevel=0, brush=pg.mkBrush('#374c80'))

    def changeXAxisRangePoisson(self):
        """Allow the user to change the maximum range of the X-axis for the histogram."""
        maxXRange, ok = QtWidgets.QInputDialog.getInt(self, "Change X-axis Range",
                                                     "Enter new max X-axis value (hours):",
                                                     value=self.maxXRangePoisson, min=1)
        if ok:
            self.maxXRangePoisson = maxXRange
            self.updatePoisson()  # Update histogram to reflect new X-axis range immediately

    def changeNumberOfBinsPoisson(self):
        """Allow the user to change the number of bins for the histogram."""
        numBins, ok = QtWidgets.QInputDialog.getInt(self, "Change Number of Bins", "Enter new number of bins:", value=self.numBinsPoisson, min=1)
        if ok:
            self.numBinsPoisson = numBins
            self.updatePoisson()  # Update histogram to reflect new number of bins immediately

    def clearPlotPoisson(self):
        """Clear the plot and the underlying data."""
        self.poissonPlotWidget.clear()  # This clears the visual plot
        self.timeStamps.clear()

    def savePlot(self, plotWidget, defaultName="plot"):
        """Save the current plot to a file."""
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, "Select Folder")
        if not folder_path:
            return

        today_date = date.today().strftime("%Y-%m-%d")
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Save Plot", os.path.join(folder_path, f"{defaultName}_{today_date}.png"),
            "PNG Image (*.png);;All Files (*)"
        )

        if fileName:
            if not fileName.endswith('.png'):
                fileName += '.png'
            try:
                exporter = pg.exporters.ImageExporter(plotWidget.plotItem)
                exporter.export(fileName)
                QMessageBox.information(self, "Success", "Plot saved successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save the file: {str(e)}")
                print(f"Error saving the plot: {e}")
        else:
            QMessageBox.warning(self, "Cancelled", "Save operation cancelled.")

    def savePlotExp(self):
        """Save the current exponential plot to a file."""
        self.savePlot(self.exponentialPlotWidget, "exponential_histogram")

    def savePlotPoisson(self):
        """Save the current Histogram plot to a file."""
        self.savePlot(self.poissonPlotWidget, "poisson_histogram")


if __name__ == '__main__':
    signal.signal(signal.SIGINT, signal.SIG_DFL) # ^C works this way

    app = QtWidgets.QApplication(sys.argv)
    window = SerialHistogram(arduinoPort)
    window.resize(1000, 600)
    window.show()
    sys.exit(app.exec_())
