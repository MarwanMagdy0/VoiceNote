from PyQt5.QtWidgets import QMainWindow, QApplication ,QLabel ,QPushButton, QSizePolicy, QTreeWidgetItem
from PyQt5 import uic
from group import *


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\load.ui",self)
        self.setWindowIcon(QIcon(SCRIPT_DIRECTORY + "\\" + 'ui\\data\\icon.png'))
        self.setWindowTitle(os.path.basename(sys.argv[1]))
        self.layout = self.scrollArea.widget().layout()
        self.scrollArea.widget().setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.scroll_area_bar = self.scrollArea.verticalScrollBar()
        self.add_new_group_button.clicked.connect(self.create_new_group)
        self.groups = []
        self.load_directory_to_ui()
        self.treeWidget.itemClicked.connect(self.handle_item_clicked)


    def load_directory_to_ui(self):
        for group_fname in json_file.keys():
            root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [json_file[group_fname]["group-title"]])
            group = Group(self, group_fname, root, self.treeWidget.topLevelItem(len(self.groups)))
            self.layout.addWidget(group)
            group.load_data()
            group.activate_mainwindow.connect(self.activateWindow)
            self.scroll_area_bar.setMaximum(2147483647)
            self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
            self.groups.append(group)
    

    def create_new_group(self):
        group_fname = USER_FILE_DIRECTORY + "\\" + get_time()
        root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [f"Title"])
        json_file[group_fname] = {"group-title":f"Title", "items":[]}
        os.mkdir(group_fname)
        group = Group(self, group_fname, root, self.treeWidget.topLevelItem(len(self.groups)))
        self.layout.addWidget(group)
        self.scroll_area_bar.setMaximum(self.scroll_area_bar.maximum()+200)
        self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
        self.groups.append(group)
    

    def resizeEvent(self, event):
        # TODO try to resize images when ever this happens
        pass

    def handle_item_clicked(self, item, column):
        index = self.treeWidget.indexOfTopLevelItem(item)
        if index != -1:
            self.scroll_area_bar.setValue(self.groups[index].y())
        

app = QApplication([])
wind = UI()
wind.showMaximized()
app.exec_()
