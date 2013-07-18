#!/usr/bin/env python
#-*- coding:utf-8 -*-
try:
    from bs4 import BeautifulSoup
    import urllib2		
    import re
    import sys
    import feedparser
    import time

    # Mine
    from onepage.models import Article        
    from onepage.publicMethod import errorCatcher, to_unicode, clean_html_tags, setDefaultEncoding
    import crawler_huxiu, crawler_36kr, crawler_geekpark, crawler_163

except ImportError:
        print >> sys.stderr, """\
        ***[fetch_rss]***
Import error in fetch_rss.py
The error leading to this problem was:
*** %s ***
""" % (sys.exc_value)
        sys.exit(1)


'''
===Global===
'''
g_fileName_rssList = 'static/pubconstant/c_rss_list.txt'


def start():
    for rss in __load_rss_source():
        print '*** *** Now begin to fetch rss %s *** ***' % rss
        fetch_rss(rss)


def fetch_rss(rss_url):
    rss_url = to_unicode(rss_url)
    '''
    获取一个rss地址中的所有内容，包括文章内容
    # 返回内容均为unicode 
    '''
    
    article_list = __parse_rss(rss_url)
    print ('Fetch Completely! %s %s' \
           % (rss_url, time.ctime()))

    print 'ALL DONE'

@errorCatcher
def __parse_rss(rss_url):
    '''
    获取一个rss地址中的所有内容，包括文章内容
    # 返回内容均为unicode    
    * 出错返回None
    '''

    # 解析rss基本信息
    rss_source = feedparser.parse(rss_url)
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
        article.content  = __get_content(entity.link)
        article.pub_time = __parseTime(entity.published)
        article.origin   = to_unicode(rss_source_title)
        article.title    = to_unicode(entity.title)
        article.link     = to_unicode(entity.link)
        article.summary  = to_unicode(entity.summary)

        article.save()
        article_list.append(article)
        # -for entity
    return article_list


def __parseTime(raw_time):
    '''
    解析发布时间，将其同意化为格式——%Y-%m-%d %H:%M:%S(unicode)
    '''
    
    try:
        raw_time = re.match('.+ ', raw_time).group[0]
        fmt      = '%a, %d %b %Y %H:%M:%S'
        t        = time.strptime(raw_time, fmt)
        return to_unicode(time.strftime('%Y-%m-%d %H:%M:%S', t))
    except:
        return to_unicode(time.strftime('%Y-%m-%d %H:%M:%S'))

        
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

    
def __load_rss_source():
    '''
    获取所有RSS源的列表
    # list
    '''

    global g_fileName_rssList
    f = open(g_fileName_rssList)
    rss_list = []
    for link in f.readlines():
        rss_list.append(link[:-1])
    return rss_list


def __get_content(url):    
    '''
    获取url对应文章的内容
    # 纯文字(unicode)
    * 异常返回''
    '''

    try:
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        if soup is None:
            return ''
        
        else:
            return clean_html_tags(__get_raw_content_by_crawler(url, soup))

    
    except:
        print 'Exception in __get_raw_content()'
        return ''    


@errorCatcher
def __get_raw_content_by_crawler(url, soup):
    '''
    通过爬虫获取粗内容()
    # 返回content (unicode,但是包含有html标记)
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
