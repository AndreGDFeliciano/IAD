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
                            QMessageBox,QVBoxLayout
import pyqtgraph as pg
from pyqtgraph import PlotWidget
import os
import serial
import numpy as np
import time
import sys

#arduino=serial.Serial(port='/dev/tty.usbmodem1101',baudrate=9600,timeout=.1)
arduino=serial.Serial(port='/dev/cu.usbmodem1101',baudrate=9600,timeout=.1)
#arduino = serial.Serial(port="/dev/ttyACM0", baudrate= 9600, timeout=.1)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()
        self.x = []
        self.y = []

    def initUI(self):
        self.setGeometry(300, 300, 500, 400) # (x, y, width, height)
        self.setWindowTitle('My PyQt5 App')

        self.button1 = QPushButton('test button', self)
        self.button1.setToolTip('This is a <b>QPushButton</b> widget')
        self.button1.clicked.connect(self.showMessageBox)
        #button1.clicked.connect(self.comando("3"))

        self.button2 = QPushButton('Enviar 1 comando', self)
        self.button2.setToolTip('Enviar comando para arduino')
        self.button2.clicked.connect(
            lambda:self.callFunctionWithArgument('Hello from PyQt!'))

        self.button3 = QPushButton('Enviar comandos periódicos', self)
        self.button3.setCheckable(True)
        self.button3.setChecked(False)
        self.button3.setToolTip(
                              'Envia comando periodicamente e atualiza gráfico')
        self.button3.toggled.connect(self.toggleGraphUpdate)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)

        # Create QtGraph plot
        self.plotWidget = PlotWidget()
        self.plotWidget.setLabel('left', 'Voltage', units='V')
        self.plotWidget.setLabel('bottom', 'Time', units='s')
        self.xlim = 10
        self.div  = self.xlim
        self.x = np.linspace(0, self.xlim, self.div)
        self.y = np.sin(self.x)
        self.xval = []
        self.t    = -1
        self.yval = []
        self.plotWidget.plot(self.xval, self.yval, pen='b')

        # Add plot to layout
        layout.addWidget(self.plotWidget)

        self.setLayout(layout)

        # Timer for periodic updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateGraph)
        #define what to do in the time "tick" == "timeout"



    def showMessageBox(self):
        QMessageBox.information(self, 'Message', 'You clicked the button!')

    def callFunctionWithArgument(self, argument):
        QMessageBox.information(self, 'Function Called',
                f'Function called with argument:{self.comando("1")}')

    def comando(self,argumento):
        """
        Sends comando to arduino
        Receives:
            argumento (float): value sent in
        Returns:
            float: measured value
        """
        if (isinstance(argumento, str) and argumento.isnumeric()) or\
            isinstance(argumento, int):
            int(argumento)
            arduino.write(bytes(argumento,"utf-8"))
            time.sleep(0.1)
            data = arduino.readline().decode("UTF-8")
            data = float(data)
            return data
        raise ValueError("comando: argumento inválido")

    def toggleGraphUpdate(self):
        if self.button3.isChecked():
            self.timer.start(1000)  # Update every 1 second
        else:
            self.timer.stop()  # Stop the timer

    def updateGraph(self):
        # Generate new data for the plot
        self.xlim += 1
        self.div = self.xlim
        self.x = np.linspace(0,self.xlim,self.div) ##self.comando("1")
        self.y = np.sin(self.x)
        self.t += 1
        self.xval.append(self.t)
        valor = self.comando("1")
        print(valor)
        self.yval.append(valor)
        self.plotWidget.plot(self.xval, self.yval, pen='b')



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