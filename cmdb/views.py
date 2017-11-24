# coding:utf-8
import werobot
from django.shortcuts import render
from django.shortcuts import HttpResponse
from cmdb.robot import robot
from django.core import serializers


# Create your views here.

def index(request):
    return render(request, 'home.html')


def cal(request, a, b):
    c = int(a) + int(b)
    return HttpResponse(str(c))


def get_token(request):
    c = robot.client.get_access_token()
    return HttpResponse(c)
