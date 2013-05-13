#!/usr/bin/env python
#-*- coding:utf-8 -*-

'''
拆分词 根据tf * idf 计算大小
'''
from char_parse import isEnglish, isChinese

def get_labels(u_content):
    weight_dict = __read_weight_dict()
    terms = __get_words(u_content)
    
    temp_dict = dict()
    for term in terms:
        if term in weight_dict:
            temp_dict[term] = weight_dict[term]
            print '%s,%f' % (term, temp_dict[term])
            
    sorted_list = sorted(temp_dict.items(), key = lambda x: x[1], reverse = True)
    return sorted_list[:4]

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


def __read_weight_dict():
    import cPickle
    return cPickle.load(open('data/words.dict'))
