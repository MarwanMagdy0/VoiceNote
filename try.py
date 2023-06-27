import sys
import pyaudio
import wave
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel
from PyQt5.QtCore import QThread, pyqtSignal

class AudioRecorder(QThread):
    audio_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.frames = []

    def run(self):
        # Audio settings
        FORMAT = pyaudio.paInt16  # Audio format
        CHANNELS = 1  # Mono audio
        RATE = 44100  # Sample rate (Hz)
        CHUNK = 1024  # Buffer size

        self.stream = self.audio.open(format=FORMAT,
                                      channels=CHANNELS,
                                      rate=RATE,
                                      input=True,
                                      frames_per_buffer=CHUNK)

        self.frames = []
        while not self.isInterruptionRequested():
            data = self.stream.read(CHUNK)
            self.frames.append(data)

        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()

        self.audio_finished.emit()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Audio Recorder")

        self.record_button = QPushButton("Record", self)
        self.record_button.setGeometry(50, 50, 100, 50)
        self.record_button.clicked.connect(self.start_recording)

        self.stop_button = QPushButton("Stop Recording", self)
        self.stop_button.setGeometry(160, 50, 130, 50)
        self.stop_button.clicked.connect(self.stop_recording)
        self.stop_button.setEnabled(False)

        self.status_label = QLabel("Click 'Record' to start recording", self)
        self.status_label.setGeometry(50, 110, 250, 20)

        self.recorder = AudioRecorder()
        self.recorder.audio_finished.connect(self.recording_finished)

    def start_recording(self):
        self.status_label.setText("Recording...")
        self.record_button.setEnabled(False)
        self.stop_button.setEnabled(True)

        self.recorder.start()

    def stop_recording(self):
        self.recorder.requestInterruption()

    def recording_finished(self):
        # Save the recorded audio to a file
        wave_file = wave.open("output.wav", 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(self.recorder.audio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(44100)
        wave_file.writeframes(b''.join(self.recorder.frames))
        wave_file.close()

        self.status_label.setText("Recording saved to output.wav")
        self.record_button.setEnabled(True)
        self.stop_button.setEnabled(False)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setGeometry(300, 300, 350, 200)
    window.show()
    sys.exit(app.exec_())
