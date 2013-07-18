#-*- coding:utf-8 -*-

import time
import datetime
import ast

# django
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template
from django.views.static import * 
from django.conf import settings

# mine
from onepage.models import Article, Behavior
from crawler.fetch_rss import start
from parser.article_refiner import refine
from publicMethod import errorCatcher
#from sae_memop import save as savemem, loadmem
from fsop import save, load

@errorCatcher
def automake():
    print '*** auto make *** %s' % time.ctime()
    start()
    print '[auto]1/3 Crawler Done.'
    
    refine()
    print '[auto]2/3 Refine Done.'
    
    html = build()
    print '[auto]3/3 Build Done.'
    
    return html

@errorCatcher
def build():
    article_list = generateContent()
    # generate page content
    html = get_template('1-lan.html').render(Context({'article_list': article_list}))

    # save page into memcached
    save('1lan.html', html)
    return html

@errorCatcher
def generateContent():
    '''
    生成具体的内容
    '''
    article_list = __load_articles_today()
    for article in article_list:
        try:
            article.mm_labels = ast.literal_eval(article.mm_labels) #from string to dict
        except Exception as e:
            print 'error in build()'
            print e
            print article.mm_labels
            article.mm_labels = None
            
    return article_list

@errorCatcher
def __load_articles_today():
    '''
    从数据库里取出当天的文章
    '''
    today = datetime.date.today()
    return Article.objects.filter(\
                                  create_date__year  = today.year,\
                                  create_date__month = today.month,\
                                  create_date__day   = today.day).order_by('-mm_score')


@errorCatcher
def show_login(uid):
    template = Template(show())
    context = Context({
        'uid': uid
    })
    
    html = template.render(context)
    return html


@errorCatcher
def dynamicShow(uid):
    
    article_list = generateContent()
    t = get_template('1-lan.html')
    c = Context({
        'article_list': article_list,
        'uid': uid
    })
    html = get_template('1-lan.html').render(c)
    return html
    

@errorCatcher
def show():
    '''
    显示已经build好的html页
    '''
    html = load('1lan.html')
    if html is None:
        html = automake()


    #test
    article_list = generateContent()
    t = get_template('1-lan.html')
    c = Context({
        'article_list': article_list,
        'uid': -1
    })
    html = t.render(c)
    return html
        # ---
    template = get_template('1-lan.html')
    a_list = load('article_list')
    context = Context({
        article_list: a_list,
        'uid': -1
    })
    print 'uid-1;'
    html = template.render(context)
    return html


# --- 行为交互部分 ---

@errorCatcher
def isLogined():
    '''
    判断用户是否已经登陆
    '''
    if 'uid' in request.session == True:
        return True
    else:
        return False

@errorCatcher
def getUidInSession():
    '''
    返回存于session中的uid,如果不存在则返回-1
    '''
    return request.session.get('uid', -1)

@errorCatcher
def set_preference(p_uid, p_aid):
    print 'New behavior:'
    bh         = Behavior()
    bh.aid     = p_aid
    bh.uid     = p_uid
    bh.op      = 1
    bh.op_time = time.strftime('%Y-%m-%d %H:%M:%S')
    bh.save()
    print bh
    return bh.op
    
