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

# Mine
from publicMethod import errorCatcher, to_unicode
import userManager

def regist_form(request):
    t = get_template('regist_form.html')
    html = t.render(Context({"",""}))
    return HttpResponse(html)

"""
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
        user.email       = mail             # email
        user.psw         = sha.hexdigest()  # sha-1 
        user.pushmail    = pushmail         # 0-false; 1-true
        user.regist_date = datetime.now()
        
        user.hit_count     = 0
        user.origin_count  = 0
        user.like_count    = 0
        user.dislike_count = 0

        user.save()
        return HttpResponse("DONE!")
    
    return redirect('')
"""
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


# about user

@errorCatcher
def regist(request):
    print request.POST.keys()
    if request.POST.has_key('email') == False or \
        request.POST.has_key('psw') == False:
        info = 'regist failed: Missed some fields'
        print info
        return HttpResponse(info)


    u_email = to_unicode(request.POST['email'])
    print 'email:' + u_email # test
    
    if userManager.isMailExist(u_email) == True:
        info = 'Email is already exist.'
        print info
        return HttpResponse(info)
    print 'new email'

    u_psw = userManager.encryption(to_unicode(request.POST['psw']))
    print 'get key'
    user  = userManager.regist(u_email, u_psw, True)
    if user is None:
        info = 'unknown reason...'
        print info
        return HttpResponse(info)
    
    info = 'Congradulation!'
    print info
    request.session['uid'] = to_unicode(u.uid)    
    return HttpResponse(info)

    
@errorCatcher
def signin(request):
    u_email = to_unicode(request.POST['email'])
    u_psw   = userManager.encryption(to_unicode(request.POST['psw']))

    u = userManager.signin(u_email, u_psw)
    if u is None:
        info = 'Sign in failed'
        print info
        return HttpResponse(info)
    
    else:
        info = 'welcome back :) '
        print info
        return HttpResponse(info)


@errorCatcher
def logout(request):
    userManager.logout()
    return HttpResponse('loged out.')

@errorCatcher
def set_preference(request):
    uid = userManager.getUidInSession()
    if uid == -1:
        info = 'Does not sign in, no uid in session'
        print info
        return HttpResponse(info)

    if request.POST.has_key('aid') == False:
        info = 'aid not in session'
        print info
        return HttpResponse(info)
    
    aid = to_unicode(request.POST['aid'])
    userManager.set_preference(uid, aid)
    info = 'preference done.'
    print info
    return HttpResponse(info)
    
    
# test below:

def set(request):
    uid = request.session.get('uid', -1)
    if uid != -1:
        page.set_preference(uid,2)
    else:
        print 'uid = -1...'
    return HttpResponse(uid)

def testbtn(request):
    print 'get request ~~ '
    if request.POST.has_key('message') == False:
        print 'doesnot contain [message]'

    request.session['uid'] = 99

    print 'got message!'
    print str(request.POST['message'])
    return HttpResponse('get request~');


def testshow(request):
    html = get_template('1-lan.html').render(Context({'article_list': None}))
    return HttpResponse(html)

