from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy, QTreeWidgetItem
from PyQt5 import uic
from file_view import *


# Checking if the .vnote file is not empty and if it was , dump the initial directory data to it
with open(sys.argv[1], "r") as f:
    if f.read() == "":
        group_fname = get_time()
        if not os.path.isdir(USER_FILE_DIRECTORY):
            os.mkdir(USER_FILE_DIRECTORY)

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\main_window.ui",self)
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "\\" + 'ui\\data\\icon.png'))
        self.setWindowTitle(os.path.basename(sys.argv[1]))
        space = FileView(sys.argv[1])
        self.stackedWidget.addWidget(space)
        self.stackedWidget.setCurrentWidget(space)


app = QApplication([])
wind = UI()
wind.showMaximized()
app.exec_()
collector.stop()
