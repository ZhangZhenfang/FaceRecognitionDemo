import sys
import cv2
import time
import face_detect_utils
from helloui import Ui_MainWindow
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMainWindow
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage


# 这个窗口继承了用QtDesignner 绘制的窗口
class mywindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)

    def openStream(self):
        th = Thread(self)
        th.changePixmap.connect(self.set_image)
        th.start()

    def snap(self):
        return

    def openImage(self):
        img_name, img_type = QFileDialog.getOpenFileName(self, "选择图片", "", " *.jpg;;*.png;;*.jpeg;;*.bmp")
        print(img_name, img_type)
        # 利用qlabel显示图片
        # print(str(img_name))
        # QtGui.QPixmap.fr
        png = QtGui.QPixmap(img_name).scaled(self.imgLable.width(), self.imgLable.height())# 适应设计label时的大小
        self.imgLable.setPixmap(png)
        print("openImage")

    def recognize(self):
        print("recognize")

    def set_image(self, image):
        self.videoLabel.setPixmap(QPixmap.fromImage(image))

    def image_processing(self):
        img_name, img_type = QFileDialog.getOpenFileName(self, "选择图片", "", " *.jpg;;*.png;;*.jpeg;;*.bmp")
        # 利用qlabel显示图片
        # print(str(img_name))
        png = QtGui.QPixmap(img_type).scaled(self.label_2.width(), self.label_2.height())#适应设计label时的大小
        self.label_2.setPixmap(png)


class Thread(QThread):# 播放视频线程

    changePixmap = pyqtSignal(QtGui.QImage)

    def run(self):
        cap = cv2.VideoCapture(0)
        # print(videoName)
        while cap.isOpened():
            ret, frame = cap.read()
            if ret:
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # 在这里可以对每帧图像进行处理
                face_detect_utils.detect_and_lable(rgb_image)
                convert_to_QtFormat = QtGui.QImage(rgb_image.data, rgb_image.shape[1], rgb_image.shape[0], QImage.Format_RGB888)
                p = convert_to_QtFormat.scaled(320, 240, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                time.sleep(0.001) #控制视频播放的速度
            else:
                break


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = mywindow()
    window.show()
    sys.exit(app.exec_())

