from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TabWidget(object):

    def setupUi(self, TabWidget):
        TabWidget.setObjectName("TabWidget") #创建的是"TabWidget"
        TabWidget.resize(789, 619)
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab") #"第一个子窗口"
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(10, 30, 75, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.tab)
        self.pushButton_2.setGeometry(QtCore.QRect(10, 90, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(110, 30, 461, 311))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(620, 30, 151, 341))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        TabWidget.addTab(self.tab, "")
        self.tab1 = QtWidgets.QWidget() # "第二个子窗口"
        self.tab1.setObjectName("tab1")
        TabWidget.addTab(self.tab1, "")
        self.tab_2 = QtWidgets.QWidget() #"第三个子窗口"
        self.tab_2.setObjectName("tab_2")
        TabWidget.addTab(self.tab_2, "")

        self.retranslateUi(TabWidget)
        TabWidget.setCurrentIndex(0)
        self.pushButton.clicked.connect(TabWidget.image_processing) #将按键与事件相连
        self.pushButton_2.clicked.connect(TabWidget.video_processing)
        QtCore.QMetaObject.connectSlotsByName(TabWidget)

    def retranslateUi(self, TabWidget):
        _translate = QtCore.QCoreApplication.translate
        TabWidget.setWindowTitle(_translate("TabWidget", "TabWidget"))
        self.pushButton.setText(_translate("TabWidget", "打开图片"))
        self.pushButton_2.setText(_translate("TabWidget", "打开视频"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab), _translate("TabWidget", "Tab 1"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab1), _translate("TabWidget", "Tab 2"))
        TabWidget.setTabText(TabWidget.indexOf(self.tab_2), _translate("TabWidget", "页"))

