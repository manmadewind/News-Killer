import codecs

def save(fileName, content, isappend=True):
    try:
        if isappend is True:
            op = 'wb+'
        else:
            op = 'wb'
        
        f = codecs.open(fileName, op, 'utf-8')
        f.write(content)
        f.flush()
        f.close()
    except Exception as e:
        print 'error in save()'
        print e


def load(fileName):
    try:
        f = codecs.open(fileName, 'rb', 'utf-8')
        content = f.read()
        f.close()
    except Exception as e:
        print 'error in load()'
        print e
        return None
    return content
