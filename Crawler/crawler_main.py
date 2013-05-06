#!/usr/bin/env python
#-*- coding:utf-8 -*-


try:
    from bs4 import BeautifulSoup
    import urllib2		
    import re
    import os
    import sys

    # Mine
    import publicMethod
    # crawlers
    import crawler_huxiu
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

def get_html_soup(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        return soup
    except:
        print 'Exception in get_html()'
        return None

def fetch(url):
    if isUrlNew(url) is not True:
        return
    
    soup = get_html_soup(url)
    if soup is None:
        return

    title, content = get_info(url, soup)
    towrite = '%s\n%s' % (title, content)
    
    publicMethod.write_file_utf8(towrite, generateFileName(url))

def get_info(url, soup):
    if 'huxiu.com' in url:
        return crawler_huxiu.get_info(soup)
    
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
    return str(name + '.txt')
    
fetch('http://www.huxiu.com/article/14099/1.html')
