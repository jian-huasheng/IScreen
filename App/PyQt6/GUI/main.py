####### [signals_and_slots] #######
import socket
import time

import cv2
import numpy as np
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot, QObject
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QVBoxLayout, QWidget, QPushButton, \
    QHBoxLayout, QSpinBox, QFormLayout
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC
from PyQt6.QtCore import QTimer
import sys
import shoot_screen

from ip_scan import iscreen_start, iscreen_ip, iscreen_start_2
from PyQt6.QtCore import QThread



class MainWindow(QMainWindow):
    # 信号槽传输图片
    img_change = pyqtSignal(np.ndarray)

    def __init__(self):
        super().__init__()
        # form左标签右输入
        form = QFormLayout()
        # 默认参数设置->图像的宽,高,质量,图像是否可以修改使能
        self.i_width = 320
        self.i_height = 172
        self.i_quality = 50
        self.i_adjust = True
        # 窗口设置
        self.setWindowTitle("IScreen")
        self.resize(488, 172)

        # 无边框
        # self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # 透明窗
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # 按钮1: Start
        self.button1 = QPushButton("Start", self)
        self.button1.setStyleSheet("QpushButton:pressed{background-color: yellow}")
        self.button1.setStyleSheet("color: #EC35FA")
        self.button1.clicked.connect(self.start)
        # 按钮2: DeskTop/Camera 切换屏幕录制或摄像头录制
        self.button2 = QPushButton("DeskTop", self)
        self.button2.setStyleSheet("QpushButton:pressed{background-color: yellow}")
        self.button2.setStyleSheet("color: #FA77F8")
        self.button2.clicked.connect(self.button2_clicked)

        # 设置输出图片大小和质量i_width, i_height, i_quality
        self.screen_width = QSpinBox()
        self.screen_width.setRange(0, 4096)
        self.screen_width.setValue(self.i_width)
        self.screen_width.setSingleStep(10)
        form.addRow("Width", self.screen_width)

        self.screen_height = QSpinBox()
        self.screen_height.setRange(0, 4096)
        self.screen_height.setValue(self.i_height)
        self.screen_height.setSingleStep(10)
        form.addRow("Height",self.screen_height)

        self.img_quality = QSpinBox()
        self.img_quality.setRange(1, 100)
        self.img_quality.setValue(self.i_quality)
        self.img_quality.setSingleStep(10)
        form.addRow("Quality", self.img_quality)

        # 设置回调函数
        self.screen_width.valueChanged.connect(self.width_changed)
        self.screen_height.valueChanged.connect(self.height_changed)
        self.img_quality.valueChanged.connect(self.quality_changed)

        # print(self.i_width,self.i_height,self.i_quality)

        # FPS绘制,plot设置
        self.fps = 0.0
        self.fig = plt.figure()
        plt.rcParams.update({'font.size': 4})
        self.canvas = FC(self.fig)
        self.y = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # y轴

        # 定时刷新图片和fps画布
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_plot)
        self.timer1.start(1000)

        self.timer2 = QTimer(self)
        self.timer2.timeout.connect(self.update_pic)
        self.timer2.start(10)

        # 默认读取桌面图片
        self.img = shoot_screen.shoot_image()
        self.img = shoot_screen.img_decode_pyqt_imshow(self.img)
        self.pix_w = QLabel("pic_show")
        self.pix_w.setPixmap(self.img)

        # 布局规划 V H form ->layout
        bbox = QHBoxLayout()
        bbox.addWidget(self.button2, 1)
        bbox.addWidget(self.button1, 1)

        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addWidget(self.canvas)
        vbox.addLayout(bbox)

        hbox = QHBoxLayout()
        hbox.addWidget(self.pix_w)
        hbox.addLayout(vbox)

        # 创建用户界面对象QWidge
        container = QWidget()
        container.setLayout(hbox)
        container.setStyleSheet("background-color: #FCF0FB")
        self.setCentralWidget(container)

    # 按钮1回调函数: 失能窗口调节图片大小,创建发送图像线程,连接图像传输槽
    def start(self):
        self.i_adjust = False
        self.work = WorkThread()
        self.work.start()
        self.work.fps_change.connect(self.update_fps)
        self.img_change.connect(self.work.img_update)

    # 按钮2回调函数: 切换DeskTop/Camera,创建摄像头,释放摄像头
    def button2_clicked(self):
        # print("button2_clicked")
        if self.button2.text() == "DeskTop":
            self.capture = cv2.VideoCapture(0)
            self.button2.setText("Camera")
        elif self.button2.text() == "Camera":
            self.capture.release()
            self.button2.setText("DeskTop")

    # timer1回调函数: 读取fps数值,更新fps画布
    def update_plot(self):
        fps = self.fps
        for i in range(len(self.y) - 1):
            self.y[i] = self.y[i + 1]
            self.y[i + 1] = fps
        plt.cla()  # 清空画布
        plt.plot(self.y, color='#FAAEF1', linewidth=0.5, linestyle='-', marker='.')
        plt.ylabel("FPS")
        self.canvas.draw()  # 绘制
    # timer2回调函数: 读取button2.text切换输出图像数据,传递到信号槽img_change,更新画布
    def update_pic(self):
        if self.button2.text() == "Camera":
            self.img = shoot_screen.camera_eyes_sq(self.capture,self.i_width,self.i_height,self.i_quality)
        else:
            self.img = shoot_screen.shoot_image_sq(self.i_width,self.i_height,self.i_quality)
        self.img_change.emit(self.img)
        self.img = shoot_screen.img_decode_pyqt_imshow(self.img)
        self.pix_w.setPixmap(self.img)
        self.canvas.draw()  # 绘制
    # fps信号槽接收函数,读取fps
    @pyqtSlot(float)
    def update_fps(self, fps):
        # print('FPS: %.2f' % fps)
        self.fps = fps
    # 数值微调框回调函数,读取i_width, i_height, i_quality
    def width_changed(self):
        if self.i_adjust:
            self.i_width = self.screen_width.value()
            # print("width_changed:", self.i_width)

    def height_changed(self):
        if self.i_adjust:
            self.i_height = self.screen_height.value()
            # print("height_changed:", self.i_height)

    def quality_changed(self):
        self.i_quality = self.img_quality.value()
        # print("quality_changed:", self.i_quality)


# 新线程: 用于图像发送
class WorkThread(QThread):
    # 信号槽传输fps
    fps_change = pyqtSignal(float)

    def __init__(self):
        super(WorkThread, self).__init__()

    # 读取图像传输槽的图像
    @pyqtSlot(np.ndarray)
    def img_update(self, value: np.ndarray):
        self.img = value
        # print(self.img)

    # 图像socket传输
    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        ip = iscreen_ip()
        if ip:
            s.connect((ip, 9090))
            while True:
                # 时间记录
                start_time = time.time()
                img = self.img
                iscreen_start_2(img, s)
                end_time = time.time()
                # 计算插值
                elapsed_time = end_time - start_time

                fps = 1 / elapsed_time
                fps = round(fps, 2)
                self.fps_change.emit(fps)
                # 打印时长
                # print("包大小: %d 帧率：%0.2f FPS" % (len(img), (fps)))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()


