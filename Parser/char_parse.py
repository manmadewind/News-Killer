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
    print 'hello world'
    termCount_dict = get_term_count()

    real_words = get_train_words()
    term_list.append(real_words[200])    
    term_list.append(real_words[100])
    term_list.append(real_words[300])
    result_list = term_list

    content_list = []
    path = './article_train/'
    for f in os.listdir(path):
        if f[0] == '.':
            continue
        content_list.append(open(path + f, 'r').read().decode('utf-8'))

    # start from here
    count = 0
    p_count = 0
    for word in result_list:
        count += 1
        
        print 'count:%d\tlen of list:%d' %(count, len(result_list))
        if count > 2:
            print '>20000!'
            break

        # get patterns
        pattern_list = []
        for content in content_list:
            temp_pattern_list = find_patterns(word, content)
            if temp_pattern_list is None or len(temp_pattern_list) == 0:
                continue
            pattern_list.extend(temp_pattern_list) # extend not append here.
            print 'pattern count = %d' % len(pattern_list)

        # user patterns to find new words
        for content in content_list:
            for pattern in pattern_list:
                term_candidates = find_new_word(pattern, content, word)

                # varify new candidate
                for new_word in term_candidates:
                    # pattern verification
                    pattern.raw_candidates.append(new_word)

                    if isValid(new_word) == False:
                        continue
                    
                    # calculate term count
                    if new_word not in candidate_dict:
                        candidate_dict[new_word] = 1
                    else:
                        candidate_dict[new_word] += 1
                        
                    if new_word in result_list: # alread in
                        continue;

                    if new_word in real_words:
                        print ('find REAL WORD:%s' % new_word)
                        pattern.fine_candidates.append(new_word)
                    if validTermCount(new_word, termCount_dict):
                        result_list.append(new_word)
                        # pattern verification
                    
                # out for new_word
                pattern.save()
            # out for pattern
        # for content
                
                        

    file1 = open('new_word.txt', 'w')
    file2 = open('new_word_dict.txt', 'w')
    '''temp##
    for k,v in candidate_dict.iteritems():
        tc = get_tc(k, termCount_dict)
        #print ('term:%s,count:%d' % (k,tc))
        candidate_dict[k] = tc * v
    '''
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

class Pattern():
    pre = ""
    post = ""
    raw_candidates = []
    fine_candidates = []
    confidence = 1.0
    
    def __init__(self, p_pre, p_post):
        self.pre = p_pre
        self.post = p_post
    def save(self):
        if len(self.raw_candidates) == 0 or len(self.fine_candidates) == 0:
            self.confidence = 0
            return
        
        else:
            self.confidence = len(self.fine_candidates) / float(len(self.raw_candidates))

        
        f = open('pattern/%d:%f:%s-%s.txt' % (len(self.fine_candidates), self.confidence, self.pre.encode('utf-8'), self.post.encode('utf-8')), 'w')
        f.write('raw::\n')
        for c in self.raw_candidates:
            f.write('%s\n' % c.encode('utf-8'))
        f.write('fine::\n')
        for c in self.fine_candidates:
            f.write('%s\n' % c.encode('utf-8'))
        f.close()

def find_patterns(word, content):
    pattern_list = []
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
        p = Pattern(pre, post)
        
        pattern_list.append(p)
        index += 1
    return pattern_list


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

def find_new_word(pattern, content, old_word=""):
    term_list = []
    delta = 0
    pre = pattern.pre
    post = pattern.post
    while delta < len(content):
        content = content[delta:]
        p_pre = content.find(pre)
        p_post = content.find(post)
        if p_pre == -1 or p_post == -1:
            break
        span = p_post - p_pre - len(pre)
        if span <= 5 and span > 1:
            term = content[p_pre + len(pre):p_post]
            if term != old_word:
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

def get_train_words():
    print 'IN get train words!'
    real_words = []
    f = open('train_words.txt', 'r')
    for i in f.readlines():
        if ':' not in i:
            real_words.append(i.decode('utf-8').replace('\n',''))

    print ('len:%d' % len(real_words))
    return real_words


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
