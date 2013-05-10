#!/usr/bin/env python
#-*- coding:utf-8 -*-
from char_parse import isChinese, isEnglish
import cPickle
import codecs
import os

def dump(model, fileName):
    cPickle.dump(model, codecs.open(fileName, 'wb', 'utf-8'))

def load(fileName):
    return cPickle.load(open(fileName, 'rb'))

def calculate():
    biGram_dict = dict()
    termSum_dict = dict()
    
    #files = ['0.txt']
    files = []
    path = './article_train/'
    for f in os.listdir(path):
        if f[0] == '.':
            continue
        files.append(path + f)
        
    docCount = 0
    for f in files:
        docCount += 1
        content = open(f, 'r+').read().decode('utf-8')
        biGram_dict, termSum = word_calculate(biGram_dict, docCount, content)
        termSum_dict[docCount] = termSum
    print 'parse done'
    
    print 'begin to dump'
    dump(biGram_dict, 'data/biGram_dict_raw.dict')
    dump(termSum_dict, 'data/termSum.dict')
    print 'dump done'
    print 'detail start'
    generateDetail(biGram_dict, termSum_dict, docCount)
    print 'detail done'
    return biGram_dict

def generateDetail(raw_dict, sum_dict, sum_doc):
    import math
    tc_dict = dict()
    detail_dict = dict()
    for k, v in raw_dict.iteritems():
        if v[0] < 5:
            continue

        tCount = v[0]
        dCount = len(v[1:])
        tc_dict[k] = tCount

        # tf, idf, tf * idf
        tf = tCount / len(sum_dict)
        idf = math.log(float(sum_doc) / len(raw_dict[k][1:]))
        detail_dict[k] = [tf, idf, tf * idf]
    dump(tc_dict, 'data/termCount.dict')
    dump(detail_dict, 'data/tidf.dict')

    
    file = open('data/termCount.txt','w')
    for k,v in tc_dict.iteritems():
        file.write('%s\t%s\n' % (k.encode('utf-8'), str(v)))

def word_calculate(biGram_dict, docId, content):
    i = 0
    termSum = 0
    while i < len(content):
        term, i = bigram_find(content, i)
        if term == "" and i == -1:
            break

        termSum += 1

        if term in biGram_dict:
            biGram_dict[term][0] += 1 # term count
        else:
            biGram_dict[term] = [1, 1/len(content)] # new term, append<term count, term frequency>

        #for df
        if docId not in biGram_dict[term][1:]:
            biGram_dict[term].append(docId) # doc ID

    #print ('dict len:%d' % len(biGram_dict))
    return biGram_dict, termSum
    
def bigram_find(content, i):
    while i < len(content):
        if isChinese(content[i]):
            if (i + 1) < len(content) and isChinese(content[i + 1]):
                term = content[i:i + 2]                
                return term, i + 1
            i = i + 1
            
        elif isEnglish(content[i]):
            delta = 1
            while (i + delta) < len(content) and isEnglish(content[i + delta]):
                delta += 1
            term = content[i:i + delta].lower() # to lower
            #print term
            i += delta
            return term, i
        else:
            i += 1
    return "", -1
