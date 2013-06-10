#-*- coding:utf-8 -*-
import re
import urllib2
from bs4 import BeautifulSoup
import sys
import time
sys.setdefaultencoding('utf-8')

def get_count_from_baidu(words):
    '''
    返回百度新闻上搜索过去24个小时之内的与words有关的新闻数量
    * 查询失败/未果都将返回0
    '''
    span     = 86400 # 24h = 86400s    
    endSec   = int(time.time())
    startSec = endSec - span

    query = ''
    for word in words:
        if query == '':
            query = word
        else:
            query = query + '+' + word
    
    url=u'\
http://news.baidu.com/ns?from=news&\
bt=%d&et=%d&q1=%s' % (startSec, endSec, query)
    """
    AND: q1 = k1 + k2
    OR : q3 = k1 + k2
    """
    print url
    req = urllib2.Request(url, headers= {'User-Agent': 'Mm-Bot'})
    soup = BeautifulSoup(urllib2.urlopen(req).read())

    result_container = soup.find('span', 'nums') # <span class='nums'>
    if result_container is None:
        print "Couldn't find result_div"
        return 0
    
    match = re.search('\d.?\d', result_container.get_text())
    if match is None:
        match = re.search('\d', result_container.get_text())
        if match is None:
            print "Couldn't find match"
            return 0

    count = int(match.group(0).replace(',', ''))
    print '[score] :: %d' % count
    return count

def get_count_from_google(words):
    query = ''
    for word in words:
        if query == '':
            query = word
        else:
            query = query + '+' + word
            
    url = u'\
https://www.google.com.hk/search?tbm=nws&tbs=qdr%%3Ad&gl=hk&\
q=%s' % (query)
    
    print url
    req = urllib2.Request(url, headers= {'User-Agent': 'Mm-Bot'})
    soup = BeautifulSoup(urllib2.urlopen(req).read)

    result_div = soup.find(id='resultStats')
    print result_div
    if result_div is None:
        print "Couldn't find result_div"
        return -1
    
    match = re.search('\d.?\d', result_div.get_text())
    if match is None:
        match = re.search('\d', result_div.get_text())
        if match is None:
            print "Couldn't find match"
            return -1
    

    count = int(match.group(0).replace(',', ''))
    return count
