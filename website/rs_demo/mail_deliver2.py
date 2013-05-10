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

def t1():
    t=Title()
    t.text = u'丰哥哥最强壮最英俊'
    t.link = t.origin = 'http://marvin-space.info/blog'
    l1,l2,l3= Label(), Label(), Label()
    l1.text,l2.text, l3.text = u'丰哥哥',u'强壮',u'英俊'
    l1.color = 'dd3355'
    l2.color = '2277aa'
    t.label_list = [l1,l2,l3]
    return t

def t2():
    t=Title()
    t.text=u'全球最富有教授：谷歌第一位投资人'
    t.link = t.origin = 'http://www.cnbeta.com/articles/236709.htm'
    
    l1,l2 = Label(), Label()
    l1.text,l2.text = u'最富',u'谷歌'
    l1.color = u'2277aa'
    t.label_list = [l1,l2]
    return t

def t3():
    t=Title()
    t.text=u'从心理学的角度来聊聊微博和微信'
    t.link = t.origin = 'http://www.cnbeta.com/articles/236719.htm'
    l1 = Label()
    l1.text = u'微信'
    l1.color = '2277aa'
    l2 = Label()
    l2.text = u'微博'
    t.label_list = [l1,l2]
    return t

def t4():
    t=Title()
    t.text=u'创造性人才懂得对别人说不'
    t.link = t.origin = 'http://www.36kr.com/p/203114.html'
    l1 = Label()
    l1.text = u'人才'
    t.label_list = [l1]
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

def fetch_rss(url):
    entries = 'entries'
    rss_source = feedparser.parse(url)
    if (rss_source[entries] is None or
        len(rss_source[entries]) == 0):
        return None
    
    rss_source_title = rss_source['feed']['title']
    article_list = []
    count = 0
    for entity in rss_source[entries]:
        if count > 2:
            break
        
        count+=1
        # md5 the title
        article = Article()
        
        article.title = entity.title
        article.summary = strip_tags(entity.summary)[:80] + '... ...'
        article.link = entity.link
        article.date = entity.published
        article.ref = rss_source_title
        
        article_list.append(article)

    return article_list

def generate_html_mail(list):
    for item in list:
        title, link, summary = item.split('::')
        
    

def get_fulltext(url, summary):
    '''
    TODO:
    '''
    soup = get_html_soup(url)
    

def get_html_soup(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        return soup
    except:
        print 'Exception in get_html()'
        return None
