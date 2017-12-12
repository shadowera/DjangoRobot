import requests
from aip import AipSpeech

from cmdb.robot import robot

APP_ID = '10485551'
API_KEY = 'AKZcOwQvhemGLxre8INXtGas'
SECRET_KEY = 'cc1ead9bbcb8278ed6b106fe3fecce4c'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)


def get_media_path(media_id):
    return 'wechat_sound//%s' % media_id


def download(url, path):
    r = requests.get(url, stream=True)
    with open(path, "wb") as pdf:
        for chunk in r.iter_content(chunk_size=1024 * 8):
            if chunk:
                pdf.write(chunk)


def get_file_content(path):
    with open(path, 'rb') as fp:
        return fp.read()


def recognize_sound(media_id):
    url = 'http://file.api.weixin.qq.com/cgi-bin/media/get?access_token=%s&media_id=%s' % (
        robot.client.get_access_token(), media_id)
    path = get_media_path(media_id)
    download(url, path)
    result = aipSpeech.asr(get_file_content(path), 'amr', 8000, {'lan': 'zh', })
    print(result)
    if result['err_no'] == 0:
        return result['result'][0]
    else:
        print(result['err_msg'])
        return '你说啥？'
