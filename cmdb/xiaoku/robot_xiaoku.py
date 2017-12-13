# Filename: robot.py
import json
from aip import AipSpeech
from werobot.messages.messages import TextMessage
from cmdb.jpushserver import push_message_by_alias
from cmdb.logger import logger
import time
import requests
from werobot import WeRoBot
from werobot.replies import ArticlesReply, Article

robot = WeRoBot(token='kuyunhudong')
robot.config['APP_ID'] = 'wxb067c8b8e210e780'
robot.config['APP_SECRET'] = '057c03777f4fac33b71ec23f1d85a1c7'
client = robot.client


@robot.error_page
def make_error_page(url):
    return "<h1>喵喵喵 %s 不是给麻瓜访问的快走开</h1>" % url


def reply_guidance(source):
    pass


@robot.subscribe
def on_subscribe(event):
    info = json.dumps(robot.client.get_user_info(event.source))
    return reply_guidance(event.source)


@robot.scan
def on_scan(message):
    push_message_by_alias('guishuai', 'hello world', data_from='data_form')
    return ''


def process_text_message(text, open_id):
    pass


@robot.text
def on_wechat_message(message):
    logger.info('from %s says: %s' % (message.source, message.content))
    return process_text_message(message.content, message.source)


@robot.voice
def on_wechat_sound(message):
    logger.info('from %s says: %s' % (message.recognition, message.content))
    return process_text_message(message.recognition, message.source)
