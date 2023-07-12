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
        # Timer to control seconds after creating new group
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(lambda: self.add_new_group_button.setEnabled(True))


    def load_directory_to_ui(self):
        for group_fname in json_file.keys():
            root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [json_file[group_fname]["group-title"]])
            group = Group(self, group_fname, root, self.treeWidget.topLevelItem(len(self.groups)))
            group.group_is_deleted.connect(self.delete_group)
            self.layout.addWidget(group)
            group.load_data()
            group.activate_mainwindow.connect(self.activateWindow)
            self.scroll_area_bar.setMaximum(2147483647)
            self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
            self.groups.append(group)
    

    def create_new_group(self):
        self.add_new_group_button.setEnabled(False)
        group_fname = get_time()
        group_directory = USER_FILE_DIRECTORY + "\\" + group_fname
        root = QTreeWidgetItem(self.treeWidget.invisibleRootItem(), [f"Title"])
        json_file[group_fname] = init_group
        os.mkdir(group_directory)
        group = Group(self, group_fname, root, self.treeWidget.topLevelItem(len(self.groups)))
        group.group_is_deleted.connect(self.delete_group)
        self.layout.addWidget(group)
        self.scroll_area_bar.setMaximum(self.scroll_area_bar.maximum()+200)
        self.scroll_area_bar.setValue(self.scroll_area_bar.maximum())
        self.groups.append(group)
        self.timer.start()
            

    def delete_group(self, group_fname):
        group_to_delete = None
        group_index = 0
        for i, group in enumerate(self.groups):
            if group.group_fname == group_fname:
                group_index = i
                break
        
        self.groups.pop(group_index)
        self.treeWidget.takeTopLevelItem(group_index) 


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
collector.stop()
