# Filename: robot.py

from werobot import WeRoBot

robot = WeRoBot(token='guishuai')


@robot.handler
def hello(message):
    return 'Hello World!'
