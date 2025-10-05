# -*- coding: gbk -*-
# 或者
# coding=gbk

import cv2
import numpy as np
import pyautogui
from PyQt6.QtGui import QPixmap, QImage

"---获取电脑屏幕---"
"---shoot_image---"

def shoot_image():

    # #设置屏幕区域
    monitor = (0, 0, 1920, 1080)
    # 设置捕获对象
    screenshot = pyautogui.screenshot(region=monitor)
    # 数据转换
    screenshot_np = np.array(screenshot)
    # 将 BGR 转换为 RGB (OpenCV 默认使用 RGB)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    # 压缩到指定的像素尺寸
    screenshot_image = cv2.resize(screenshot_np, (320, 172))
    # 设置JPEG图像的质量参数为50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    # 解码为JPG格式
    _, image_data = cv2.imencode('.jpg', screenshot_image, encode_param)

    return image_data

"---输入IScreen屏幕大小和图像质量size_quality---"
"---获取电脑屏幕---"
"---shoot_image_sq---"

def shoot_image_sq(i_width, i_height, i_quality):

    # #设置屏幕区域
    # monitor = (0, 0, 1920, 1080)
    # 设置捕获对象
    screenshot = pyautogui.screenshot()#region=monitor
    # 数据转换
    screenshot_np = np.array(screenshot)
    # 将 BGR 转换为 RGB (OpenCV 默认使用 RGB)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    # 压缩到指定的像素尺寸
    screenshot_image = cv2.resize(screenshot_np, (i_width, i_height))
    # 设置JPEG图像的质量参数为50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), i_quality]
    # 解码为JPG格式
    _, image_data = cv2.imencode('.jpg', screenshot_image, encode_param)

    return image_data

"---输入IScreen屏幕大小和图像质量size_quality---"
"---获取电脑摄像头---"
"---camera_eyes---"
# 加载Haar特征分类器
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# 0为电脑内置摄像头
# capture = cv2.VideoCapture(0)


def camera_eyes(capture):

    # 摄像头读取,ret为是否成功打开摄像头,true,false。 frame为视频的每一帧图像
    ret, frame = capture.read()
    # 摄像头是和人对立的，将图像左右调换回来正常显示
    frame = cv2.flip(frame, 1)

    # 灰度变换
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 眼睛检测
    # eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    # # eye_image = 0
    # # 遍历检测到眼睛并抠出
    # for (x, y, w, h) in eyes:
    #     eye_image = frame[y: y + h, x: x + w]
    # #     # cv2.imshow("Detected Eye", eye_image)

    # 压缩到指定的像素尺寸
    eye_image = cv2.resize(frame, (320, 172))
    # 设置JPEG图像的质量参数为50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    # 解码为JPG格式
    _, image_data = cv2.imencode('.jpg', eye_image, encode_param)
    return image_data

"---获取电脑摄像头---"
"---camera_eyes---"
# 加载Haar特征分类器
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# 0为电脑内置摄像头

# capture = cv2.VideoCapture(0)
def camera_eyes_sq(capture, i_width, i_height, i_quality):

    ret, frame = capture.read()
    # 摄像头是和人对立的，将图像左右调换回来正常显示
    frame = cv2.flip(frame, 1)
    # cv2.imshow("video", frame)

    # 灰度变换
    # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 眼睛检测
    # eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    # eye_image = 0
    # 遍历检测到眼睛并抠出
    # for (x, y, w, h) in eyes:
    #     eye_image = frame[y: y + h, x: x + w]
    #     # cv2.imshow("Detected Eye", eye_image)

    # 压缩到指定的像素尺寸
    eye_image = cv2.resize(frame, (i_width, i_height))
    # 设置JPEG图像的质量参数为50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), i_quality]
    # 解码为JPG格式
    _, image_data = cv2.imencode('.jpg', eye_image, encode_param)
    return image_data


"---图像数据编解码bytes流---"
"---img_decode_send---"
def img_decode_send(image_data):
    # 获取字长
    lent = len(image_data)
    # 字长转byte
    h = lent.to_bytes(2, byteorder='big')
    # list结合首位长度字节
    new_img = list(h) + list(image_data)
    # list转byte发送
    new_img = bytes(new_img)
    print(len(new_img))
    return new_img


"---图像数据编解码cv2显示---"
"---img_decode_cv2_show---"
def img_decode_cv2_show(image_data):
    new_img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return new_img


"---图像数据编解码pixmap显示---"
"---img_decode_show---"
def img_decode_pyqt_imshow(img):
    img = img_decode_cv2_show(img)
    width = img.shape[1]
    height = img.shape[0]
    cv2.cvtColor(img, cv2.COLOR_BGR2RGB, img)
    qt_img = QImage(img.data, width, height, QImage.Format.Format_RGB888)
    qt_img = QPixmap.fromImage(qt_img)
    return qt_img

# img = shoot_image()
# print(img_decode_send(img))
# img = cv2.imdecode(img, cv2.IMREAD_COLOR)
# # print(img)
# cv2.imshow("img",img)

# while True:
# # 显示图像
#     img = shoot_image()
#     img = img_decode_show(img)
#     cv2.imshow("img",img)
# # 等待10毫秒
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()