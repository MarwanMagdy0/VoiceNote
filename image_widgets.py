from utiles import *

class ImageWidget(QWidget):
    def __init__(self, parent_group):
        super().__init__(parent_group)
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\image.ui",self)
    
    def set_img(self, image_from_object):
        pixmap = QPixmap.fromImage(image_from_object)
        self.image.setPixmap(pixmap)
    
    def load_img(self, path):
        pixmap = QPixmap(path)
        self.image.setPixmap(pixmap)