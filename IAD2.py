"""
Project 2 - Instrumentação e Aquisição de Dados
Group 5
Project using arduino Uno and raspberry pi3
languages: C and python3

Sends command to arduino and reads AnalogIn
"""

__author__ = "ist1100286 André Feliciano & ist1103132 Rodrigo Casimiro"
__version__ = "42"



from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,\
                            QMessageBox,QVBoxLayout,QInputDialog
from pyqtgraph import PlotWidget
import os
import serial
import numpy as np
import time
import sys

#arduino=serial.Serial(port='/dev/tty.usbmodem1101',baudrate=9600,timeout=.1)
#arduino=serial.Serial(port='/dev/cu.usbmodem1101',baudrate=9600,timeout=.1)
arduino = serial.Serial(port="/dev/ttyACM0", baudrate= 9600, timeout=.1)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        # Create lists to store values to graph
        self.xval = []
        self.yval = []
        # Create time count
        self.t    = 0
        #Create a place to store command and time interval, set the default
        self.command  = "1"
        self.time_int = 1000
        self.initUI()

    def initUI(self):
        """
        Starts the UI for the windows program
        2 buttons:
            Send 1 Command
            Start/Stop periodic command
        1 Graph:
            yaxis: Voltage read in arduino
            xaxis: time
        3 buttons
            Change comand
            Change time interval
            Clear graph
        """
        self.showMaximized() #maximise window at start
        self.setWindowTitle('First IAD Project')

        # Creating Buttons with tooltips
        self.buttonCommand = QPushButton('Send 1 command', self)
        self.buttonCommand.setToolTip(
                    'Send command for arduino to read voltage(V)')
        self.buttonCommand.clicked.connect(self.sendCommand)

        self.buttonStart = QPushButton('Start/Stop periodic command', self)
        self.buttonStart.setToolTip(
            'Sends commands periodically and updates graph while toggled')
        self.buttonStart.setCheckable(True) # make it a toggle button
        self.buttonStart.setChecked(False)  # Guarantee it starts turned off
        self.buttonStart.toggled.connect(self.toggleGraphUpdate)

        self.buttonChangeC = QPushButton('Change command', self)
        self.buttonChangeC.setToolTip('Click to change command')
        self.buttonChangeC.clicked.connect(self.inputCommand)

        self.buttonChangeT = QPushButton('Change time interval', self)
        self.buttonChangeT.setToolTip('Click to change time interval')
        self.buttonChangeT.clicked.connect(self.inputTime)

        self.buttonClearGraph = QPushButton('Clear graph', self)
        self.buttonClearGraph.setToolTip('Click to clear the graph below')
        self.buttonClearGraph.clicked.connect(self.clearGraph)


        # Create layout
        layout = QVBoxLayout()

        #Add buttons on top of the graphic
        layout.addWidget(self.buttonCommand)
        layout.addWidget(self.buttonStart)


        # Create QtGraph plot
        self.plotWidget = PlotWidget()
        self.plotWidget.setLabel('left', 'Voltage', units='V')
        self.plotWidget.setLabel('bottom', 'Time', units='s')
        self.plotWidget.setYRange(0, 5)

        self.plotWidget.plot(self.xval, self.yval, pen='b')

        # Add plot to layout
        layout.addWidget(self.plotWidget)
        # Add the buttons below the graph
        layout.addWidget(self.buttonChangeC)
        layout.addWidget(self.buttonChangeT)
        layout.addWidget(self.buttonClearGraph)

        self.setLayout(layout)

        # Timer for periodic updates
        self.timer = QTimer(self)
        # define what to do in the time "ticks" == "timeout"
        self.timer.timeout.connect(self.updateGraph)

    def sendCommand(self):
        """
        Creates a QMessageBox and sends a command to the arduino.
        Reads the voltage in the arduino
        """
        QMessageBox.information(self, 'Command sent',
                f'Voltage measured:{self.comando()}')

    def comando(self):
        """
        Sends command to arduino..
        Returns:
            float: measured value
        Error in case there is a wrong command or empty string
        """
        arduino.write(bytes(self.command,"utf-8"))
        time.sleep(0.001) # wait for the arduino to write to the Serial in s
        read = arduino.readline().decode("UTF-8").rstrip()
        # rstring takes out the \n and \r at the end of the line
        if read == "Error: Invalid command":
            QMessageBox.information(self, 'Invalid Command',
            f'Function called with command: {self.command} \n \
Correct command ("1") was reset')
            self.command = "1"
            raise ValueError("Error: Invalid Command")
        elif read == "": # in order to avoid the unknown error of empty string
            raise ValueError("Empty string")
        else:
            read = float(read)
            return read


    def toggleGraphUpdate(self):
        """
        Sets the timer for updating graph at the set interval.
        """
        if self.buttonStart.isChecked():
            self.new = True
            self.timer.start(self.time_int)  # timeout every 1 second
        else:
            self.new = False
            self.timer.stop() #stops the timer
        return None

    def updateGraph(self):
        """
        Generate new data
        Print value to terminal
        Update graph
        """
        # Generate new data for the plot
        value = self.comando()
        print(value)
        # Add time and value to lists to graph
        self.yval.append(value)
        self.xval.append(self.t)
        self.t += self.time_int / 1000 # transform ms to s
        self.plotWidget.plot(self.xval, self.yval, pen='b')

    def inputCommand(self):
        """
        Opens a window and asks for the user to choose the new command
        Tests if it is the right command
        """
        comm, ok = QInputDialog.getInt(self, 'Input command',
                                    'Enter new command \nCorrect command: 1')
        if ok:
            QMessageBox.information(self, 'New Command',
                                    f'You entered: {comm}')
            # comm is an int and bytes function receives a string
            self.command = str(comm)
            self.comando()


    def inputTime(self):
        """
        Opens a window and asks for the user to choose the new time interval.
        In case the toggle is checked: clears the graph and keeps adding values
        """
        time, ok = QInputDialog.getInt(self, 'Input time interval',
                                        'Enter new time interval (ms):',
                                        min = 10)
        if ok:
            QMessageBox.information(self, 'Input Values',
                                    f'You entered: {time}')
            self.time_int = time
        if self.buttonStart.isChecked():
            self.clearGraph()
            self.toggleGraphUpdate()

    def clearGraph(self):
        """
        Clears the graph
        """
        self.plotWidget.clear()
        self.xval = []
        self.yval = []
        self.t    = 0

# Starts the new window
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())