from django.utils.html import strip_tags

import functools
import time
import re

def errorCatcher(func):
    @functools.wraps(func)
    def __do__(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print '!!!Error in %s' % str(func)
            print '\tMessage:%s' % str(e)
            #print '\tTime:' % time.strftime('%Y-%m-%d %H:%M:%S')            
            return None
        return result
    return __do__


@errorCatcher
def setDefaultEncoding():
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print 'reset defaultEncoding = %s' % sys.getdefaultencoding()


@errorCatcher
def to_unicode(obj, encoding='utf-8'):
    if isinstance(obj, basestring):
       if not isinstance(obj, unicode):
       	  obj = unicode(obj, encoding)
    return obj


@errorCatcher
def clean_html_tags(content):
    if content is None or content == '':
        return ''

    content = to_unicode(content)
    content = strip_tags(content)
    content = re.sub("<img src=[^>]* alt=\"", "", content)
    content = re.sub("<.+?>",  "",   content)
    content = re.sub("&quot;", "\"", content)
    content = re.sub("&apos;", "\'", content)
    content = re.sub("&amp;",  "&",  content)
    content = re.sub("&lt;",   "<",  content)
    content = re.sub("&gt;",   ">",  content)
    content = re.sub('&nbsp;', " ",   content)
    
    return content
