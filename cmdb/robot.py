# Filename: robot.py

from werobot import WeRoBot

robot = WeRoBot(token='guishuai')
robot.config['APP_ID'] = 'wxe31287e98a274894'
robot.config['APP_SECRET'] = '3d8b928b3263ad3fc88e497a5f494abc'


@robot.handler
def hello(message):
    return 'Hello World!'


@robot.error_page
def make_error_page(url):
    return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url
