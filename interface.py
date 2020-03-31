from __init__ import ConfigPath


conf = "{'device_id': ''}"


# 写文件
def _write(path, arg):
    fp = open(path, 'w', encoding='utf-8')
    fp.write(arg)
    fp.close()

# 读文件
def _read(path):
    file = open(path, 'r', encoding='utf-8')
    content = file.read()
    file.close()
    return content


"""写入配置文件 device_id"""


def _reset(data):
    with open(ConfigPath, 'r+') as f:
        config_dic = eval(f.read())
        config_dic['device_id'] = data
        f.seek(0)
        f.truncate()
        f.write(str(config_dic))


"""重置配置文件"""


def reset_config():
    try:
        _reset('')
    except Exception as e:
        _write(ConfigPath, conf)


"""写入设备号"""


def save_device(device_id):
    try:
        _reset(device_id)
        return {'ret': True, 'msg': ''}
    except Exception as e:
        _write(ConfigPath, conf)
        return {'ret': False, 'msg': '配置文件丢失或损坏，请重试！'}


"""读取设备号"""


def load_config():
    try:
        with open(ConfigPath, 'r') as f:
            config_dic = eval(f.read())
            device_id = config_dic['device_id']
            return {'ret': True, 'msg': device_id}
    except Exception as e:
        _write(ConfigPath, conf)
        return {'ret': False, 'msg': '配置文件丢失或损坏，请尝试重新连接登录！'}

