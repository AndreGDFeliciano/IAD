"""
Project 1 - Instrumentação e Aquisição de Dados
Group 5
Project using arduino Uno and raspberry pi3
languages: C and python3

Sends command to arduino and reads AnalogIn
"""

__author__ = "ist1100286 André Feliciano & ist110???? Rodrigo Casimiro"
__version__ = "42"


import PyQt5
from PyQt5.QtWidgets import QApplication,QWidget,QPushButton,QMessageBox
import pyqtgraph
import os
import serial
import numpy
import time
import sys

#arduino = serial.Serial(port = '/dev/tty.usbmodem1101',
#                        baudrate= 9600, timeout=.1)
arduino = serial.Serial(port = "/dev/ttyACM0",
                        baudrate= 9600, timeout=.1)


class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 200) # (x, y, width, height)
        self.setWindowTitle('My PyQt5 App')

        button1 = QPushButton('Enviar comando', self)
        button1.setToolTip('This is a <b>QPushButton</b> widget')
        button1.clicked.connect(self.showMessageBox)
        #button1.clicked.connect(self.comando("3"))
        button1.move(100, 50)

        button2 = QPushButton('Function with Argument', self)
        button2.setToolTip('This button calls a function with an argument')
        button2.clicked.connect(
            lambda:self.callFunctionWithArgument('Hello from PyQt!'))
        button2.move(100, 100)

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
            return data
        raise ValueError("comando: argumento inválido")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    ex.show()
    sys.exit(app.exec_())


""" test with integers
###
while True: #cycle to test if we can talk to the arduino
    num = input("Enter a number: ")
    value = comando(num)
    print((value))
"""