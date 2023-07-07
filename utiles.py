from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel, QDialog, QApplication, QTreeWidgetItem, QFontDialog, QMessageBox
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
if len(sys.argv)==1:
    sys.argv.append("C:\\Users\\hp\\Documents\\My_Data\\Python Projects\\Qt\\VoiceNote\\test_folder.vnote")

SCRIPT_DIRECTORY    = os.path.dirname(os.path.realpath(__file__))
USER_FILE_DIRECTORY = sys.argv[1][:-6] # C:\Users\hp\Desktop\new

class JsonIt:
    def __init__(self,file_directory):
        self.file_directory = file_directory
        try:
            f=open(f'{self.file_directory}','r')
            data=json.load(f)
            f.close()
        except:
            data = {}
            dump =json.dumps(data)
            file = open(f'{file_directory}','w')
            file.write(dump)
            file.close()

    def save_data(self,Data):
        with open(f'{self.file_directory}','w') as f:
            dic=json.dumps(Data)
            f.write(dic)

    def read_data(self):
        f=open(f'{self.file_directory}','r')
        data=json.load(f)
        f.close()
        return data
    
    def __getitem__(self,key):
        f=open(f'{self.file_directory}','r')
        data=json.load(f)
        f.close()
        return data.get(key)
    
    def __setitem__(self, key: str, value) -> None:
        with open(self.file_directory, "r") as f:
            data = json.load(f)
    
        with open(self.file_directory, "w") as f:
            data[key] = value
            f.write(json.dumps(data))
        
    def keys(self):
        with open(self.file_directory, "r") as f:
            data = json.load(f)
            return data.keys()


def get_time():
    return str(int(time.time() + 0.5 )) 

init_group = {"group-title":"Title", "items":[], "refrences":{}}

# Checking if the .vnote file is not empty and if it was , dump the initial directory data to it
with open(sys.argv[1], "r") as f:
    if f.read() == "":
        group_fname = get_time()
        if not os.path.isdir(USER_FILE_DIRECTORY):
            os.mkdir(USER_FILE_DIRECTORY)


json_file = JsonIt(sys.argv[1])
if __name__ == "__main__":
    print(USER_FILE_DIRECTORY)