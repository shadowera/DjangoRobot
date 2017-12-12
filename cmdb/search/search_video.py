# from urllib import request

import json
from urllib.parse import quote, urlencode
import requests
# from flask_restful import abort
import asyncio
import time, threading
from cmdb.search.get_more_tv_access_token import get_more_tv_access_token

VIDEO_FROM_IQIYI = 0
VIDEO_FROM_MORE_TV = 1

FETCH_VIDEO_STATUS_IQIYI = 1
FETCH_VIDEO_STATUS_MORE_TV = 2
FETCH_VIDEO_STATUS_COMPLETE = FETCH_VIDEO_STATUS_IQIYI + FETCH_VIDEO_STATUS_MORE_TV

IQIYI_API_SERVER = 'http://expand.video.iqiyi.com'
IQIYI_API_KEY = '71c300df4a7f4e89a43d8e19e5458e6f'

MORE_TV_API_SERVER = 'http://open.moretv.com.cn/search'
MORE_TV_API_KEY = '71c300df4a7f4e89a43d8e19e5458e6f'

SEARCH_TYPE = [
    'list'
]

FORMAT_FIELDS = {
    'DATA_FORM': 'data_from',
    'TITLE': 'title',
    'THUMB': 'thumb',
    'PIC_URL': 'pic_url',
    'PLAY_URL': 'play_url',
    'H5_PLAY_URL': 'h5_play_url'
}

fetch_data_status = 0
video_data = []
lock = threading.Lock()


class SearchVideo:
    @staticmethod
    def search_video_by_keywords(key_words):
        coroutine_iqiyi = request_video_response_by_keywords(VIDEO_FROM_IQIYI, key_words)
        coroutine_more_tv = request_video_response_by_keywords(VIDEO_FROM_MORE_TV, key_words)
        loop = asyncio.get_event_loop()
        tasks = [
            asyncio.ensure_future(coroutine_iqiyi),
            asyncio.ensure_future(coroutine_more_tv)
        ]
        loop.run_until_complete(asyncio.wait(tasks))
        result = []
        for task in tasks:
            response = task.result()
            temp = json.loads(response.text)
            if IQIYI_API_SERVER in response.url:
                result.extend(filter_iqiyi_fields(temp))
            else:
                result.extend(filter_more_tv_fields(temp))
        try:
            loop.run_forever()
        finally:
            loop.close()
        return result


def search_video_in_thread(video_from, key_word, callback):
    lock.acquire()
    try:
        fetch_video_data(video_from, key_word, callback)
    finally:
        lock.release


def fetch_video_data(video_from, key_word, callback):
    global fetch_data_status
    temp_data = request_video_info_by_keywords(video_from, key_word)
    temp_data = json.loads(temp_data)
    temp_data = filter_fields(video_from, temp_data)
    if video_from == VIDEO_FROM_IQIYI:
        fetch_data_status = fetch_data_status + FETCH_VIDEO_STATUS_IQIYI
    if video_from == VIDEO_FROM_MORE_TV:
        fetch_data_status = fetch_data_status + FETCH_VIDEO_STATUS_MORE_TV
    if fetch_data_status == FETCH_VIDEO_STATUS_COMPLETE:
        return callback(video_data)
    return video_data.extend(temp_data)


def request_video_info_by_keywords(video_from, key_words):
    keywords = quote(key_words)
    if video_from == VIDEO_FROM_IQIYI:
        url = IQIYI_API_SERVER + \
              '/api/search/list.json?type=list&apiKey=' + IQIYI_API_KEY + \
              '&keyWord=' + keywords + '&pageNo=' + '1' + '&pageSize=' + '10'
        response = requests.get(url)
        print('requests.get : ' + response.text)
        ''' 传统urllib的get方式
        with request.urlopen(url) as f:
            data = f.read()
            print('Status:', f.status, f.reason)
            for k, v in f.getheaders():
                print('%s: %s' % (k, v))
            print('Data:', data.decode('utf-8'))
        '''
        return response.text
    else:
        access_token = get_more_tv_access_token()
        if access_token == '':
            return ''
        # abort(400, message="没有取到access_token".format())
        post_data = {
            'access_token': access_token,
            'keyword': quote(keywords),
            'pageIndex': 1,
            'pageSize': 10,
            'contentType': 'movie'
        }
        print('post_data = ', post_data)
        post_data = urlencode(post_data)
        print('url encode post_data = ', post_data)
        url = MORE_TV_API_SERVER
        response = requests.post(url + '?' + post_data)
        print('response = ' + response.text)
        return response.text


