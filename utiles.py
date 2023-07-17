from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QDialog, QApplication, QTreeWidgetItem, QFontDialog, QMessageBox, QFrame, QSizePolicy, QColorDialog
from PyQt5.QtGui import QPixmap, QImage, QIcon, QFont
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
import os
from PIL import Image
from PyQt5 import uic
import pyaudio
import wave
import json
import os, sys
import time
import random
import shutil
import cv2
import numpy as np
import gc
import threading
if len(sys.argv)==1:
    sys.argv.append("C:\\Users\\hp\\Documents\\My_Data\\Python Projects\\Qt\\VoiceNote\\test_folder.vnote")

SCRIPT_DIRECTORY    = os.path.dirname(os.path.realpath(__file__))
USER_FILE_DIRECTORY = sys.argv[1][:-6] # C:\Users\hp\Desktop\new

class HandleJsonFiles:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_directory = os.path.dirname(self.file_path) + "\\" + os.path.basename(self.file_path).split(".")[0]
        if not os.path.isfile(self.file_path):
            self.save_data({})
        with open(sys.argv[1], "r") as f:
            if f.read() == "":
                with open(self.file_path, 'w') as write_to_file:
                    write_to_file.write("{}")

    def save_data(self, data):
        with open(self.file_path, 'w') as f:
            json.dump(data, f)

    def read_data(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)
        
    def __getitem__(self, key):
        return self.read_data()[key]
    
    def __setitem__(self, key: str, value) -> None:
        data = self.read_data()
        data[key] = value
        self.save_data(data)
        
    def keys(self):
        data = self.read_data()
        return data.keys()


def get_time():
    return str(int(time.time() + 0.5 )) 

class GarbageCollector:
    def __init__(self):
        self.run = True
        self.time_interval = 5
        self.interrupt_event = threading.Event()
        self.thread = threading.Thread(target=self._collect)

    def start(self):
        self.thread.start()

    def _collect(self):
        while self.run:
            gc.collect()
            self.interrupt_event.wait(self.time_interval)
            self.interrupt_event.clear()

    def stop(self):
        self.run = False
        self.interrupt_event.set()
        self.thread.join()

collector = GarbageCollector()
collector.start()

init_group = {"group-title":"Title", "items":[], "refrences":{}}



def message_box() -> bool:
    msg_box = QMessageBox()
    msg_box.setIcon(QMessageBox.Question)
    msg_box.setText("Are you sure you want to delete?")
    msg_box.setWindowTitle("Confirmation")
    msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    result = msg_box.exec_()
    return result == QMessageBox.Yes


class QHSeparationLine(QFrame):
    def __init__(self, group_fname, separator_name):
        super().__init__()
        self.group_fname = group_fname
        self.separator_name = separator_name
        self.setFrameShape(QFrame.HLine)
        self.setFrameShadow(QFrame.Sunken)
        self.setStyleSheet("background-color: #1e1e1e;")
        self.setContentsMargins(0, 0, 0, 0)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            if message_box():
                self.deleteLater()
                data = self.workspace_file.read_data()
                data[self.group_fname]["items"].remove(self.separator_name)
                self.workspace_file.save_data(data)



if __name__ == "__main__":
    print(USER_FILE_DIRECTORY)