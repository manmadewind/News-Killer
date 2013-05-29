#!/usr/bin/env python
#-*- coding:utf-8 -*-

class Article:
    
    #label_list = []
    
    def __init__(self):
        self.title     = ""
        self.origin    = ""
        self.link      = ""
        self.summary   = ""
        self.summaryid = ""
        self.content   = ""
        self.date      = ""
        self.summary_auto = ""
        self.label_dict = dict()
        print 'initial article'

    def fromjson(self, d):
        self.title      = d['title']
        self.origin     =d['origin']
        self.link       =d['link']
        self.summary    =d['summary']
        self.content    =d['content']
        self.date       =d['date']
        if 'summaryid' in d:
            self.summaryid  =d['summaryid']
        if 'summary_auto' in d:
            self.summary_auto =d['summary_auto']
        
        self.label_dict =d['label_dict']

class Label:
    type = "l_3"
    text = "label"
    # --- --- ---


