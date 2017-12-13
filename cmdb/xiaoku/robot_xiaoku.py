# Filename: robot.py
from aip import AipSpeech
from werobot.messages.messages import TextMessage
from cmdb.jpushserver import push_message_by_alias
from cmdb.logger import logger
from cmdb.search.search_video import request_video_response_by_keywords, request_video_info_by_keywords, \
    VIDEO_FROM_IQIYI, filter_iqiyi_fields, FORMAT_FIELDS
import time
import requests
from werobot import WeRoBot
import json

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
    return '正在绑定 %s' % message.key


@robot.click
def on_click(event):
    pass


def process_text_message(text, message):
    search = request_video_info_by_keywords(VIDEO_FROM_IQIYI, text)
    json_str = json.loads(search)
    result = filter_iqiyi_fields(json_str)
    reply = ArticlesReply(message=message)
    i = 0
    for data in result:
        if i >= 8:
            break
        article = Article(
            title=data[FORMAT_FIELDS['TITLE']],
            img=data[FORMAT_FIELDS['PIC_URL']],
            url=data[FORMAT_FIELDS['PLAY_URL']]
        )
        reply.add_article(article)
        i = i + 1
    return reply


@robot.text
def on_wechat_message(message):
    logger.info('from %s says: %s' % (message.source, message.content))
    return process_text_message(message.content, message)


@robot.voice
def on_wechat_sound(message):
    logger.info('from %s says: %s' % (message.recognition, message.content))
    return process_text_message(message.recognition, message)


def make_article(result, message):
    reply = ArticlesReply(message=message)
    if not isinstance(result, (list, tuple)):
        return ''
    elif len(result) <= 0:
        return ''
