#!/usr/bin/env python
#-*- coding:utf-8 -*-
try:
    from bs4 import BeautifulSoup
    import urllib2		
    import re
    import os
    import sys
    import feedparser
    import codecs
    import json
    import md5
    import time

    # Mine
    from onepage.publicMethod import errorCatcher, to_unicode, clean_html_tags
    import crawler_huxiu, crawler_36kr, crawler_geekpark, crawler_163
    from onepage.models import Article    
except ImportError:
        print >> sys.stderr, """\
There was a problem importing one of the Python modules required.
The error leading to this problem was:

%s

Please install a package which provides this module, or
verify that the module is installed correctly.

It's possible that the above module doesn't match the current version of Python,
which is:
%s
""" % (sys.exc_value, sys.version)
        sys.exit(1)


'''
===Global===
'''
g_fileName_rssList = 'static/pubconstant/c_rss_list.txt'
sys.setdefaultencoding('utf-8')


def start():
    for rss in __load_rss_list():
        print '*** *** Now begin to fetch rss %s *** ***' % rss
        fetch_rss(rss)


def fetch_rss(rss_url):
    rss_url = to_unicode(rss_url)
    '''
    获取一个rss地址中的所有内容，包括文章内容
    ! 返回内容均为unicode 
    '''
    
    article_list = __parse_rss(rss_url)
    print ('Fetch Completely! %s %s' \
           % (rss_url, time.ctime()))

    print 'ALL DONE'


def __parse_rss(url):
    '''
    获取一个rss地址中的所有内容，包括文章内容
    ! 返回内容均为unicode    
    * 出错返回None
    '''

    rss_source = feedparser.parse(url)
    if rss_source is None or\
        rss_source['feed'] is None or\
        rss_source['feed']['title'] is None or\
        rss_source['entries'] is None:
        print 'invalid RSS source %s' % url
        return None


    rss_source_title = rss_source['feed']['title']    
    if (rss_source['entries'] is None or\
        len(rss_source['entries']) == 0):
        return None


    article_list = []
    for entity in rss_source['entries']:
        if __is_url_new(entity.link) == False:
            continue        

        article          = Article()
        article.content  = clean_html_tags(content)
        article.origin   = to_unicode(rss_source_title)
        article.title    = to_unicode(entity.title)
        article.link     = to_unicode(entity.link)
        article.summary  = to_unicode(entity.summary)
        article.pub_time = to_unicode(__parseTime(entity.published))

        article.save()
        article_list.append(article)
        # -for entity
    return article_list


def __parseTime(raw_time):
    '''
    解析发布时间，将其同意化为格式——%Y-%m-%d %H:%M:%S
    '''

    pattern = '.+ '
    m = re.match(pattern, raw_time)
    if m is None:
        return time.strftime('%Y-%m-%d %H:%M:%S')
    try:
        fmt = '%a, %d %b %Y %H:%M:%S'
        t = time.strptime(raw_time, fmt)
        return time.strftime('%Y-%m-%d %H:%M:%S', t)
    except:
        return time.strftime('%Y-%m-%d %H:%M:%S')
        
def __is_url_new(p_link):
    '''
    判断某个链接是否尚未被采集
    '''

    if len(Article.objects.filter(link=to_unicode(p_link))) > 0:
        print 'old link'
        return False
    else:
        print 'new link~'
        return True
    
def __load_rss_list():
    '''
    获取所有RSS源的列表
    '''

    global g_fileName_rssList
    f = open(g_fileName_rssList)
    rss_list = []
    for link in f.readlines():
        rss_list.append(link[:-1])
    return rss_list


def __get_raw_content(url):    
    '''
    获取url对应文章的粗内容(内容格式不确定，并且包含有html标记)
    * 异常返回''
    '''

    try:
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        if soup is None:
            return ''


        content = __get_raw_content_by_crawler(url, soup)
        return content

    except:
        print 'Exception in __get_raw_content()'
        return ''    


def __get_raw_content_by_crawler(url, soup):
    '''
    通过爬虫获取粗内容
    '''

    print 'Crawler is working... :%s' % url
    if 'huxiu.com' in url:
        return crawler_huxiu.get_raw_content(soup)

    if '36kr.com' in url:
        return crawler_36kr.get_raw_content(soup)

    if 'geekpark.net' in url:
        return crawler_geekpark.get_raw_content(soup)

    if '163.com' or 'rss.feedsportal.com' in url:
        return crawler_163.get_raw_content(soup)

    print ('Unknown Url for Crawler %s' % url)
    p_list = soup.find_all('p')
    content = ''
    for p in p_list:
        content += str(p)

    return clean_content(content)
