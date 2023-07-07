from PyQt5.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QTreeWidget

class MyWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.treeWidget = QTreeWidget(self)

        # Add invisible items to the treeWidget
        item1 = self.treeWidget.invisibleRootItem().child(0)
        item2 = self.treeWidget.invisibleRootItem().child(1)
        item3 = self.treeWidget.invisibleRootItem().child(2)

        layout = QVBoxLayout()
        layout.addWidget(self.treeWidget)

        removeButton = QPushButton("Remove Invisible Items", self)
        removeButton.clicked.connect(self.removeInvisibleItems)
        layout.addWidget(removeButton)

        self.setLayout(layout)

    def removeInvisibleItems(self):
        invisibleRootItem = self.treeWidget.invisibleRootItem()
        invisibleIndex2 = self.treeWidget.indexOfTopLevelItem(invisibleRootItem.child(2))
        invisibleIndex1 = self.treeWidget.indexOfTopLevelItem(invisibleRootItem.child(1))

        self.treeWidget.takeTopLevelItem(invisibleIndex2)  # Remove the third invisible item
        self.treeWidget.takeTopLevelItem(invisibleIndex1)  # Remove the second invisible item

if __name__ == '__main__':
    app = QApplication([])
    window = MyWidget()
    window.show()
    app.exec()
