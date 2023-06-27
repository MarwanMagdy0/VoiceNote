from PyQt5.QtWidgets import QWidget, QLineEdit, QVBoxLayout, QLabel
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PIL import Image
from PyQt5 import uic

class VoiceNote(QWidget):
    def __init__(self, parent, path = None):
        super().__init__(parent)
        uic.loadUi("voice_note.ui",self)
        self.path = path
        self.init_audio()
        self.pushButton.clicked.connect(self.toggle_playback)
        self.horizontalSlider.sliderMoved.connect(self.set_position)
    def init_audio(self):
        self.media_player = QMediaPlayer()
        audio_url = QUrl.fromLocalFile(self.path)
        self.media_player.setMedia(QMediaContent(audio_url))
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_slider)
        self.media_player.durationChanged.connect(self.update_duration_label)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def toggle_playback(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
            self.pushButton.setIcon(QIcon("data/play.png"))
            self.timer.stop()
        else:
            self.media_player.play()
            self.pushButton.setIcon(QIcon("data/pause.png"))
            self.timer.start()

    def update_slider(self):
        if self.media_player.duration() > 0:
            self.horizontalSlider.setMaximum(self.media_player.duration())
            self.horizontalSlider.setValue(self.media_player.position())
            self.update_duration_label()

    def update_duration_label(self):
            duration = self.media_player.duration() // 1000
            elapsed = self.media_player.position() // 1000
            remaining = duration - elapsed
            remaining_minutes = remaining // 60
            remaining_seconds = remaining % 60
            self.duration_label.setText(f"{remaining_minutes}:{remaining_seconds:02}")


class EditableLabel(QLabel):
    def __init__(self, existing_label):
        super().__init__("Title")
        self.setGeometry(existing_label.geometry())
        layout = existing_label.parentWidget().layout()
        layout.replaceWidget(existing_label, self)

        existing_label.deleteLater()
        self.line_edit = QLineEdit("")
        self.line_edit.hide()
        self.line_edit.returnPressed.connect(self.finish_editing)

    def mouseDoubleClickEvent(self, event):
        if self.line_edit.isHidden():
            self.line_edit.setText(self.text())
            self.line_edit.setParent(self.parentWidget())
            self.line_edit.setGeometry(self.geometry())
            self.line_edit.show()
            self.line_edit.setFocus()
            self.hide()
        else:
            self.setText(self.line_edit.text())
            self.line_edit.hide()
            self.show()
    
    def finish_editing(self):
        """
        TODO: dont forget to rename the file name with os.rename
        """
        new_text = self.line_edit.text()
        self.line_edit.hide()
        self.setText(new_text)
        self.show()

class Group(QWidget):
    def __init__(self, parent, path = None):
        super().__init__(parent)
        uic.loadUi("group.ui",self)
        self.path = path
        self.title_label = EditableLabel(self.title_label)

class ImageWidget(QWidget):
    def __init__(self, parent, path = None):
        super().__init__(parent)
        uic.loadUi("image.ui",self)
        self.path = path
        self.set_img(path)
    
    def set_img(self, path):
        pixmap = QPixmap(path)
        self.image.setPixmap(pixmap)
