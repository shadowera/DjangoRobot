# Filename: robot.py

from werobot import WeRoBot

robot = WeRoBot(token='guishuai')
robot.config['APP_ID'] = 'wx860aedabf993a256'
robot.config['APP_SECRET'] = '05e69d96a6953f2cd4840fc1a1c073be'


@robot.handler
def hello(message):
    return 'Hello World!'


@robot.error_page
def make_error_page(url):
    return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url
