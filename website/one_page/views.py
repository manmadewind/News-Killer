#-*- coding:utf-8 -*-
import hashlib
from datetime import datetime
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import redirect

from django.core.mail import send_mail
# for HTML mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string


# template
from django.template import Template, Context
from django.template.loader import get_template
# other
import feedparser
from bs4 import BeautifulSoup
import urllib2

#models
from one_page.models import User

def regist_form(request):
    t = get_template('regist_form.html')
    html = t.render(Context({"",""}))
    return HttpResponse(html)

def regist(request):
    if request.method == 'POST':
        mail    = request.POST['mail']
        psw_raw = request.POST['psw']
        if request.POST.get('pushmail', ''):
            pushmail = True
        else:
            pushmail = False
    
        sha = hashlib.sha1()
        sha.update(str(psw_raw))
        
        user             = User()
        user.email       = mail              # email
        user.psw         = sha.hexdigest()     # sha-1 
        user.pushmail    = pushmail       # 0-false; 1-true
        user.regist_date = datetime.now()
        
        user.hit_count     = 0
        user.origin_count  = 0
        user.like_count    = 0
        user.dislike_count = 0

        user.save()
        return HttpResponse("DONE!")
    
    return redirect('')

'''

'''
def sendmail(title, content, list):
    r = send_mail(title, content, 'manmadewind@gmail.com', list, fail_silently = False)
    if r == 1:
        print 'Send mail successful!'
    else :
        print 'Send mail failed.'

def send_html_mail(subject, content, list):
    mail = EmailMultiAlternatives(subject, strip_tags(content), 'manmadewind@gmail.com', list)
    mail.attach_alternative(content, "text/html")
    mail.send()

def generateCSSmail():
    content = '\
    <div>\
    <style type="text/css">\
    <h2>Mail Deliver!</h2>\
    <p style="color:#f11">I am supposed to be RED:)</p>\
    </div>\
    '
    '''
class article:
    title = "t"
    ref  = "r"
    link = "l"
    summary = "s"
    
def testmail(request):
    t = get_template('mail.html')
    a1 = article()
    a1.title = "HELLO!"
    list = [a1]
    html = t.render(Context({'article_list': list}))
    return HttpResponse(html)
    
'''
class Article:
    title = ""
    ref = ""
    link = ""
    summary = ""
    date = ""

def deliver(request):
    url = 'http://www.huxiu.com/rss/1.xml'
    list = fetch_rss(url)
    t = get_template('mail.html')
    html = t.render(Context({'article_list': list}))
    return HttpResponse(html)

def fetch_rss(url):
    entries = 'entries'
    rss_source = feedparser.parse(url)
    if (rss_source[entries] is None or
        len(rss_source[entries]) == 0):
        return None
    
    rss_source_title = rss_source['feed']['title']
    article_list = []
    for entity in rss_source[entries]:
        # md5 the title
        article = Article()
        
        article.title = entity.title
        article.summary = entity.summary
        article.link = entity.link
        article.date = entity.published
        article.ref = rss_source_title
        
        article_list.append(article)

    return article_list

def get_html_soup(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        return soup
    except:
        print 'Exception in get_html()'
        return None
