#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
For HuXiu List.
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
g_list = []

def start():
    global g_list
    count = 0
    index = 0
    g_list.append('http://www.huxiu.com/focus/')

    while count < 400:
        print 'in while, count = %d, index = %d' %(count, index)
        get_list(g_list[index])
        index += 1
	count = 0
	for list in g_list:
		if 'article' in list:
			count += 1

    results = []
    for list in g_list:
	    if 'article' in list:
		    results.append(list)
    write_list(results)

def get_list(url):
    '''
    返回文章具体的内容
    '''
    
    return get_href_list(get_html(url))


def get_html(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        print "url = %s Read " % url
        return html_content
    except:
        print 'Exception in get_html()'
        return ""

def get_href_list(html_content):
    global g_list
    try:
        print 'begin to get href list'
        soup = BeautifulSoup(html_content)
        raw_href_list = soup.find_all('a')
        print 'soup done len = %d' % len(raw_href_list)
        
        for raw_href in raw_href_list:
            if raw_href['href'] is None:
                continue

            if raw_href['href'][: 4] != "http":
                link = "http://www.huxiu.com/" + str(raw_href['href'])
            else:
                link = str(raw_href['href'])
            if link not in g_list:
                g_list.append(link)
                print link
    except:
        log_error("error in get_href_list()")
                

def write_list(results, fileName='href_list.txt'):
    try:
        print "fileName = %s" % fileName
        f = open(fileName,'a+')
	#f.writelines(results)
        for link in results:
            f.write(link + "\n")

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


