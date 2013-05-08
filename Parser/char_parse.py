#!/usr/bin/env python
#-*- coding:utf-8 -*-

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


def find_similiar_word(terms, content):
    result = terms
    count = 0
    for word in result:
        count += 1
        if count > 20000:
            print '>20000!'
            break
        
        templates = find_template(word, content)
        for i in range(len(templates) / 2):
            new_terms = find_new_word(templates[i*2], templates[i*2+1], \
                                      content, word)
            for new_word in new_terms:
                if new_word not in result:
                    result.append(new_word)
    return terms

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
    terms = []
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
                terms.append(term)
            #print term
        delta = min(p_pre, p_post) + 1
    return terms

def isValid(term):
    if len(term) < 1 or len(term) > 5:
        return False

    for c in term:
        if isChinese(c) == False:
            return False
    return True

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
