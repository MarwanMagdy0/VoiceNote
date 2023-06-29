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
        self.groups = []
        if self.file_structure == {}:
            self.file_structure = initial_structure
            self.json_file.save_data(initial_structure)

        uic.loadUi("ui/load.ui",self)
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.load_directory_to_ui()
    
    def load_directory_to_ui(self):
        for key in self.file_structure.keys():
            group = Group(self, folder_name, key, self.file_structure[key])
            self.groups.append(group)
            self.layout.addWidget(group)
            group.load_data()
            group.on_group_change.connect(self.update_group)

    def update_group(self, group_object_and_file_type):
        group_object, file_type = group_object_and_file_type
        self.file_structure[group_object.group_fname]["group-name"] = group_object.group_name
        if file_type != "":
            self.file_structure[group_object.group_fname]["items"].append(str(group_object.items-1) + file_type)
        
        self.json_file.save_data(self.file_structure)

    def group_name_changed_method(self, old_name, new_name):
        for key, value in self.file_structure.items():
            if value["group-name"] == old_name:
                self.file_structure[key]["group-name"] = new_name
                
        for group in self.groups:
            if group.group_name == old_name:
                group.group_name = new_name
                break

        self.json_file.save_data(self.file_structure)
    
    def adding_new_widget_to_structure(self, group_name, fname):
        for key, value in self.file_structure.items():
            if value["group-name"] == group_name:
                self.file_structure[key][fname] = fname + ".wav"
                self.json_file.save_data(self.file_structure) 
   
app = QApplication([])
wind = UI()
wind.show()
app.exec_()
