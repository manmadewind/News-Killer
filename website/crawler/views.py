#-*- coding:utf-8 -*-
from django.http import HttpResponse

# test
from django.views.static import * 
from django.conf import settings

# mine
from crawler_thread import CrawlerThread
import fetch_rss

def crawler(request):
    fetch_rss.start()
    return HttpResponse('Fetch Done.')

g_crawlerThread = CrawlerThread()
def startCrawler(request):
    global g_crawlerThread
    CrawlerThread.s_isworking = True
    g_crawlerThread.start()
    return HttpResponse('Crawler thread is working now.');

def switchCrawler(request):
    if CrawlerThread.s_isworking == True:
        CrawlerThread.s_isworking = False
        return HttpResponse('Switch to STOP')
    
    else:
        CrawlerThread.s_isworking = True
        return HttpResponse('Switche to START')

        
