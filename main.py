from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy
from PyQt5 import uic
from widgets import *
import sys
from utiles import *
folder_name = "test_folder"
initial_structure = {"0":{"group-name":"Title", "items":[]}}
if len(sys.argv)==2:
    folder_name = sys.argv[1]

if not os.path.isdir(folder_name):
    os.mkdir(folder_name)
    os.mkdir(folder_name + "//" + "0")

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_file = JsonIt(folder_name + ".vnote")
        self.file_structure = self.json_file.read_data()
        if self.file_structure == {}:
            self.file_structure = initial_structure
            self.json_file.save_data(initial_structure)

        uic.loadUi("ui/load.ui",self)
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.add_new_group_button.clicked.connect(self.create_new_group)
        self.load_directory_to_ui()
    
    def load_directory_to_ui(self):
        for key in self.file_structure.keys():
            group = Group(self, folder_name, key, self.file_structure[key])
            group.on_group_change.connect(self.update_group)
            self.layout.addWidget(group)
            group.load_data()

    def update_group(self, group_fname, group_name, items, file_type):
        self.activateWindow()
        self.file_structure[group_fname]["group-name"] = group_name
        if file_type != "":
            self.file_structure[group_fname]["items"].append(items + file_type)
        
        self.json_file.save_data(self.file_structure)
    
    def create_new_group(self):
        group_name = int([name for name in self.file_structure.keys()][-1]) + 1 # to get the added group name
        self.file_structure[str(group_name)] = {"group-name":"Title", "items":[]}
        self.json_file.save_data(self.file_structure)
        group = Group(self, folder_name, str(group_name), self.file_structure[str(group_name)])
        group.on_group_change.connect(self.update_group)

        self.layout.addWidget(group)
        os.mkdir(folder_name + "//" + str(group_name))

    
app = QApplication([])
wind = UI()
wind.showMaximized()
app.exec_()
