# Filename: robot.py
import json
from cmdb.logger import logger
import time

import requests
from werobot import WeRoBot

robot = WeRoBot(token='kuyunhudong')
robot.config['APP_ID'] = 'wxb067c8b8e210e780'
robot.config['APP_SECRET'] = '057c03777f4fac33b71ec23f1d85a1c7'


@robot.text
def hello(message):
    logger.info(message.source)
    send_template(message.source, '2')
    info = robot.client.get_user_info(message.source)
    print(info.headimgurl)
    return 'Hello :%s' % message.source


@robot.error_page
def make_error_page(url):
    return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url


@robot.scan
def scan_code(message):
    send_template(message.source, message.key)
    return ""


def send_template(open_id, key):
    logger.info('send_template')
    headers = {"Content-type": "application/json"}  # application/x-www-form-urlencoded
    url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s' % robot.client.get_access_token()
    params = ({'touser': open_id, 'template_id': 'sCIXkD03qCBGtbiU07Mznfnd3d802jWfDiNBB-TJCUY',
               'data': {'first': {'value': '你好，你已成功绑定设备。'}, 'keyword1': {'value': key},
                        'keyword2': {'value': time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))},
                        'keyword3': {'value': '已绑定'}, 'keyword4': {'value': '1'}, 'remark': {'value': '感谢您的使用。'}}})
    logger.info(json.JSONEncoder().encode(params))
    post = requests.post(url, data=json.JSONEncoder().encode(params))
    logger.info(post.content)


@robot.subscribe
def on_subscribe(message):
    info = json.dumps(robot.client.get_user_info(message.source))
    return 'hello %s' % info['nickname']
