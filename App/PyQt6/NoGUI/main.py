import cv2 #opencv读取的格式是BGR
import numpy as np
import socket
import time
import pyautogui

def shoot_image():
    #时间记录
    start_time = time.time()
    # #设置屏幕区域
    # monitor = (0, 0, 1920, 1080)
    # 设置捕获对象
    screenshot = pyautogui.screenshot()#region=monitor
    # 数据转换
    screenshot_np = np.array(screenshot)
    # 设置JPEG图像的质量参数为50
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    # 将 BGR 转换为 RGB (OpenCV 默认使用 RGB)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    # 压缩到指定的像素尺寸
    screenshot_image = cv2.resize(screenshot_np, (320, 172))
    # 解码为JPG格式
    _, image_data = cv2.imencode('.jpg', screenshot_image, encode_param)
    # 获取字长
    lent = len(image_data)
    # 字长转byte
    h = lent.to_bytes(2, byteorder='big')
    # list结合首位长度字节
    new_img = list(h) + list(image_data)
    # list转byte发送
    new_img = bytes(new_img)
    # 时间记录结束
    end_time = time.time()
    # 计算插值
    elapsed_time = end_time - start_time
    # 打印时长
    print("图像转换用时：%.2f s" % (elapsed_time))
    return new_img

# 电脑指向设备ip,指定连接(客户端)
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("输入IP地址：123.345.789.123",9090))#151

while True:
    # 时间记录
    start_time = time.time()
    # 获取屏幕像素
    new_img = shoot_image()
    # 接收对方发送过来的数据
    recv_data = s.recv(2)  # 接收1024个字节
    data = recv_data.decode('utf-8')
    if data:
        print('接收到的数据为:', recv_data.decode('gbk'))
        if (data == 'ok'):

            # 计时开始
            s.sendall(new_img)
            # 时间记录结束
            end_time = time.time()
            # 计算插值
            elapsed_time = end_time - start_time
            # 打印时长
            print("包大小: %d 帧率：%.2f FPS" %(len(new_img),(1/elapsed_time)))
            print('收到OK')

    else:
        break
