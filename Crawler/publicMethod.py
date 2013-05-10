#!/user/bin/env python
#-*- coding:utf-8 -*-

'''
Public Method
'''
import re
import sys
import io
import codecs
import cPickle
from django.utils.html import strip_tags

def dump(model, fileName):
    cPickle.dump(model, codecs.open(fileName, 'wb', 'utf-8'))

def load(fileName):
    return cPickle.load(open(fileName, 'rb'))

def write_file_utf8(content, fileName='noname.txt'):
    try:
	content = to_unicode(content)
	f = codecs.open(fileName, 'w+','utf-8')
	f.write(content)
	f.close()
    except:
	log_error('error in write file utf8() \n %s' % str(sys.exc_info()[0]))
    print 'Done!'

    
def log_error(content):
    for i in sys.exc_info():
        print str(i)
    print >> sys.stderr, """\
    ERROR: %s
"""% content


def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
       if not isinstance(obj, unicode):
       	  obj = unicode(obj, encoding)
    return obj


def clean_content(content):

    print 'in clean_content'
    print type(content)    
    print content
    if content is None or content == '':
        return ''
    try:
        content = to_unicode(content)
        #?.encode('utf-8') why?
        
        content = strip_tags(content)
        content = re.sub("<img src=[^>]* alt=\"", "", content)
        content = re.sub("<.+?>", "", content)
        content = re.sub("&quot;", "\"", content)
        content = re.sub("&apos;", "\'", content)
        content = re.sub("&amp;", "&", content)
        content = re.sub("&lt;", "<", content)
        content = re.sub("&gt;", ">", content)
	content = re.sub('&nbsp;', "", content)
        return content
    
    except:
        print '---Exception in clean_content'
        log_error('cleaning')        
        return content


def write_file(content, fileName='noname.txt'):
    try:
        print "content = %s" % content
        print "fileName = %s" % fileName
        f = open(fileName, 'a+')
        f.write(content)
        f.close()
        #with io.open(fileName) as file:
        #    file.write(unicode(str(content)))
    except:
        log_error("error in write_file() \n %s" % str(sys.exc_info()[0]))
    print 'DONE!'
