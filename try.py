from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication, QWidget, QHBoxLayout, QPushButton, QListWidget, QGridLayout
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, uic
from utiles import *


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\main_window.ui",self)
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "\\" + 'ui\\data\\icon.png'))
        self.setWindowTitle(os.path.basename(sys.argv[1]))
    
    def closeEvent(self, event):
        print("ex")
        event.accept()
        self.close()


app = QApplication([])
myWindow = UI()
myWindow.show()
sys.exit(app.exec_())
