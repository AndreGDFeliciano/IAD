"""
Project 1 - Instrumentação e Aquisição de Dados
Group 5
Project using arduino Uno and raspberry pi3
languages: C and python3

Sends command to arduino and reads AnalogIn
"""

__author__ = "ist1100286 André Feliciano & ist1103132 Rodrigo Casimiro"
__version__ = "42"


import PyQt5
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,\
                            QMessageBox,QVBoxLayout,QInputDialog
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import os
import serial
import numpy as np
import time
import sys

arduino=serial.Serial(port='/dev/tty.usbmodem1101',baudrate=9600,timeout=.1)
#arduino=serial.Serial(port='/dev/cu.usbmodem1101',baudrate=9600,timeout=.1)
#arduino = serial.Serial(port="/dev/ttyACM0", baudrate= 9600, timeout=.1)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.xval = []
        self.yval = []
        self.t    = 0
        self.command  = "1"
        self.time_int = 1000
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 500, 400) # (x, y, width, height)
        self.setWindowTitle('My PyQt5 App')

        self.buttonTest = QPushButton('Test button', self)
        self.buttonTest.setToolTip('This is a <b>QPushButton</b> widget')
        self.buttonTest.clicked.connect(self.showMessageBox)

        self.buttonCommand = QPushButton('Enviar 1 comando', self)
        self.buttonCommand.setToolTip(
                    'Enviar comando para arduino, devolve tensão(V)')
        self.buttonCommand.clicked.connect(
            lambda:self.callFunctionWithArgument('Hello from PyQt!'))

        self.buttonStart = QPushButton('Start/Stop comandos periódicos', self)
        self.buttonStart.setCheckable(True)
        self.buttonStart.setChecked(False)
        self.buttonStart.setToolTip(
                    'Envia comando periodicamente e atualiza gráfico')
        self.buttonStart.toggled.connect(self.toggleGraphUpdate)

        self.buttonChangeC = QPushButton('Change Command', self)
        self.buttonChangeC.setToolTip('Click to change command')
        self.buttonChangeC.clicked.connect(self.inputCommand)

        self.buttonChangeT = QPushButton('Change time interval', self)
        self.buttonChangeT.setToolTip('Click to change time interval')
        self.buttonChangeT.clicked.connect(self.inputTime)

        self.buttonCleanGraph = QPushButton('Clean Graph', self)
        self.buttonCleanGraph.setToolTip('Click to clean the graph below')
        self.buttonCleanGraph.clicked.connect(self.cleanGraph)


        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.buttonTest)
        layout.addWidget(self.buttonCommand)
        layout.addWidget(self.buttonStart)
        layout.addWidget(self.buttonChangeC)
        layout.addWidget(self.buttonChangeT)
        layout.addWidget(self.buttonCleanGraph)


        # Create QtGraph plot
        self.plotWidget = PlotWidget()
        self.plotWidget.setLabel('left', 'Voltage', units='V')
        self.plotWidget.setLabel('bottom', 'Time', units='s')
        self.plotWidget.setYRange(0, 5)

        self.plotWidget.plot(self.xval, self.yval, pen='b')

        # Add plot to layout
        layout.addWidget(self.plotWidget)

        self.setLayout(layout)

        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGraph)
        #define what to do in the time "ticks" == "timeout"

    def showMessageBox(self):
        QMessageBox.information(self, 'Message', 'You clicked the button!')

    def callFunctionWithArgument(self, argument):
        QMessageBox.information(self, 'Function Called',
                f'Function called with argument:{self.comando(self.command)}')

    def comando(self,argumento):
        """
        Sends comando to arduino
        Receives:
            argumento (float): value sent in
        Returns:
            float: measured value
        """
        arduino.write(bytes(argumento,"utf-8"))
        time.sleep(0.001) # wait for the arduino to write to the Serial
        data = arduino.readline().decode("UTF-8")
        if data == "Erro: comando inválido!":
            raise ValueError(data)
        else:
            data = float(data)
            return data


    def toggleGraphUpdate(self):
        """
        Sets the timer for updating graph at a set interval
        Receives:
            time = 1000 (int, optional): time interval
        """

        if self.buttonStart.isChecked():
            self.new = True
            self.timer.start(self.time_int)  # Update every 1 second
        else:
            self.new = False
            self.timer.stop() #stops the timer
        return None

    def updateGraph(self):
        """
        Define the action to take at timeout update graph
        Receives:
            time = 1000 (int, optional): time interval
        """
        # Generate new data for the plot
        valor = self.comando(self.command)
        print(valor)
        self.yval.append(valor)
        self.xval.append(self.t)
        self.t += self.time_int / 1000
        self.plotWidget.plot(self.xval, self.yval, pen='b')

    def inputCommand(self):
        comm, ok = QInputDialog.getText(self, 'Input command',
                                    'Enter new command \nCorrect command: 1')
        if ok:
            QMessageBox.information(self, 'New Command',
                                    f'You entered: {comm}')
            self.command = comm

    def inputTime(self):
        time, ok = QInputDialog.getInt(self, 'Input time interval',
                                        'Enter new time interval (ms):',
                                        min = 10)
        if ok:
            QMessageBox.information(self, 'Input Values',
                                    f'You entered: {time}')
            self.time_int = time

    def cleanGraph(self):
        self.plotWidget.clear()
        self.xval = []
        self.yval = []
        self.t    = 0




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())


# Janela Utilizador introduzir comando
# Start/Stop
# comando

""" test with integers
###
while True: #cycle to test if we can talk to the arduino
    num = input("Enter a number: ")
    value = comando(num)
    print((value))
"""