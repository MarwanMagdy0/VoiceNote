from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeWidget, QTreeWidgetItem
import sys

class TreeWidgetExample(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the QTreeWidget
        self.tree_widget = QTreeWidget(self)
        self.setCentralWidget(self.tree_widget)

        # Add columns to the QTreeWidget
        self.tree_widget.setColumnCount(2)
        self.tree_widget.setHeaderLabels(['Column 1', 'Column 2'])

        # Add items to the QTreeWidget
        root_item = QTreeWidgetItem(self.tree_widget, ['Root Item', 'Data 1'])
        child_item = QTreeWidgetItem(root_item, ['Child Item', 'Data 2'])

        # Connect the itemClicked signal to a custom slot
        self.tree_widget.itemClicked.connect(self.handle_item_clicked)

    def handle_item_clicked(self, item, column):
        top_index = self.tree_widget.indexOfTopLevelItem(item)
        child_index = item.parent().indexOfChild(item)

        print(f"Top-Level Index: {top_index}")
        print(f"Child Index: {child_index}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TreeWidgetExample()
    window.show()
    sys.exit(app.exec_())
