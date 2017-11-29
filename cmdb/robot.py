# Filename: robot.py
import json

from werobot import WeRoBot

robot = WeRoBot(token='kuyunhudong')
robot.config['APP_ID'] = 'wxb067c8b8e210e780'
robot.config['APP_SECRET'] = '057c03777f4fac33b71ec23f1d85a1c7'


@robot.text
def hello(message):
    return 'Hello World!'


@robot.error_page
def make_error_page(url):
    return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url


@robot.scan
def scan_code(message):
    return "mac 是 %s" % message.key


@robot.subscribe
def on_subscribe(message):
    info = json.dumps(robot.client.get_user_info(message.source))
    return 'hello %s' % info['nickname']