async def request_video_response_by_keywords(video_from, key_words):
    keywords = quote(key_words)
    if video_from == VIDEO_FROM_IQIYI:
        url = IQIYI_API_SERVER + \
              '/api/search/list.json?type=list&apiKey=' + IQIYI_API_KEY + \
              '&keyWord=' + keywords + '&pageNo=' + '1' + '&pageSize=' + '10'
        response = requests.get(url)
        print('requests.get : ' + response.text)
        ''' 传统urllib的get方式
        with request.urlopen(url) as f:
            data = f.read()
            print('Status:', f.status, f.reason)
            for k, v in f.getheaders():
                print('%s: %s' % (k, v))
            print('Data:', data.decode('utf-8'))
        '''
        return response
    else:
        access_token = get_more_tv_access_token()
        if access_token == '':
            return ''
            # abort(400, message="没有取到access_token".format())
        post_data = {
            'access_token': access_token,
            'keyword': quote(keywords),
            'pageIndex': 1,
            'pageSize': 10,
            'contentType': 'movie'
        }
        print('post_data = ', post_data)
        post_data = urlencode(post_data)
        print('url encode post_data = ', post_data)
        url = MORE_TV_API_SERVER
        response = requests.post(url + '?' + post_data)
        print('response = ' + response.text)
        return response


def filter_iqiyi_fields(data):
    return filter_fields(VIDEO_FROM_IQIYI, data)


def filter_more_tv_fields(data):
    return filter_fields(VIDEO_FROM_MORE_TV, data)


def filter_fields(video_from, data):
    result = []
    if video_from == VIDEO_FROM_IQIYI:
        for item in data['data']:
            temp = {FORMAT_FIELDS['DATA_FORM']: VIDEO_FROM_IQIYI}
            for key in item:
                if key == 'albumName':
                    temp[FORMAT_FIELDS['TITLE']] = item[key]
                    result.append(temp)
                if key == 'posterPicUrl':
                    temp[FORMAT_FIELDS['THUMB']] = item[key]
                    result.append(temp)
                if key == 'picUrl':
                    temp[FORMAT_FIELDS['PIC_URL']] = item[key]
                    result.append(temp)
                if key == 'playUrl':
                    temp[FORMAT_FIELDS['PLAY_URL']] = item[key]
                    result.append(temp)
                if key == 'html5PlayUrl':
                    temp[FORMAT_FIELDS['H5_PLAY_URL']] = item[key]
            result.append(temp)
    else:
        for item in data['items']:
            temp = {FORMAT_FIELDS['DATA_FORM']: VIDEO_FROM_MORE_TV}
            for key in item:
                if key == 'item_title':
                    temp[FORMAT_FIELDS['TITLE']] = item[key]
                    result.append(temp)
                if key == 'item_icon1':
                    temp[FORMAT_FIELDS['THUMB']] = item[key]
                    result.append(temp)
                if key == 'item_icon1':
                    temp[FORMAT_FIELDS['PIC_URL']] = item[key]
                    result.append(temp)
                if key == 'link_data':
                    temp[FORMAT_FIELDS['PLAY_URL']] = item[key]
                    result.append(temp)
                if key == 'link_data':
                    temp[FORMAT_FIELDS['H5_PLAY_URL']] = item[key]
            result.append(temp)
    return result
