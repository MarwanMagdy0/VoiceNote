from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy, QTreeWidgetItem, QScrollBar
from PyQt5 import uic
from widgets import *
import sys
from utiles import *
main_directory = "test_folder"
initial_structure = {"0":{"group-name":"Title", "items":[]}}
if len(sys.argv)==2:
    main_directory = sys.argv[1]

if not os.path.isdir(main_directory):
    os.mkdir(main_directory)
    os.mkdir(main_directory + "//" + "0")

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.json_file = JsonIt(main_directory + ".vnote")
        self.file_structure = self.json_file.read_data()
        self.groups = {}
        if self.file_structure == {}:
            self.file_structure = initial_structure
            self.json_file.save_data(initial_structure)

        uic.loadUi("ui/load.ui",self)
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()
        self.add_new_group_button.clicked.connect(self.create_new_group)
        self.load_directory_to_ui()
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)


    def load_directory_to_ui(self):
        for group_fname in self.file_structure.keys():
            root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [self.file_structure[group_fname]["group-name"]])
            group = Group(self, main_directory, group_fname, self.file_structure[group_fname], root, self.treeWidget.topLevelItem(int(group_fname)))
            self.groups[group_fname] = group
            group.on_group_change.connect(self.update_group)
            self.layout.addWidget(group)
            group.load_data()
            self.scroll_area_bar.setMaximum(2147483647)
            self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())


    def update_group(self, group_fname, group_name, items, file_type):
        print("request update")
        self.activateWindow()
        if file_type == "name-changed":
            self.file_structure[group_fname]["group-name"] = group_name
        
        elif file_type == "text-added":
            self.file_structure[group_fname]["items"].append({"text":items, "font":group_name})
            print("file saved")
        elif file_type == ".wav" or file_type == ".png":
            self.file_structure[group_fname]["items"].append(items + file_type)
        
        self.json_file.save_data(self.file_structure)
    

    def create_new_group(self):
        group_fname = int([name for name in self.file_structure.keys()][-1]) + 1 # to get the added group name
        root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [f"Title_{group_fname}"])
        self.file_structure[str(group_fname)] = {"group-name":f"Title_{group_fname}", "items":[]}
        group = Group(self, main_directory, str(group_fname), self.file_structure[str(group_fname)], root, self.treeWidget.topLevelItem(int(group_fname)))
        group.on_group_change.connect(self.update_group)
        os.mkdir(main_directory + "//" + str(group_fname))
        self.layout.addWidget(group)
        self.groups[str(group_fname)] = group
        self.json_file.save_data(self.file_structure)
        self.scroll_area_bar.update()
        self.scroll_area_bar.setMaximum(self.scroll_area_bar.maximum()+200)
        self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
    

    def handle_item_clicked(self, item, column):
        find_widget = [None, item.text(column)]
        parent_text = item.text(column)
        if item.parent():
            parent_text = item.parent().text(0)
        for i in range(self.treeWidget.topLevelItemCount()):
            top_level_item = self.treeWidget.topLevelItem(i)
            if top_level_item.text(0) == parent_text:
                find_widget[0] = i
                break
        self.scroll_area_bar.setValue(self.groups[str(find_widget[0])].y())
        

app = QApplication([])
wind = UI()
wind.showMaximized()
app.exec_()
