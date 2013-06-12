#-*- coding:utf-8 -*-
import sys
sys.setdefaultencoding('utf-8')


def get_summary(title, content): #TODO:
    '''
    生成摘要信息 # TODO: tf-idf
    '''
    if content is None:
        return ''
    
    return content[:140] + '... ...'
