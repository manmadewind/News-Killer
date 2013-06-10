#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import json
import codecs
import time
import datetime

from onepage.models import Article
from label_generator import get_labels_jieba as get_labels
from summary_maker import get_summary as get_summary
from score_calculator import get_count_from_baidu as get_score

sys.setdefaultencoding('utf-8')

def refine():
    '''
    return a list of parsed articles
    '''
    
    print 'begin to refine'
    article_list = __load_articles_today()
    for article in article_list:
        # generate labels
        article.mm_labels = get_labels(article.title, article.summary)

        # generate summary
        article.mm_summary = get_summary(article.title, article.content)

        # generate score
        article.mm_score = get_score(article.mm_labels.keys()) # score

        # Done.
        article.save()
    print 'end of refine'
    return article_list


def __load_articles_today():
    '''
    取得爬虫采集的文章集合(只获取当天的)
    '''
    
    print 'begin to load from db'
    today = datetime.date.today()
    return Article.objects.filter(\
                                  create_date__year=today.year,\
                                  create_date__month=today.month,\
        create_date__day=today.day)


