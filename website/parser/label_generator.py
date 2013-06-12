#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import jieba
import jieba.analyse
from onepage.publicMethod import errorCatcher, to_unicode
from text_helper import isEnglish, isChinese


@errorCatcher
def get_labels_jieba(p_title, p_content=""):
    '''
    use jieba to find words
    '''
    result_dict = dict() # <key: Term, value: Level>
    
    # 1.generate labels  from my method
    manual_dict = __get_manual_dict()    
    for term in __get_words(p_title):
        if term in manual_dict:
            result_dict[to_unicode(term)] = manual_dict[term]
            if len(result_dict) >=3 :
                break

    # 2.generate labels from JIEBA
    # -2.1 load user dict first
    # ##jieba.load_userdict('static/res/__.dicts/manmade_dict.txt')

    # -2.2 extract 3+1 terms first
    terms = jieba.analyse.extract_tags(p_title, 4 - len(result_dict))

    # -2.3 find important term
    temp_max = 0
    prettyimportant = ''
    for term in terms:
        if len(re.findall(term, p_content)) > temp_max:
            temp_max = len(re.findall(term, p_content))
            prettyimportant = term
            
        if term in manual_dict:
            if term not in result_dict.keys():
                result_dict[term] = manual_dict[term]
        else:
            result_dict[term] = 'l_3'
    
    if prettyimportant != '' and result_dict[prettyimportant] != 'l_1':
        result_dict[prettyimportant] = 'l_2'

        # 超过3个标签时(4个)，删掉不重要的一个
        if len(result_dict) > 3:
            for key in result_dict.keys():
                if result_dict[key] == 'l_3':
                    del result_dict[key]
                    break

    return result_dict


@errorCatcher
def __get_manual_dict():
    '''
    将自建词库从磁盘载入系统内存中
    '''
    manual_dict = dict()
    __load_dict(manual_dict, 'static/res/__.dicts/m_dict_1.txt', 'l_1')
    __load_dict(manual_dict, 'static/res/__.dicts/m_dict_2.txt', 'l_2')
    print 'manual_dict DONE. len:%d' % len(manual_dict)
    return manual_dict


@errorCatcher    
def __load_dict(manual_dict, fileName, level):
    '''
    将自建词库从磁盘载入系统内存中的具体操作
    '''
    f = open(fileName)
    for item in f.readlines():
        i = item.replace('\n','').decode('utf-8')
        if i not in manual_dict:
            manual_dict[i] = level


@errorCatcher
def __get_words(p_content):
    raw_strings = []
    i = 0
    while i < len(p_content):
        string = ""
        if isChinese(p_content[i]):
            while i < len(p_content) and isChinese(p_content[i]) == True:
                string += p_content[i]
                i += 1
        elif isEnglish(p_content[i]):
            while i < len(p_content) and isEnglish(p_content[i]) == True:
                string += p_content[i]
                i += 1
        else:
            i += 1
            continue

        raw_strings.append(string)
    # out of while
        
    words = []
    for string in raw_strings:
        if isEnglish(string[0]):
            words.append(string)
            continue

        if isChinese(string[0]):
            for i in range(len(string) - 1):
                for delta in range(2,5):
                    if i + delta > len(string):
                        break
                    words.append(string[i:i+delta])
    return words
