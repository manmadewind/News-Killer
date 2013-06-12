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

# mime
import codecs
import json
import public_model

def __get_source():
    article_list = __load_articles()
    article_list = __filter(article_list)

    for article in article_list:
        for text,t in article['label_dict'].iteritems():
            article['label_dict'][text] = __get_color(t)
    return article_list

def __load_articles():
    f = open('static/res/articles_refine.json_list_utf8.txt', 'rb')
    d = json.JSONDecoder().decode(f.read())
    l = []
    for k,v in d.iteritems():
        l.append(v)
    return l

def __filter(article_list):
    return article_list
    
def __send_html_mail(subject, content, list):
    mail = EmailMultiAlternatives(subject, strip_tags(content), 'manmadewind@gmail.com', list)
    mail.attach_alternative(content, "text/html")
    mail.send()

def __get_color(t):
    if t == "l_1":
        return "#f79"
    
    elif t == "l_2":
        return "#591"
    
    else:
        return "#269"

def generate_mail(request):
    container = dict()

    article_list = __get_source()
    
    t = get_template('mail3.html')
    html = t.render(Context({'article_list': article_list}))
    f = codecs.open('static/res/dailymail.html', 'w','utf-8')
    f.write(html)
    f.flush()
    f.close()
    return HttpResponse(html)

def deliver(request):
    '''
    container = dict()
    article_list = __get_source()
    
    
    t = get_template('mail3.html')
    html = t.render(Context({'article_list': article_list}))
    '''
    f = codecs.open('static/res/dailymail.html', 'r', 'utf-8')
    html = f.read()
    #mail_list = ['manmadewind@gmail.com','1346869@qq.com']

    mail_list = [\
    'zhuayuba@hotmail.com',\
    '350424185@qq.com',\
    '125984678@qq.com',\
    'yunjiaojiao@hotmail.com',\
    '8243215@qq.com',\
    '1346869@qq.com']

    #mail_list = ['manmadewind@gmail.com','zhuayuba@hotmail.com', '1346869@qq.com']
    #mail_list = ['1346869@qq.com','manmadewind@gmail.com']
    __send_html_mail('(BETA)NEWS_2 from 1-lan!', html, mail_list)
    
    return HttpResponse(html)
