# Filename: robot.py
import json
from aip import AipSpeech
from cmdb.logger import logger
import time
import requests
from werobot import WeRoBot

robot = WeRoBot(token='kuyunhudong')
robot.config['APP_ID'] = 'wxb067c8b8e210e780'
robot.config['APP_SECRET'] = '057c03777f4fac33b71ec23f1d85a1c7'

APP_ID = '10485551'
API_KEY = 'AKZcOwQvhemGLxre8INXtGas'
SECRET_KEY = 'cc1ead9bbcb8278ed6b106fe3fecce4c'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def download(url):
    r = requests.get(url, stream=True)
    with open("python.pdf", "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                pdf.write(chunk)


def get_file_content(filePath):
    with open('python.pdf', 'rb') as fp:
        return fp.read()


def recognize_voice(media_id, cuid):
    print('recognize voice ....')
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (
        robot.client.get_access_token(), media_id)
    print(url)
    aipSpeech.asr('', 'amr', 8000, {
        'url': url,
        'cuid': cuid,
        'callback': 'http://18.217.19.97/recognize/',
    })


def recognize_sound(media_id):
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (
        robot.client.get_access_token(), media_id)
    download(url)
    return aipSpeech.asr(get_file_content('python.pdf'), 'amr', 8000, {
        'lan': 'zh',
    })


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


@robot.handler
def on_wechat_message(message):
    print('type=%s' % message.type)
    if message.type == 'voice':
        return recognize_sound(message.media_id)

    if message.type == 'text':
        logger.info(message.source)
        send_template(message.source, '2')
        info = robot.client.get_user_info(message.source)
        for n, m in info.items():
            print('name=%s ,value=%s' % (n, m))
        return 'Hello :%s' % message.source
