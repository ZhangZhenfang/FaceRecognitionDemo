import sys
import cv2
import time
import face_detect_utils
import numpy as np
import load
from helloui import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage


# 这个窗口继承了用QtDesignner 绘制的窗口
class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setupUi(self)
        self.th = None
        self.current_image = None

    def openStream(self):
        self.th = Thread(self)
        self.th.changePixmap.connect(self.set_video_image)
        self.th.start()

    def snap(self):
        ret, frame = self.th.cap.read()
        if ret:
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            self.current_image = rgb_image
            face_detect_utils.detect_and_label(rgb_image)
            convert_to_QtFormat = QtGui.QImage(rgb_image.data, rgb_image.shape[1],
                                               rgb_image.shape[0],
                                               QImage.Format_RGB888)
            p = convert_to_QtFormat.scaled(320, 240, Qt.KeepAspectRatio)
            self.set_image(self.imgLabel, p)

    def openImage(self):
        img_name, img_type = QFileDialog.getOpenFileName(self, "选择图片", "", " *.bmp;;*.jpg;;*.png;;*.jpeg")
        print(img_name, img_type)
        imread = cv2.imread(img_name)
        imread = cv2.cvtColor(imread, cv2.COLOR_BGR2GRAY)
        imread = imread / 255.
        imread = cv2.resize(imread, (28, 28))
        self.current_image = np.reshape(imread, (1, 28, 28, 1))
        # 利用qlabel显示图片
        # 适应设计label时的大小
        png = QtGui.QPixmap(img_name).scaled(self.imgLabel.width(), self.imgLabel.height())
        self.imgLabel.setPixmap(png)
        print("openImage")

    def recognize(self):
        result = load.predict(self.current_image)
        print(result)
        self.resultNumber.setProperty("intValue", int(result[0]))

    def set_video_image(self, image):
        self.set_image(self.videoLabel, image)

    def set_image(self, label, image):
        label.setPixmap(QPixmap.fromImage(image))


# 播放视频线程
class Thread(QThread):
    def __init__(self, other):
        super(Thread, self).__init__()
        self.cap = None
        self.pause = False

    changePixmap = pyqtSignal(QtGui.QImage)

    def run(self):
        self.cap = cv2.VideoCapture(0)
        while self.cap.isOpened():
            if 1 - self.pause:
                ret, frame = self.cap.read()
                if ret:
                    rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    # 在这里可以对每帧图像进行处理
                    # face_detect_utils.detect_and_label(rgb_image)
                    convert_to_QtFormat = QtGui.QImage(rgb_image.data, rgb_image.shape[1],
                                                       rgb_image.shape[0],
                                                       QImage.Format_RGB888)
                    p = convert_to_QtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                    self.changePixmap.emit(p)
                else:
                    break
                time.sleep(0.02)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())

