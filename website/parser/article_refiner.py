#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import codecs
import time
from label_generator import get_labels_jieba as get_labels
from public_model import Article


# global variables
g_RAW_ARTICLE_DIR = 'static/res/__.article_raw/'
g_ARTICLES_DIR = 'static/res/showcase/'
#fileName = g_ARTICLES_DIR + time.strftime('%m-%d') + '.json-utf8.txt'

def refine():
    '''
    return a list of parsed articles
    '''
    global g_ARTICLES_DIR
    
    raw_article_list = __load_article_raw()
    final_dict = dict()
    count = 0
    for raw_article in raw_article_list:
        article = Article()
        article.fromjson(raw_article)
        
        article.label_dict = get_labels(article.title, article.summary)
        article.summaryid = count
      
        final_dict[count] = article.__dict__
        count += 1

    fileName = g_ARTICLES_DIR + time.strftime('%m-%d') + '.json-utf8.txt'
    __dumpDict(final_dict, fileName)
    return final_dict


def __load_article_raw():
    '''
    取得爬虫采集的文章集合(只获取当天的)
    '''
    global g_RAW_ARTICLE_DIR
    path = g_RAW_ARTICLE_DIR

    raw_article_list = []
    todayDate = time.strftime('%m-%d')
    
    for f in os.listdir(path):
        if f[0] == '.': # jump hidden file
            continue
        fullName = path + f

        creationDate = time.strftime('%m-%d', time.gmtime(os.path.getmtime(fullName)))

        if todayDate != creationDate:
            continue
        
        raw_article_list.append(__loadJsonFile(fullName))
    print ('raw article list = %d' % len(raw_article_list))
    return raw_article_list


def __dumpDict(d, fileName):
    print '-dump %s' % fileName
    json.dump(d, codecs.open(fileName, 'w+b', 'utf-8'))
    print '=dump %s' % fileName

def __loadJsonFile(fileName):
    content = open(fileName, 'rb').read()
    return json.JSONDecoder().decode(content)
