import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLabel, QGroupBox, QVBoxLayout


class DynamicGridLayoutApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Dynamic GridLayout Example')
        self.setGeometry(100, 100, 400, 300)

        # Create the main layout and its container
        self.main_layout = QGridLayout()
        self.setLayout(self.main_layout)

        # Create a list to store the dynamically added items
        self.items = []

        # Add some initial items to the layout
        self.add_item("Item 0", 0, 0)
        self.add_item("Item 1", 0, 1)
        self.add_item("Item 2", 1, 0)
        self.add_item("Item 3", 1, 1)
        self.add_item("Item 4", 2, 0)
        self.add_item("Item 5", 2, 1)
        self.add_item("Item 6", 3, 0)
        self.add_item("Item 7", 3, 1)

        self.remove_button = QPushButton("Remove Item", self)
        self.remove_button.clicked.connect(self.remove_item)

        self.main_layout.addWidget(self.remove_button, 4, 0, 1, 2)

        self.show()

    def add_item(self, text, row, col):
        item = QGroupBox()
        item_layout = QVBoxLayout()
        label = QLabel(text)
        item_layout.addWidget(label)
        item.setLayout(item_layout)
        self.items.append(item)
        self.main_layout.addWidget(item, row, col)

    def remove_item(self):
        print(len(self.items))
        self.main_layout.addWidget(QLabel("nn"), 40, 20)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DynamicGridLayoutApp()
    sys.exit(app.exec_())
