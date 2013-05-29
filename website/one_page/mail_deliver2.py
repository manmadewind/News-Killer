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

class Article:
    title = ""
    ref = ""
    link = ""
    summary = ""
    date = ""
class Label:
    color = "2299aa"
    text = "label"
    
    def set_color(self, type=3):
        if type == 3:
            self.color = '2299aa'
        elif type == 2:
            self.color = '2277aa'
        elif type == 1:
            self.color = 'dd3355'
        else:
            self.color = '2277aa'
            
class Title:
    label_list = []
    link = ""
    origin = ""
    text = ""
    
class Container:
    article_list = []
    title_list = []

    # --- --- ---
    
def send_html_mail(subject, content, list):
    mail = EmailMultiAlternatives(subject, strip_tags(content), 'manmadewind@gmail.com', list)
    mail.attach_alternative(content, "text/html")
    mail.send()

def get_title():
    t = Title()
    t.link = 'marvin-space.info/blog'
    t.origin = 'marvin-space.info/blog'
    t.text = 'Hello World'
    l1 = Label()
    l2 = Label()
    t.label_list = [l1,l2]
    return t

def t5():
    t=Title()
    t.text=u'移动互联网成各行业标配手段？迪斯尼推出相册应用St...'
    t.link = t.origin = 'http://www.36kr.com/p/203116.html'
    l1,l2 = Label(), Label()
    l1.text,l2.text = u'互联网',u'迪斯尼'
    l1.color = '2277aa'
    t.label_list = [l1,l2]
    return t

def deliver(request):
    container = dict()
    
    url = 'http://www.huxiu.com/rss/1.xml'
    article_list = fetch_rss(url)
    container['article_list'] = article_list    
    
    title = get_title()
    title2 = get_title()
    title_list = [title, title2]
    container['title_list'] = [t1(), t2(), t3(), t4(), t5(), t2(), t3(), t4(), t5(), t2(), t3(), t4(), t5(), t2(), t3(), t4(), t5()]
    
    t = get_template('mail2.html')    
    html = t.render(Context({'container': container}))
    #html = t.render(Context({'article_list': list}))
    #mail_list = ['350424185@qq.com','125984678@qq.com','1346869@qq.com']
    mail_list = ['manmadewind@gmail.com','zhuayuba@hotmail.com']
    #mail_list = ['1346869@qq.com','manmadewind@gmail.com']
    #send_html_mail('(BETA)Secret Mail from Brother FENG!', html, mail_list)
    
    return HttpResponse(html)
