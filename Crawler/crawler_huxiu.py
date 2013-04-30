#-*- coding:utf-8 -*-

"""
'''
For HuXiu.
'''

try:
    from bs4 import BeautifulSoup
    import urllib2
    import re
    import os
    import sys
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

def get_detail(url):
    '''
    返回文章具体的内容
    '''
    return clean_content(get_raw_content(get_html(url)))


def get_html(url):
    try:
        html = urllib2.urlopen(url).read()
    except:
        print 'Exception in get_html()'
    return html


def get_raw_content(html):
    try:
        soup = BeautifulSoup(html)
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
    return content
