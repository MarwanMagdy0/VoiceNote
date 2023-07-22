from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy, QTreeWidgetItem
from PyQt5 import QtGui, uic
from file_view import *
from workspace import *


class MainWindow(QMainWindow):
    stackedWidget: QStackedWidget
    def __init__(self):
        super().__init__()
        self.init_ui()
        if len(sys.argv) > 1:
            self.check_if_vnote_is_empty()

    def init_ui(self):
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\main_window.ui",self)
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "\\" + 'ui\\data\\icon.png'))
        self.setWindowTitle(os.path.basename(sys.argv[1]))
    
    
    def check_if_vnote_is_empty(self):
        with open(sys.argv[1], "r") as f:
            if f.read() == "":
                starting_screen = StartingScreen()
                starting_screen.file_type_choosed.connect(self.created_first_form)
                starting_screen.show()
            else: # if there is a current vnote form
                self.load_from_vnote(sys.argv[1])


    def created_first_form(self, file_type):
        file_json = HandleJsonFiles(sys.argv[1])
        if file_type == "workspace":
            file_json.save_data({"type":"workspace", "cards":[], "card-title":"Title", "back":None})
        else:
            file_json.save_data({"type":"file-view"})
        if not os.path.isdir(sys.argv[1][:-6]):
            os.mkdir(sys.argv[1][:-6])
        
        self.load_from_vnote(sys.argv[1])


    def load_from_vnote(self, path):
        self.workspace_json_file = HandleJsonFiles(path)
        if self.workspace_json_file["type"] == "workspace":
            w = WorkSpace(path)
            w.card_selected.connect(self.card_selected)
            w.go_back_from_workspace.connect(self.card_selected)
            self.update_stacked(w)
        else:
            file_view = FileView(path)
            file_view.go_back.connect(self.card_selected)
            self.update_stacked(file_view)
        self.showMaximized()


    def card_selected(self, card_data: dict):
        if card_data["type"] == "workspace":
            w = WorkSpace(card_data["directory"])
            w.card_selected.connect(self.card_selected)
            w.go_back_from_workspace.connect(self.card_selected)
            self.update_stacked(w)
        else:
            file_view = FileView(card_data["directory"])
            file_view.go_back.connect(self.card_selected)
            self.update_stacked(file_view)

    def update_stacked(self, widget):
        self.stackedWidget.addWidget(widget)
        self.stackedWidget.setCurrentWidget(widget)


app = QApplication([])
collector = GarbageCollector()
collector.start()
wind = MainWindow()
app.exec_()

collector.stop()

