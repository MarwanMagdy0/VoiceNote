import typing
from PyQt5 import QtGui
from PyQt5.QtCore import QObject
from utiles import *

class ImageWidget(QWidget):
    def __init__(self, parent_group, group_fname, image_fname):
        super().__init__(parent_group)
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\image.ui",self)
        self.group_fname = group_fname
        self.image_fname = image_fname
        self.workspace_json_file = parent_group.workspace_json_file
    

    def set_img(self, image_from_object):
        pixmap = QPixmap.fromImage(image_from_object)
        self.image.setPixmap(pixmap)
    

    def load_img(self, path):
        pixmap = QPixmap(path)
        self.image.setPixmap(pixmap)
    

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            edit_image = EditImage(self, self.group_fname, self.image_fname)
            edit_image.image_is_deleted.connect(self.deleteLater)
            edit_image.image_is_saved.connect(self.save_new_image)
            edit_image.setWindowModality(Qt.ApplicationModal)
            edit_image.show()


    def save_new_image(self, qimg):
        pixmap = QPixmap.fromImage(qimg)
        self.image.setPixmap(pixmap)



class EditImage(QDialog):
    image_is_deleted = pyqtSignal()
    image_is_saved   = pyqtSignal(QImage)
    def __init__(self, parent, group_fname, image_fname):
        super().__init__(parent)
        self.workspace_json_file = parent.workspace_json_file
        self.drawing_color = [255,255,255]
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\edit_image.ui",self)
        self.setWindowTitle("Image Editor")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.group_fname = group_fname
        self.image_fname = image_fname
        self.pixmap = QPixmap(self.workspace_json_file.file_directory + "\\" + self.group_fname + "\\" + self.image_fname)
        self.src_frame = cv2.imread(self.workspace_json_file.file_directory + "\\" + self.group_fname + "\\" + self.image_fname)
        self.edit_frame = self.src_frame.copy()
        self.image.setPixmap(self.pixmap)
        self.delete_button.clicked.connect(self.delete_image)
        self.choose_color_button.clicked.connect(self.choose_color_method)
        self.save_button.clicked.connect(self.save_image_method)
        self.image.mouseMoveEvent = self.mouse_moved_over_image
        self.points_buffer = []
        self.selection_width = 5
        self.cropping_mode = False


    def save_image_method(self):
        cv2.imwrite(self.workspace_json_file.file_directory + "\\" + self.group_fname + "\\" + self.image_fname,self.edit_frame)
        self.image_is_saved.emit(self.frame2qimg(self.edit_frame))
        self.close()


    def delete_image(self):
        if message_box():
            data = self.workspace_json_file.read_data()
            data[self.group_fname]["items"].remove(self.image_fname)
            self.workspace_json_file.save_data(data)
            self.image_is_deleted.emit()
            os.remove(self.workspace_json_file.file_directory + "\\" + self.group_fname + "\\" + self.image_fname)
            self.close()


    def frame2qimg(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        q_img = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return q_img

    def set_image_from_frame(self, frame : np.ndarray):
        q_img = self.frame2qimg(frame)
        pixmap = QPixmap.fromImage(q_img)
        self.image.setPixmap(pixmap)
    

    def choose_color_method(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.drawing_color = [color.blue(), color.green(), color.red()]
    

    def mouse_moved_over_image(self, event):
        mouse_pos = event.pos()
        x,y = mouse_pos.x(), mouse_pos.y()
        if event.buttons() == Qt.LeftButton:
            self.points_buffer.append((x,y))
            if len(self.points_buffer)>2:
                cv2.line(self.edit_frame, self.points_buffer[0], self.points_buffer[1], self.drawing_color, self.selection_width)
                self.points_buffer.pop(0)
                self.set_image_from_frame(self.edit_frame)
        
        elif event.buttons() == Qt.RightButton:
            self.edit_frame[y - self.selection_width * 3//2:y+self.selection_width * 3//2, x- self.selection_width * 3//2:x+self.selection_width * 3//2] = self.src_frame[y - self.selection_width * 3//2:y+self.selection_width * 3//2, x - self.selection_width * 3//2:x+self.selection_width * 3//2]
            self.set_image_from_frame(self.edit_frame)


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.points_buffer = []
    


class CameraCapture(QDialog):
    image_is_deleted = pyqtSignal()
    image_is_saved_from_camera   = pyqtSignal(str)
    def __init__(self, parent_group, group_fname):
        super().__init__(parent_group)
        self.workspace_json_file = parent_group.workspace_json_file
        uic.loadUi(SCRIPT_DIRECTORY + "\\" + "ui\\open_camera.ui",self)
        self.setWindowTitle("Image Editor")
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.group_fname = group_fname
        self.pause_stream_button.clicked.connect(self.pause_stream_method)
        self.save_image_button.clicked.connect(self.save_image_method)
        self.flip_box.stateChanged.connect(self.img_is_flipped)
        self.camera_thread = CameraThread()
        self.camera_thread.frame_captured.connect(lambda qimg: self.set_image_from_qimg(qimg))
        self.camera_thread.start()
    
    def set_image_from_qimg(self, qimg):
        if self.isVisible():
            pixmap = QPixmap.fromImage(qimg)
            self.image.setPixmap(pixmap)

    
    def img_is_flipped(self, state):
            self.camera_thread.is_flipped = state
    
    def save_image_method(self):
        image_fname = get_time() + ".png"
        self.camera_thread.requestInterruption()
        self.camera_thread.save_img(self.workspace_json_file.file_directory + "\\" + self.group_fname + "\\" + image_fname)
        data = self.workspace_json_file.read_data()
        data[self.group_fname]["items"].append(image_fname)
        self.workspace_json_file.save_data(data)
        self.image_is_saved_from_camera.emit(image_fname)
        self.close()
    
    def pause_stream_method(self):
        if self.camera_thread.pause == False:
            self.camera_thread.pause = True
        else:
            self.camera_thread.pause = False

    def closeEvent(self, event):
        self.camera_thread.requestInterruption()
        self.close()


class CameraThread(QThread):
    frame_captured = pyqtSignal(QImage)
    def __init__(self):
        super().__init__()
        self.pause = False
        self.last_frame = None
        self.is_flipped = False
    def run(self):
        self.cap = cv2.VideoCapture(0)
        while not self.isInterruptionRequested():
            ret, frame = self.cap.read()
            if ret and not self.pause:
                if self.is_flipped:
                    frame = cv2.flip(frame, 1)

                self.last_frame = frame
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                q_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                self.frame_captured.emit(q_image)
            cv2.waitKey(1)
        self.cap.release()
    
    def save_img(self, path):
        if self.last_frame is not None:
            cv2.imwrite(path, self.last_frame)

