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
from onepage.models import User
import page

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


def deliver(request):
    url = 'http://www.huxiu.com/rss/1.xml'
    #list = fetch_rss(url)
    list = []
    t = get_template('mail.html')
    html = t.render(Context({'article_list': list}))
    return HttpResponse(html)

def build(request):
    html = page.build()
    return HttpResponse(html)

def show(request):
    html = page.show()
    return HttpResponse(html)

def automake(request):
    html = page.automake()
    return HttpResponse('AutoMakeDone.')
