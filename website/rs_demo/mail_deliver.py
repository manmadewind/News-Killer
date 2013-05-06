import feedparser
from bs4 import BeautifulSoup
import urllib2
from django.utils.html import strip_tags
#
from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

# mail
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

class Article:
    title = ""
    ref = ""
    link = ""
    summary = ""
    date = ""

def send_html_mail(subject, content, list):
    mail = EmailMultiAlternatives(subject, strip_tags(content), 'manmadewind@gmail.com', list)
    mail.attach_alternative(content, "text/html")
    mail.send()

def deliver(request):
    url = 'http://www.huxiu.com/rss/1.xml'
    list = fetch_rss(url)
    t = get_template('mail.html')
    html = t.render(Context({'article_list': list}))

    mail_list = ['zhuayuba@hotmail.com']
    send_html_mail('Secret Mail From Brother FENG!', html, mail_list)
    
    return HttpResponse(html)

def fetch_rss(url):
    entries = 'entries'
    rss_source = feedparser.parse(url)
    if (rss_source[entries] is None or
        len(rss_source[entries]) == 0):
        return None
    
    rss_source_title = rss_source['feed']['title']
    article_list = []
    count = 0
    for entity in rss_source[entries]:
        if count > 5:
            break
        
        count+=1
        # md5 the title
        article = Article()
        
        article.title = entity.title
        article.summary = strip_tags(entity.summary)
        article.link = entity.link
        article.date = entity.published
        article.ref = rss_source_title
        
        article_list.append(article)

    return article_list

def generate_html_mail(list):
    for item in list:
        title, link, summary = item.split('::')
        
    

def get_fulltext(url, summary):
    '''
    TODO:
    '''
    soup = get_html_soup(url)
    

def get_html_soup(url):
    try:
        html_content = ""
        html_content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(html_content)
        return soup
    except:
        print 'Exception in get_html()'
        return None
