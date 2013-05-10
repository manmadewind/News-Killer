#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os

def isChinese(u_char):
    if u_char >= u'\u3300' and u_char <= u'\u9fff':
        return True
    return False

def isEnglish(u_char):
    # lower char [0061, 007a]
    # upper char [0041, 005a]
    return judge(u_char, u'\u0061', u'\u007a') or \
        judge(u_char, u'\u0041', u'\u005a')


def isDigit(u_char):
    return judge(u_char, u'\u0030', u'\u0039')

# !!!Not implement!!!
def isSymbol(u_char):
    #全角符号[fe30, ffa0]
    return False
#return judge(u_char, u'\ufe30', u'\uffa0')

def judge(u_char, lower, upper):
    if u_char >= lower and u_char <= upper:
        return True
    return False



def gram_2(content):
    cn_dict = dict()
    i = 0
    while i < len(content):
        if isChinese(content[i]):
            if (i + 1) < len(content) and isChinese(content[i + 1]):
                term = content[i:i + 2]                
                #print term
            i = i + 1
            
        elif isEnglish(content[i]):
            delta = 1
            while (i + delta) < len(content) and isEnglish(content[i + delta]):
                delta += 1
            term = content[i:i + delta]
            #print term
            i += delta
        else:
            i += 1
    return cn_dict


def find_similiar_word(term_list):
    candidate_dict = dict()
    termCount_dict = get_term_count()
    result_list = term_list

    content_list = []
    path = './article_train/'
    for f in os.listdir(path):
        if f[0] == '.':
            continue
        content_list.append(open(path + f, 'r').read().decode('utf-8'))

    # start from here
    count = 0
    
    for word in result_list:
        count += 1
        print 'count:%d\tlen of list:%d' %(count, len(result_list))
        if count > 2:
            print '>20000!'
            break

        templates = []
        for content in content_list:
            temp_template = find_template(word, content)
            if temp_template is None:
                continue
            templates.extend(temp_template) # extend not append here.

        for content in content_list:
            for i in range(len(templates) / 2):
                new_terms = find_new_word(templates[i*2], templates[i*2+1], \
                                          content, word)
                
                for new_word in new_terms:
                    if new_word not in candidate_dict:
                        candidate_dict[new_word] = 1
                    else :
                        candidate_dict[new_word] += 1
                        
                    if new_word in result_list: # alread in
                        continue;
                    if validTermCount(new_word, termCount_dict):
                        result_list.append(new_word)

    file1 = open('new_word.txt', 'w')
    file2 = open('new_word_dict.txt', 'w')
    for k,v in candidate_dict.iteritems():
        tc = get_tc(k, termCount_dict)
        print ('term:%s,count:%d' % (k,tc))
        candidate_dict[k] = tc * v
        
    for k,v in sorted(candidate_dict.items(), key=lambda x:x[1], reverse=True):
        file2.write('%s\t%d\n' %(k.encode('utf-8'),v))
    for i in result_list:
        file1.write('%s\n' % i.encode('utf-8'))

    return result_list
def get_tc(word, t_dict):
    if len(word) == 2:
        if word not in t_dict:
            return 0
        else:
            return t_dict[word]
    elif len(word) > 2:
        i = 0
        temp_min = 99999
        temp_max = 0
        while i + 1 < len(word):
            temp = get_tc(word[i:i+2], t_dict)
            i += 1
            temp_max = max(temp_max, temp)
            temp_min = min(temp_min, temp)
        return (temp_min + temp_max) / 2
    return 0

def validTermCount(word, t_dict):
    if len(word) == 2:
        if word in t_dict:
            return True
        else:
            return False
    elif len(word) > 2:
        if word[:2] in t_dict:
            return True
        else:
            return False
    return False

def find_template(word, content):
    templates = []
    index = content.find(word)
    if index == -1:
        return None

    while (index - 1) in range(len(content)) and \
        (index + 1) in range(len(content)):
        content = content[index + 1:]
        index = content.find(word)
        if index == -1:
            break
        
        pre = content[index - 1]
        post = content[index + len(word)]
        templates.append(pre)
        templates.append(post)
        index += 1
    return templates


    '''
    while (isChinese(content[index-1]) and isChinese(content[index-2])\
        and isChinese(content[index+1]) and isChinese(content[index+2])) is False:
        index = content[index + 1:]
        if index == -1:
            return None
    pre = content[index - 2: index]
    post = content[index + len(word): index + len(word) + 2]
    print pre
    print post
    return pre, post            
    '''

def find_new_word(pre, post, content, old_word=""):
    term_list = []
    delta = 0
    while delta < len(content):
        content = content[delta:]
        p_pre = content.find(pre)
        p_post = content.find(post)
        if p_pre == -1 or p_post == -1:
            break
        span = p_post - p_pre - len(pre)
        if span <= 5 and span > 1:
            term = content[p_pre + len(pre):p_post]
            if term != old_word and isValid(term):
                term_list.append(term)
            #print term
        delta = min(p_pre, p_post) + 1
    return term_list

def isValid(term):
    if len(term) < 1 or len(term) > 5:
        return False

    for c in term:
        if isChinese(c) == False:
            return False

    return True

def get_term_count():
    import cPickle
    return cPickle.load(open('data/termCount.dict', 'rb'))


'''
index()
isalnum alphanumeric?
isalpha?
isdecimal
isdigit
islower
isnumeric
isspace
isupper
replace()
rfind() rindex
'''
