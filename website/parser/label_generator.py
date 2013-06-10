#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import jieba
import jieba.analyse
'''
拆分词 根据tf * idf 计算大小
'''
from text_helper import isEnglish, isChinese

def get_labels_jieba(u_title, u_content=""):
    '''
    use jieba to find words
    '''
    

    result_dict = dict()
    count_dict = dict()
    manual_dict = __get_manual_dict()
    
    # get terms from my old method
    terms = __get_words(u_title)

    count = 0
    for term in terms:
        if term in manual_dict:
            result_dict[__get_string(term)] = manual_dict[term]
            count += 1
            if count >=3 :
                break
            
    # use jieba
    # load user dict first
    # ##jieba.load_userdict('static/res/__.dicts/manmade_dict.txt') 
    labels = jieba.analyse.extract_tags(u_title, 4 - len(result_dict)) # extract 3+1 first    
    temp_max = 0
    prettyimportant = ''
    
    for label in labels:
        if len(re.findall(label, u_content)) > temp_max:
            temp_max = len(re.findall(label, u_content))
            prettyimportant = label
        if label in manual_dict:
            result_dict[label] = manual_dict[label]
        else:
            result_dict[label] = 'l_3'


    if prettyimportant != '':
        print prettyimportant
        print result_dict[prettyimportant]
    
    if prettyimportant != '' and result_dict[prettyimportant] != 'l_1':
        result_dict[prettyimportant] = 'l_2'
        print prettyimportant

    if len(result_dict) > 3:
        for key in result_dict.keys():
            if result_dict[key] == 'l_3':
                del result_dict[key]
                break

    return result_dict


def get_labels(u_title, u_content=""):
    terms = __get_words(u_title)
    
    manual_dict = __get_manual_dict()
    #weight_dict = __get_weight_dict()

    result_dict = dict()
    #temp_dict = dict()

    count = 0
    for term in terms:
        if term in manual_dict:
            result_dict[__get_string(term)] = manual_dict[term]
            count += 1
            if count >= 3:
                break
            continue
    '''    
        if term in weight_dict:
            temp_dict[term] = weight_dict[term]
            print '%s,%f' % (term, temp_dict[term])
            continue

    # find content
    if len(result_dict) < 3 and u_content != "":
        terms = __get_words(u_content)
        for term in terms:
            if term in manual_dict and term not in result_dict:
                result_dict[__get_string(term)] = manual_dict[term]
                continue

            if term in weight_dict and term not in temp_dict:
                temp_dict[__get_string(term)] = weight_dict[term]
                #print '%s,%f' % (term, temp_dict[term])
                continue

        
    if len(result_dict) < 3:
        sorted_list = sorted(temp_dict.items(), key = lambda x: x[1], reverse = True)
        if sorted_list != None and len(sorted_list) > 1:
            pass
            #result_dict[sorted_list[0]] = 'l_3'
            #temp comment it
    '''
    print 'FINALLY got labels:'
    for k,v in result_dict.iteritems():
        print k
    return result_dict

def __get_string(term):
    if isinstance(term, unicode):
        term = term.encode('utf-8')
    return term
    

def __get_words(u_content):
    raw_strings = []
    i = 0
    while i < len(u_content):
        string = ""
        if isChinese(u_content[i]):
            while i < len(u_content) and isChinese(u_content[i]) == True:
                string += u_content[i]
                i += 1
        elif isEnglish(u_content[i]):
            while i < len(u_content) and isEnglish(u_content[i]) == True:
                string += u_content[i]
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

def __get_manual_dict():
    manual_dict = dict()
    __generate_dict(manual_dict, 'static/res/__.dicts/m_dict_1.txt', 'l_1')
    __generate_dict(manual_dict, 'static/res/__.dicts/m_dict_2.txt', 'l_2')
    #__generate_dict(manual_dict, 'static/res/__.dicts/m_dict_3.txt', 'l_3')
    print 'manual_dict DONE. len:%d' % len(manual_dict)
    return manual_dict
    
def __generate_dict(manual_dict, fileName, level):
    f = open(fileName)
    for item in f.readlines():
        i = item.replace('\n','').decode('utf-8')
        if i not in manual_dict:
            manual_dict[i] = level
            
    
