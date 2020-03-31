#!/usr/bin/env python
# coding=utf-8
from modes.tank.mqtt import mqtt_send


import numpy as np
import cv2
import socket
import threading
import os

import queue

que = queue.Queue()
lock = threading.Lock()
count = 0


# port = 36660

cam_flag = 0

# udp连接 服务端

photo_flag = 0
photo = None
lastServer = None


class ImgServer(object):
    def __init__(self, choice=None, addr_port=36660):
        self.port = addr_port
        self.recv = 40 * 1024  # 接受缓冲区大小, 要设置足够大来接受一帧图片
        self.type = choice

    def get_addr(self):
        # 获取本机计算机名称
        hostname = socket.gethostname()
        # ip = socket.gethostbyname(hostname)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 26660))
        ip = s.getsockname()[0]
        # 获取本机ip
        host = (ip, self.port)
        print('主机名： '+str(hostname) + ' 地址：' + str(ip) + ':' +str(self.port))
        return host

    def set_server(self):
        if lastServer:
            try:
                lastServer.close()
            except Exception as e:
                print(str(e))
        udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_server.bind(self.get_addr())
        print('服务端开启')
        return udp_server

    def close_server(self):
        self.set_server().close()

    def img_data(self):
        img = ''
        global photo, photo_flag, lastServer
        udp_server = self.set_server()
        lastServer = udp_server
        app_path = os.getcwd()
        faceCascade = cv2.CascadeClassifier(os.path.join(app_path, 'static/cascade/haarcascade_eye.xml'))
        eyesCascade = cv2.CascadeClassifier(os.path.join(app_path, 'static/cascade/haarcascade_frontalface_alt.xml'))
        type_dic = {'eyes': faceCascade, 'face': faceCascade}
        RGBImg = ''
        while 1:
            data = udp_server.recvfrom(self.recv)
            bytes_img = data[0]
            img_length = len(data[0])
            if img_length:
                image = cv2.imdecode(np.frombuffer(bytes_img, dtype=np.uint8), cv2.IMREAD_COLOR)
                photo = image
                photo_flag = 1
                try:
                    if self.type != 'origin':
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        squares = type_dic[self.type].detectMultiScale(
                            gray,
                            scaleFactor=1.2,
                            minNeighbors=5,
                            minSize=(20, 20)
                        )
                        for (x, y, w, h) in squares:
                            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                            if self.type == 'eyes':
                                face_gray = gray[y:y + h, x:x + w]
                                face_color = image[y:y + h, x:x + w]
                                eyes = eyesCascade.detectMultiScale(face_gray, scaleFactor=1.2, minNeighbors=10, )
                                for (e_x, e_y, e_w, e_h) in eyes:
                                    cv2.rectangle(face_color, (e_x, e_y), (e_x + e_w, e_y + e_h), (0, 255, 0), 2)
                finally:
                    if cam_flag:
                        udp_server.close()
                        cv2.destroyAllWindows()
                        break
                RGBImg = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            yield RGBImg


def close_camera_client():
    global cam_flag, photo, photo_flag
    photo_flag = 0
    mqtt_send('camera_close')
    cam_flag = 1
    return {'ret': True, 'msg': '客户端接收关闭！'}


def open_camera_client():
    global cam_flag
    cam_flag = 0
    result = mqtt_send('camera_open')
    return result


def take_photo():
    if photo_flag:
        result = {'ret': True, 'msg': ''}
    else:
        result = {'ret': False, 'msg': '没有打开摄像头'}
    return result