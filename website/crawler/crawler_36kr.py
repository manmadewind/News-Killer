#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
For 36Kr
'''
try:
    from bs4 import BeautifulSoup
    import re
    import os
    import sys
    from onepage.publicMethod import to_unicode, errorCatcher
except ImportError:
        print >> sys.stderr, """\
[ERROR:Crawler_36kr]
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

@errorCatcher	
def get_raw_content(soup):
    try:
        if soup is None:
            return None
        
        div = soup.find('div', {'class':'mainContent sep-10'})
        p_list = div.find_all('p')
        if p_list == None or len(p_list) == 0:
            return None

        content = ''
        for p in p_list:
            content += str(p)
    except:
        print 'Exception in get_raw_content()'
        return None
    return content
    
