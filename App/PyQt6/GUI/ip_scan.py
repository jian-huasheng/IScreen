import platform
import os
import time
import threading
import socket

from shoot_screen import shoot_image, img_decode_send

live_ip = 0
ips = []
def get_os():
    os = platform.system()
    if os == "Windows":
        return "n"
    else:
        return "c"


def ping_ip(ip_str):
    cmd = ["ping", "-{op}".format(op=get_os()),
           "1", ip_str]
    output = os.popen(" ".join(cmd)).readlines()
    for line in output:
        if str(line).upper().find("TTL") >= 0:
            print("ip: %s 在线" % ip_str)
            global ips
            ips.append(ip_str)
            global live_ip
            live_ip += 1
            break


def find_ip(ip_prefix):
    '''''
    给出当前的ip地址段 ，然后扫描整个段所有地址
    '''
    threads = []
    for i in range(1, 256):
        ip = '%s.%s' % (ip_prefix, i)
        threads.append(threading.Thread(target=ping_ip, args={ip, }))
    for i in threads:
        i.start()
    for i in threads:
        i.join()


def find_local_ip():
    """
    获取本机当前ip地址
    :return: 返回本机ip地址
    """
    myname = socket.getfqdn(socket.gethostname())
    myaddr = socket.gethostbyname(myname)
    return myaddr


# if __name__ == "__main__":
#     print("开始扫描时间: %s" % time.ctime())
#     addr = find_local_ip()
#     args = "".join(addr)
#     ip_pre = '.'.join(args.split('.')[:-1])
#     find_ip(ip_pre)
#     print(ips)
#     print("扫描结束时间 %s" % time.ctime())
#     print('本次扫描共检测到本网络存在%s台设备' % live_ip)

def scan_ip():
    print("开始扫描时间: %s" % time.ctime())
    addr = find_local_ip()
    args = "".join(addr)
    ip_pre = '.'.join(args.split('.')[:-1])
    find_ip(ip_pre)
    print(ips)
    print("扫描结束时间 %s" % time.ctime())
    print('本次扫描共检测到本网络存在%s台设备' % live_ip)
    return ips

def iscreen_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    iscreens = scan_ip()
    # start = False
    for num in range(len(iscreens)):
        print('尝试连接:%s ' % iscreens[num])

        try:
            s.connect((iscreens[num], 9090))
        except ConnectionRefusedError:
            continue
        except OSError:
            break
        else:
            # s.close()
            return(iscreens[num])
            # start = True



def iscreen_start():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((iscreen_ip(), 9090))

    while True:
        # 时间记录
        start_time = time.time()
        # 获取屏幕像素
        new_img = shoot_image()
        new_img = img_decode_send(new_img)
        recv_data = s.recv(2)  # 接收1024个字节
        data = recv_data.decode('utf-8')
        if data:
            # print('接收到的数据为:', recv_data.decode('gbk'))
            if (data == 'ok'):
                s.sendall(new_img)

                end_time = time.time()
                # 计算插值
                elapsed_time = end_time - start_time
                # 打印时长
                # print("包大小: %d 帧率：%.2f FPS" % (len(new_img), (1 / elapsed_time)))
                # print('收到OK')
        else:
            break

def iscreen_start_2(img, s):
    new_img = img
    new_img = img_decode_send(new_img)
    recv_data = s.recv(2)  # 接收1024个字节
    data = recv_data.decode('utf-8')
    if data:
        print('接收到的数据为:', recv_data.decode('gbk'))
        if (data == 'ok'):
            s.sendall(new_img)
            print('收到OK')


