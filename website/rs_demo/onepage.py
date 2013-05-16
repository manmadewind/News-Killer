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
# from public_model import Article, Label
import public_model
import codecs
import pickle

def refine(request):
    t = get_template('1-lan.html')    
    article_list = __load_articles()
    html = t.render(Context({'article_list': article_list}))    
    f = open('static/page.html', 'w')
    f.write(html.encode('utf-8'))
    f.close()
    return HttpResponse(html)

def __load_articles():
    
    f = open('static/res/articles_refine.list', 'rb')
    return pickle.load(f)

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

'''

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
        if count > 10:
            break
        
        count+=1
        # md5 the title
        article = Article()
        
        article.title     = entity.title
        article.summary   = strip_tags(entity.summary)[:80] + '... ...'
        article.summaryid = count
        article.link      = entity.link
        article.date      = entity.published
        article.origin    = rss_source_title
        
        for i in range(2):
            l = Label()
            l.text = article.title[i*2:i*2+2]
            article.label_list.append(l)
            
        article_list.append(article)

    return article_list

def generate_html_mail(list):
    for item in list:
        title, link, summary = item.split('::')
        
    

def get_fulltext(url, summary):
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
'''
