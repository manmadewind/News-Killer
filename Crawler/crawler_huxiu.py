#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
For HuXiu.
'''
try:
    from bs4 import BeautifulSoup
    import re
    import os
    import sys
    from publicMethod import write_file_utf8, log_error, to_unicode, clean_content
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
	
def get_info(soup):
    # url = 'http://www.huxiu.com/article/13698/1.html'
    if soup is None:
	return
    
    title = get_title(soup)
    content = clean_content(get_raw_content(soup))
    return title, content

    
def get_title(soup):
    raw_title = soup.find('h1')
    return clean_content(raw_title)

def get_raw_content(soup):
    try:
        content = soup.find('', {"id": "article_content"})
    except:
        print 'Exception in get_raw_content()'
    return content
