#-*- coding:utf-8 -*-
import feedparser
from bs4 import BeautifulSoup
import urllib2
from django.utils.html import strip_tags
#
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

# mail
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
# test
from django.views.static import * 
from django.conf import settings

# mine
import json
import public_model
import pickle
import test

def refine():
    import article_refiner
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
    f = open('static/res/articles_refine.json_list_utf8.txt', 'rb')
    d = json.JSONDecoder().decode(f.read())
    l = []
    for k,v in d.iteritems():
        l.append(v)
    return l

def show(request):
    '''
    url = 'http://www.huxiu.com/rss/1.xml'
    article_list = fetch_rss(url)
    print (article_list)
    t = get_template('1-lan.html')    
    html = t.render(Context({'article_list': article_list}))
    f = open('static/page.html', 'w')
    f.write(html.encode('utf-8'))
    f.close()
    '''
    f = open('static/page.html')
    html = f.read()
    f.close()

    return HttpResponse(html)
