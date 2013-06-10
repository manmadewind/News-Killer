#-*- coding:utf-8 -*-
import sae.storage
import sys
sys.setdefaultencoding('utf-8')

def save(fileName, content):
# 初始化一个Storage客户端。
    s = sae.storage.Client()
# PUT object至某个domain下面，put操作返回object的public url。
    ob = sae.storage.Object(content)
    s.put('fs', fileName, ob)

def load(fileName):
# GET某个domain下的object
    s = sae.storage.Client()
    ob = s.get('fs', fileName)
    data = ob.data
    return data
