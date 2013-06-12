#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
For GeekPark
'''
try:
    from bs4 import BeautifulSoup
    import re
    import os
    import sys
    from onepage.publicMethod import to_unicode, errorCatcher
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
    if soup is None:
	return None
    
    title = get_title(soup)
    content = clean_content(get_raw_content(soup))
    return title, content

    
def get_title(soup):
    if soup is None:
        return None
    
    raw_title = soup.find('h1')
    return clean_content(raw_title)

def get_raw_content(soup):
    try:
        if soup is None:
            return None
        
        outter_div = soup.find('div', {'id':'endText'})
        p_list = outter_div.find_all('p',{'class':''})
        if p_list == None or len(p_list) == 0:
            print 'no content'
            return None

        content = ''
        for p in p_list:
            content += str(p)
    except:
        print 'Exception in get_raw_content()'
        return None
    return content
    
