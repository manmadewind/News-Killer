import threading
import fetch_rss
from time import sleep

class CrawlerThread(threading.Thread):
    s_isworking = False
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print 'crawler thread begin to run!'
        CrawlerThread.s_isworking = True
        while True:
            if CrawlerThread.s_isworking == True:
                print 's_isworking:TRUE'
                fetch_rss.start()
            else:
                print 's_isworking:FALSE'
            sleep(1800)
