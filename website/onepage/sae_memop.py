#-*- coding:utf-8 -*-
import pylibmc

import sae.storage
import sys
sys.setdefaultencoding('utf-8')

def save(key, content):
    mc = pylibmc.Client()
    mc.set(key, content)
        
def load(key):
    mc = pylibmc.Client()    
    value = mc.get(key)
    return value
    

