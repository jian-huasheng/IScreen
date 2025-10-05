# -*- coding: gbk -*-
# ����
# coding=gbk

import cv2
import numpy as np
import pyautogui
from PyQt6.QtGui import QPixmap, QImage

"---��ȡ������Ļ---"
"---shoot_image---"

def shoot_image():

    # #������Ļ����
    monitor = (0, 0, 1920, 1080)
    # ���ò������
    screenshot = pyautogui.screenshot(region=monitor)
    # ����ת��
    screenshot_np = np.array(screenshot)
    # �� BGR ת��Ϊ RGB (OpenCV Ĭ��ʹ�� RGB)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    # ѹ����ָ�������سߴ�
    screenshot_image = cv2.resize(screenshot_np, (320, 172))
    # ����JPEGͼ�����������Ϊ50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    # ����ΪJPG��ʽ
    _, image_data = cv2.imencode('.jpg', screenshot_image, encode_param)

    return image_data

"---����IScreen��Ļ��С��ͼ������size_quality---"
"---��ȡ������Ļ---"
"---shoot_image_sq---"

def shoot_image_sq(i_width, i_height, i_quality):

    # #������Ļ����
    # monitor = (0, 0, 1920, 1080)
    # ���ò������
    screenshot = pyautogui.screenshot()#region=monitor
    # ����ת��
    screenshot_np = np.array(screenshot)
    # �� BGR ת��Ϊ RGB (OpenCV Ĭ��ʹ�� RGB)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    # ѹ����ָ�������سߴ�
    screenshot_image = cv2.resize(screenshot_np, (i_width, i_height))
    # ����JPEGͼ�����������Ϊ50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), i_quality]
    # ����ΪJPG��ʽ
    _, image_data = cv2.imencode('.jpg', screenshot_image, encode_param)

    return image_data

"---����IScreen��Ļ��С��ͼ������size_quality---"
"---��ȡ��������ͷ---"
"---camera_eyes---"
# ����Haar����������
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# 0Ϊ������������ͷ
# capture = cv2.VideoCapture(0)


def camera_eyes(capture):

    # ����ͷ��ȡ,retΪ�Ƿ�ɹ�������ͷ,true,false�� frameΪ��Ƶ��ÿһ֡ͼ��
    ret, frame = capture.read()
    # ����ͷ�Ǻ��˶����ģ���ͼ�����ҵ�������������ʾ
    frame = cv2.flip(frame, 1)

    # �Ҷȱ任
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # �۾����
    # eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    # # eye_image = 0
    # # ������⵽�۾����ٳ�
    # for (x, y, w, h) in eyes:
    #     eye_image = frame[y: y + h, x: x + w]
    # #     # cv2.imshow("Detected Eye", eye_image)

    # ѹ����ָ�������سߴ�
    eye_image = cv2.resize(frame, (320, 172))
    # ����JPEGͼ�����������Ϊ50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    # ����ΪJPG��ʽ
    _, image_data = cv2.imencode('.jpg', eye_image, encode_param)
    return image_data

"---��ȡ��������ͷ---"
"---camera_eyes---"
# ����Haar����������
# eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
# 0Ϊ������������ͷ

# capture = cv2.VideoCapture(0)
def camera_eyes_sq(capture, i_width, i_height, i_quality):

    ret, frame = capture.read()
    # ����ͷ�Ǻ��˶����ģ���ͼ�����ҵ�������������ʾ
    frame = cv2.flip(frame, 1)
    # cv2.imshow("video", frame)

    # �Ҷȱ任
    # gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # �۾����
    # eyes = eye_cascade.detectMultiScale(gray_image, scaleFactor=1.1, minNeighbors=5)
    # eye_image = 0
    # ������⵽�۾����ٳ�
    # for (x, y, w, h) in eyes:
    #     eye_image = frame[y: y + h, x: x + w]
    #     # cv2.imshow("Detected Eye", eye_image)

    # ѹ����ָ�������سߴ�
    eye_image = cv2.resize(frame, (i_width, i_height))
    # ����JPEGͼ�����������Ϊ50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), i_quality]
    # ����ΪJPG��ʽ
    _, image_data = cv2.imencode('.jpg', eye_image, encode_param)
    return image_data


"---ͼ�����ݱ����bytes��---"
"---img_decode_send---"
def img_decode_send(image_data):
    # ��ȡ�ֳ�
    lent = len(image_data)
    # �ֳ�תbyte
    h = lent.to_bytes(2, byteorder='big')
    # list�����λ�����ֽ�
    new_img = list(h) + list(image_data)
    # listתbyte����
    new_img = bytes(new_img)
    print(len(new_img))
    return new_img


"---ͼ�����ݱ����cv2��ʾ---"
"---img_decode_cv2_show---"
def img_decode_cv2_show(image_data):
    new_img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    return new_img


"---ͼ�����ݱ����pixmap��ʾ---"
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
# # ��ʾͼ��
#     img = shoot_image()
#     img = img_decode_show(img)
#     cv2.imshow("img",img)
# # �ȴ�10����
#     if cv2.waitKey(10) & 0xFF == ord('q'):
#         break
# cv2.destroyAllWindows()