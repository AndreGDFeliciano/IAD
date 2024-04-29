from PyQt5 import QtWidgets
import sys

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    widget.resize(250, 150)
    widget.setWindowTitle('Simple')
    widget.show()
    sys.exit(app.exec_())