from __init__ import ConfigPath


conf = "{'device_id': ''}"


# 生成配置文件
def _reset():
    fp = open(ConfigPath, 'w')
    fp.write(conf)
    fp.close()


# 写入文件
def _write(data):
    with open(ConfigPath, 'r+') as f:
        config_dic = eval(f.read())
        config_dic['device_id'] = data
        f.seek(0)
        f.truncate()
        f.write(str(config_dic))


"""重置配置文件"""


def reset_config():
    try:
        _write('')
    except Exception as e:
        _reset()


"""写入设备号"""


def save_device(device_id):
    try:
        _write(device_id)
        return {'ret': True, 'msg': ''}
    except Exception as e:
        _reset()
        return {'ret': False, 'msg': '配置文件丢失或损坏，请重试！'}


"""读取设备号"""


def load_config():
    try:
        with open(ConfigPath, 'r') as f:
            config_dic = eval(f.read())
            device_id = config_dic['device_id']
            return {'ret': True, 'msg': device_id}
    except Exception as e:
        _reset()
        return {'ret': False, 'msg': '配置文件丢失或损坏，请尝试重新连接登录！'}

