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
    # Mine
    from publicMethod import to_unicode, clean_content, log_error

    from public_model import Article
    # crawlers
    import crawler_huxiu, crawler_36kr, crawler_geekpark, crawler_163
    
    #    import crawler_36kr
    # http://www.36kr.com/feed

    #    import crawler_geekpark
    
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
Global Varibles
'''
g_link_md5_list = []
g_fileName_rssList = 'static/pubconstant/c_rss_list.txt'
g_fileName_md5list = 'static/pubconstant/md5list_utf8.txt'
g_fileName_result_dir = 'static/res/__.article_raw/'

def start():
    __initial_md5_list()
    for rss in __load_rss_list():
        print '*** *** Now begin to fetch rss %s *** ***' % rss
        fetch_rss(rss)


def fetch_rss(rss_url):
    '''
    获取一个rss地址中的所有内容，包括文章内容
    '''
    
    article_list = __parse_rss(rss_url)
    print ('Fetch Completely! %s' % to_unicode(rss_url))

    print 'ALL DONE'

def __dump(article, fileName):
    '''
    JSON 序列化文档
    '''
    try:
        print '-dump %s' % fileName
        json.dump(article.__dict__, codecs.open(g_fileName_result_dir + fileName + '.json_utf8.txt', 'wb', 'utf-8'))
        print '=dump %s' % fileName
    except ex:
        print ex

def get_html_soup(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        return soup
    except:
        print 'Exception in get_html()'
        return None

def get_content(url):
    soup = get_html_soup(url)
    if soup is None:
        return

    content = __get_raw_content(url, soup)
    return content

def __parse_rss(url):
    entries = 'entries'
    rss_source = feedparser.parse(url)
    rss_source_title = rss_source['feed']['title']
    
    if (rss_source[entries] is None or
        len(rss_source[entries]) == 0):
        return None
    
    article_list = []
    for entity in rss_source[entries]:
        if __is_url_new(entity.link) == False:
            continue
        
        content = get_content(entity.link)
        if content == "":
            continue
        
        article = Article
        article.origin  = rss_source_title
        article.content = content
        article.title   = entity.title
        article.link    = entity.link
        article.summary = entity.summary
        article.date    = entity.published
        
        article = __clean_article(article)
        
        article_list.append(article)
        try:
            print '-dump %s' % article.link
            __dump(article, __generateFileName(article.link))
            print '=dump %s done'
        except:
            print 'ERROR!!!except in dump! %s' % article.link
            continue
        #save(article, generateFileName(article.link))
    return article_list

def __clean_article(article):
    try:
        article.origin  = to_unicode(article.origin)
        article.content = to_unicode(clean_content(article.content))
        article.title   = to_unicode(article.title)
        article.link    = to_unicode(article.link)
        article.summary = to_unicode(clean_content(article.summary))
        article.date    = to_unicode(article.date)
    except:
        print 'error'
        log_error('cleaning')
        return None
    try:
        print '\tafter cleaning:%s' % article.content.encode('utf-8')
    except:
        print 'error'
        log_error('cleaning')        
        
    return article

def __get_raw_content(url, soup):
    print 'get_raw_content:%s' % url
    if 'huxiu.com' in url:
        print 'huxiu!'
        return crawler_huxiu.get_raw_content(soup)

    if '36kr.com' in url:
        print '36kr!'
        return crawler_36kr.get_raw_content(soup)

    if 'geekpark.net' in url:
        print 'geekPark!'
        return crawler_geekpark.get_raw_content(soup)

    if '163.com' or 'rss.feedsportal.com' in url:
        print '163!'
        return crawler_163.get_raw_content(soup)

    print ('No Content Crawler!%s' % url)
    p_list = soup.find_all('p')
    content = ''
    for p in p_list:
        content += str(p)

    return clean_content(content)

        
def __is_url_new(link):
    global g_link_md5_list
    global g_fileName_md5list
    
    m = to_unicode(md5.new(link).hexdigest())

    if m in g_link_md5_list:
        print '\tlink exist'
        return False

    else:
        print('\tnew url:%s' % m)
        g_link_md5_list.append(m)
        f = open(g_fileName_md5list, 'a')
        f.write(m)
        f.write('\n')
        f.flush()
        f.close()
    return True

def __load_rss_list():
    global g_fileName_rssList
    f = open(g_fileName_rssList)
    rss_list = []
    for link in f.readlines():
        rss_list.append(link[:-1])
    return rss_list

def __generateFileName(url):
    name = str(url)
    name = re.sub('http://www.', '', name)
    name = re.sub('.html', '', name)
    name = re.sub('/', '_', name)
    name = re.sub('\.', '_', name)
    name = re.sub('#', '_', name)
    name = re.sub('%', '_', name)
    name = re.sub('-', '_', name)
    return str('%s' % name)


def __initial_md5_list():
    global g_link_md5_list
    global g_fileName_md5list
    f = open(g_fileName_md5list, 'r')
    for link in f.readlines():
        g_link_md5_list.append(to_unicode(link[:-1]))
    f.close()
