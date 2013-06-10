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
    # Mine
    import publicMethod
    from publicMethod import to_unicode, clean_content
    import cPickle
    # crawlers
    import crawler_huxiu
    
    import crawler_36kr
    # http://www.36kr.com/feed
    
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


class Article:
    title   = ""
    ref     = ""
    link    = ""
    summary = ""
    content = ""
    date    = ""


def dump(model, fileName):
    print '-dump %s' % fileName
    cPickle.dump(model, codecs.open(fileName, 'wb', 'utf-8'))
    #cPickle.dump(model, open(fileName, 'wb'))
    print '=dump %s' % fileName

def load(fileName):
    print 'new'
    return cPickle.load(open(fileName, 'rb'))

    
def fetch_rss(rss_url):
    article_list = parse_rss(rss_url)
    print 'fetch done'
    
    for article in article_list:
        try:
            print '-dump %s' % article.link
            dump(article, generateFileName(article.link))
        #dump(article)
            print '=dump %s done'
        except:
            print 'except in dump! %s' % article.link
            continue
    print 'all done!'

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
    if isUrlNew(url) is not True:
        return
    
    soup = get_html_soup(url)
    if soup is None:
        return

    content = get_raw_content(url, soup)
    return content

def parse_rss(url):
    entries = 'entries'
    rss_source = feedparser.parse(url)
    rss_source_title = rss_source['feed']['title']
    
    if (rss_source[entries] is None or
        len(rss_source[entries]) == 0):
        return None
    
    article_list = []
    for entity in rss_source[entries]:
        content = get_content(entity.link)
        if content == "":
            continue
        
        article = Article()
        article.ref     = rss_source_title
        article.content = content
        article.title   = entity.title
        article.link    = entity.link
        article.summary = entity.summary
        article.date    = entity.published
        
        article = clean_article(article)
        article_list.append(article)
    return article_list

def clean_article(article):
    article.ref     = to_unicode(article.ref)
    article.content = to_unicode(clean_content(article.content))
    article.title   = to_unicode(article.title)
    article.link    = to_unicode(article.link)
    article.summary = to_unicode(clean_content(article.summary))
    article.date    = to_unicode(article.date)
    return article

def get_raw_content(url, soup):
    if 'huxiu.com' in url:
        return crawler_huxiu.get_raw_content(soup)

    if '36kr.com' in url:
        return crawler_36kr.get_raw_content(soup)
    
    return None
        
def isUrlNew(url):
    #TODO:
    return True

def generateFileName(url):
    name = str(url)
    name = re.sub('http://www.', '', name)
    name = re.sub('.html', '', name)
    name = re.sub('/', '_', name)
    name = re.sub('\.', '_', name)
    name = re.sub('#', '_', name)
    name = re.sub('%', '_', name)
    name = re.sub('-', '_', name)
    return str('article/%s.txt' % name)

#rss_url = 'http://www.huxiu.com/rss/1.xml'
#rss_url = 'http://www.36kr.com/feed'
#a_url = 'http://www.huxiu.com/article/14099/1.html'
#fetch_rss(rss_url)