#!/usr/bin/env python
# coding=utf-8
import paho.mqtt.client as mqtt
import socket

HOST = 'www.3000iot.com'
PORT = 1883
USER = 'NBguest'
PASSWORD = 'NBguest12'


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))


def on_message(client, userdata, msg):
    print("主题:"+msg.topic+" 消息:"+str(msg.payload.decode('utf-8')))
    msg = msg.payload.decode('utf-8')
    if msg.startswith('voice_recognize'):
        text = msg.split(":")[1]
        print(text)


client = mqtt.Client()
client.username_pw_set(USER, PASSWORD)
client.on_connect = on_connect
client.connect(HOST, PORT, 60)
client.on_message = on_message
client.loop_start()
server_topic = None
client_topic = None


def mqtt_send(command=None):
    global server_topic
    device_id = ''
    try:
        with open('./mac.config', 'r') as f:
            config_dic = eval(f.read())
            device_id = config_dic['device_id']
    except Exception as e:
        print('mqtt_send'+str(e))
        return {'ret': False, 'msg': '配置文件丢失或者被破坏！'+str(e)}

    if command and device_id:
        try:
            server_topic = 'aicar_pc' + device_id
            print('topic: ' +server_topic+' command: '+command)
            client.publish(server_topic, command, 1)
            return {'ret': True, 'msg': ''}
        except Exception as e:
            return {'ret': False, 'msg': 'error : '+str(e)}
    elif not command:
        return {'ret': True, 'msg': '指令不得为空！'}
    else:
        return {'ret': False, 'msg': '请先连接设备！！！'}


def connect_mqtt(device_id):
    if device_id:
        client_topic = 'aicar_pi' + device_id
        client.subscribe(client_topic)
        local_ip = ''
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 26660))
            local_ip = s.getsockname()[0]
        except Exception as e:
            return {'ret': False, 'msg': '获取本地ip失败！'+str(e)}
        try:
            with open('./mac.config', 'r+') as f:
                config_dic = eval(f.read())
                config_dic['device_id'] = device_id
                f.seek(0)
                f.write(str(config_dic))
        except Exception as e:
            print('connect'+str(e))
            return {'ret': False, 'msg': '配置文件丢失或者被破坏！'}
        mqtt_send('connect:' + local_ip)
        return {'ret': True, 'msg': '连接成功！设备号： '+device_id}
    return {'ret': False, 'msg': '连接失败！'}







