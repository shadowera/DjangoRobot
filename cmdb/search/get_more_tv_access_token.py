import json
import requests
import hashlib

# from flask_restful import abort

MORE_TV_APP_ID = '4bd8920a082ef100a6415b797bfda5bc'
MORE_TV_SECRET = '4d31e381c5b92e3bbf459e23c8059e37'


def generate_md5(src):
    m = hashlib.md5()
    m.update(src.encode('UTF-8'))
    return m.hexdigest()


def get_authorize_code():
    url = 'http://open.moretv.com.cn/authorize?appid=' + MORE_TV_APP_ID
    response = requests.get(url).text
    data = json.loads(response)
    result = ''
    if data['status'] == '200':
        result = data['authorize_code']
        print('authorize_code : ' + result)
    return result


def get_more_tv_access_token():
    authorize_code = get_authorize_code()
    if authorize_code == '':
        # abort(400, message="没有取到access_token".format())
        return ''
    key = MORE_TV_APP_ID + '_' + MORE_TV_SECRET + '_' + authorize_code
    url = 'http://open.moretv.com.cn/get_access_token?authorize_code=' + authorize_code + '&key=' + generate_md5(key)
    response = requests.get(url).text
    data = json.loads(response)
    result = ''
    if data['status'] == '200':
        result = data['access_token']
        print('access_token : ' + result)
    return result
