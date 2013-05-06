#!/user/bin/env python
#-*- coding:utf-8 -*-

'''
Public Method
'''
import re
import sys
import io
import codecs
      
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
	  print 'unicode done'

    return obj


def clean_content(content):
    try:
        content = str(content)
        content = re.sub("<img src=[^>]* alt=\"", "", content)
        content = re.sub("<.+?>", "", content)
        content = re.sub("&quot;", "\"", content)
        content = re.sub("&apos;", "\'", content)
        content = re.sub("&amp;", "&", content)
        content = re.sub("&lt;", "<", content)
        content = re.sub("&gt;", ">", content)
	content = re.sub('%nbsp;', "", content)
    except:
        print 'Exception in clean_content'
    return str(content)

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
