#!/usr/bin/env python
#-*- coding:utf-8 -*-
    
class Article_raw:
    title   = ""
    origin  = ""
    link    = ""
    summary = ""
    content = ""
    date    = ""

class Article:
    title     = ""
    origin    = ""
    link      = ""
    summary   = ""
    summaryid = ""
    content   = ""
    date      = ""
    #label_list = []
    
    def __init__(self):
        self.label_list = []
        
class Label:
    type = "l_3"
    text = "label"
    # --- --- ---


