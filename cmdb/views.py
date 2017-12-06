# coding:utf-8
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import HttpResponse
from django.shortcuts import render

from cmdb.robot import robot


# Create your views here.

def index(request):
    return render(request, 'home.html')


def cal(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def get_token(request):
    data = {'token': robot.client.get_access_token()}
    return HttpResponse(json.dumps(data))


@csrf_exempt
def recognize_voice(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body)
        print(received_json_data)
    else:
        print('abc')
    return HttpResponse('')
