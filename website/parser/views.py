#-*- coding:utf-8 -*-

from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

# test
from django.views.static import * 
from django.conf import settings

# mine
import time
import json
import article_refiner

g_ARTICLES_DIR = 'static/res/showcase/'#articles_refine.json_list_utf8.txt'
#fileName = g_ARTICLES_DIR + time.strftime('%m-%d') + '.json-utf8.txt'


def refine(request):
    article_refiner.refine()
    return HttpResponse('Refined !')

def build(request):
    t = get_template('1-lan.html')
    article_list = __load_articles()

    html = t.render(Context({'article_list': article_list}))    
    f = open('static/page.html', 'w')
    f.write(html.encode('utf-8'))
    f.close()
    return HttpResponse(html)

def __load_articles():
    global g_ARTICLES_DIR
    fileName = g_ARTICLES_DIR + time.strftime('%m-%d') + '.json-utf8.txt'    
    f = open(fileName, 'rb')
    d = json.JSONDecoder().decode(f.read())
    l = []
    for k,v in d.iteritems():
        l.append(v)
    return l

