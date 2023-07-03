from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy, QTreeWidgetItem, QScrollBar
from PyQt5 import uic
from widgets import *

class UI(QMainWindow):
    u = pyqtSignal(dict)
    def __init__(self):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "//" + "ui/load.ui",self)
        self.add_new_group_button.clicked.connect(self.create_new_group)
        self.u.connect(self.signal)
    
    def create_new_group(self):
        self.u.emit({"haha": 17})
    
    def signal(self, dictionary):
        print(dictionary, type(dictionary), dictionary["haha"])


app = QApplication([])
wind = UI()
wind.showMaximized()
app.exec_()
