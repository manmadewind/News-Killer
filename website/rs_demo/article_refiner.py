#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import pickle
import codecs
from label_generator import get_labels
from public_model import Article, Label

    
class Article_raw:
    title   = ""
    origin  = ""
    link    = ""
    summary = ""
    content = ""
    date    = ""
    
def dump(model, fileName):
    print '-dump %s' % fileName
    pickle.dump(model, codecs.open(fileName, 'wb', 'utf-8'))
    #pickle.dump(model, open(fileName, 'wb'))
    print '=dump %s' % fileName

def load(fileName):
    return pickle.load(open(fileName, 'r'))


def refine():
    '''
    return a list of parsed articles
    '''
    article_raw_list = __load_article_raw()
    article_list = []
    for a_raw in article_raw_list:
        label_dict = get_labels(a_raw.title, a_raw.summary)
        article = Article()
        article.title      = a_raw.title
        article.content    = a_raw.content
        article.summary    = a_raw.summary
        article.origin     = a_raw.origin
        article.link       = a_raw.link
        
        if label_dict is not None:
            for k,v in label_dict.iteritems():
                l = Label()
                l.text = k
                l.type = v
                
        article.label_dict = label_dict

        article_list.append(article)

    print ('after refine the length of article_list = %d' % len(article_list))
    dump(article_list, '__.data/articles_refine.list')
    return article_list


def __load_article_raw():
    raw_list = []
     # get raw article list
    files = []
    path = '__.article_raw/'
    for f in os.listdir(path):
        if f[0] == '.':
            continue
        files.append(path + f)
        raw_list.append(load(path + f))
    print ('after load raw article, list = %d' % len(raw_list))
    return raw_list


