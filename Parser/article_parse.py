#!/usr/bin/env python
#-*- coding:utf-8 -*-

from text_helper import isChinese, isEnglish
import cPickle
import codecs
import os
'''
对训练样本进行分析，
采用2-gram的方式进行，
最后主要生成的文件有:
bigram_detail.dict
{
  'Term': [tf*idf, tf, idf],
  ...
}
'''
def __dump(model, fileName):
    cPickle.dump(model, codecs.open(fileName, 'wb', 'utf-8'))

def __load(fileName):
    return cPickle.load(open(fileName, 'rb'))

def train():
    raw_biGram_dict = dict()
    # {term: [termCount, docID1, docID2, ...]}
    
    termOfArticle_dict = dict() # {docID: number of term}
    
    # get train set
    files = []
    path = '__.article_train/'
    for f in os.listdir(path):
        if f[0] == '.':
            continue
        files.append(path + f)
        
    docCount = 0
    for f in files:
        docCount += 1
        content = open(f, 'r+').read().decode('utf-8')
        raw_biGram_dict, termSumOfArticle = __word_calculate(raw_biGram_dict, docCount, content)
        termOfArticle_dict[docCount] = termSumOfArticle
        
    print 'parse done'
    
    print 'begin to dump'
    __dump(raw_biGram_dict, '__.data/raw_biGram_dict.dict')
    __dump(termOfArticle_dict, '__.data/termOfArticle.dict')
    print 'dump done'
    print 'detail start'
    __generateDetail(raw_biGram_dict, termOfArticle_dict, docCount)
    print 'detail done'
    return raw_biGram_dict

def __generateDetail(raw_dict, sum_dict, sum_doc):
    import math
    
    tc_dict     = dict()
    detail_dict = dict()
    
    for k, v in raw_dict.iteritems():
        if v[0] < 2: # term count < 5, pass
            continue

        tCount = v[0]
        dCount = len(v[1:])
        tc_dict[k] = tCount

        # tf, idf, tf * idf
        tf  = float(tCount) / len(sum_dict)
        idf = math.log(float(sum_doc) / len(raw_dict[k][1:]))
        detail_dict[k] = [tCount * idf, tCount, idf]
        
    __dump(detail_dict, '__.data/bigram_detail.dict')

    
    file = open('__.data/termCount.txt','w')
    for k,v in tc_dict.iteritems():
        # word, tcount, dcount
        file.write('%s\t%d\t%d\t%f\n' % (k.encode('utf-8'), v, len(raw_dict[k][1:]),  math.log(float(sum_doc) / len(raw_dict[k][1:]))))

def __word_calculate(biGram_dict, docId, content):
    i = 0
    termSum = 0
    while i < len(content):
        term, i = __bigram_find(content, i)
        if term == "" and i == -1:
            break

        termSum += 1

        if term in biGram_dict:
            biGram_dict[term][0] += 1 # term count
        else:
            biGram_dict[term] = [1]#, 1/len(content)] # new term, append<term count, term frequency>

        #for df
        if docId not in biGram_dict[term][1:]:
            biGram_dict[term].append(docId) # doc ID

    #print ('dict len:%d' % len(biGram_dict))
    return biGram_dict, termSum
    
def __bigram_find(content, i):
    '''寻找2-gram'''
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
