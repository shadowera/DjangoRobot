# Filename: robot.py
import json

import time

import requests
from werobot import WeRoBot

robot = WeRoBot(token='kuyunhudong')
robot.config['APP_ID'] = 'wxb067c8b8e210e780'
robot.config['APP_SECRET'] = '057c03777f4fac33b71ec23f1d85a1c7'


@robot.text
def hello(message):
    send_template('1', '2')
    return 'Hello World!'


@robot.error_page
def make_error_page(url):
    return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url


@robot.scan
def scan_code(message):
    return ""


def send_template(open_id, key):
    headers = {"Content-type": "application/json"}  # application/x-www-form-urlencoded
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % robot.client.get_access_token()
    params = ({'touser': open_id,
               'template_id': 'sCIXkD03qCBGtbiU07Mznfnd3d802jWfDiNBB-TJCUY',
               'data': {
                   'first': {'value': '你好，你已成功绑定设备。'},
                   'keyword1': {'value': key},
                   'keyword2': {'value': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))},
                   'keyword3': {'value': '已绑定'},
                   'keyword4': {'value': '1'},
                   'remark': {'value': '感谢您的使用。'}}})
    requests.post(url, json=json.JSONEncoder().encode(params))


@robot.subscribe
def on_subscribe(message):
    info = json.dumps(robot.client.get_user_info(message.source))
    return 'hello %s' % info['nickname']
