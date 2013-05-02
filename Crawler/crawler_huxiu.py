#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
For HuXiu.
'''

try:
    from bs4 import BeautifulSoup
    import urllib2
    import re
    import os
    import sys
    import io
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

def start():
    f = open('href_list.txt', 'r')

    index = 0
    for link in f:
	print index
	get_detail(link, 'article/' + str(index) + '.txt')
	index += 1

    print 'ALL DONE!'
def get_detail(url, id):
#    url = 'http://www.huxiu.com/article/13698/1.html'
    soup = get_html_soup(url)
    if soup is None:
	return
    
    title = get_title(soup)
    content = clean_content(get_raw_content(soup))
    result = '%s\n%s\n%s' % (url, title, content)
    write_file(result, id)
    
def get_title(soup):
    raw_title = soup.find('h1')
    return clean_content(raw_title)

def get_html_soup(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        return soup
    except:
        print 'Exception in get_html()'
        return None


def get_raw_content(soup):
    try:
        content = soup.find('', {"id": "article_content"})
    except:
        print 'Exception in get_raw_content()'
    return content


def clean_content(content):
    try:
        content = str(content)
        content = re.sub("<img src=[^>]* alt=\"", "", content)
        content = re.sub("<.+?>", "", content)
        content = re.sub("&quot;", "\"", content)
        content = re.sub("&apos;", "\'", content)
        content = re.sub("&amp;", "&", content)
        content = re.sub("&lt;", "<", content)
        content = re.sub("&gt;", ">", content)
    except:
        print 'Exception in clean_content'
    return str(content)

def write_file(content, fileName='noname.txt'):
    try:
        print "content = %s" % content
        print "fileName = %s" % fileName
        f = open(fileName,'a+')
        f.write(content)
        f.close()
        #with io.open(fileName) as file:
        #    file.write(unicode(str(content)))
    except:
        log_error("error in write_file() \n %s" % str(sys.exc_info()[0]))
    print 'DONE!'

def log_error(content):
    for i in sys.exc_info():
        print str(i)
    print >> sys.stderr, """\
    ERROR: %s
"""% content

start()


