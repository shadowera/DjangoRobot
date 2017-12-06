from aip import AipSpeech
from cmdb.robot import robot

APP_ID = '10485551'
API_KEY = 'AKZcOwQvhemGLxre8INXtGas'
SECRET_KEY = 'cc1ead9bbcb8278ed6b106fe3fecce4c'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def recognize_voice(media_id):
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (
        robot.client.get_access_token(), media_id)
    aipSpeech.asr('', 'pcm', 16000, {
        'url': url,
        'callback': 'http://xxx.com/receive',
    })
