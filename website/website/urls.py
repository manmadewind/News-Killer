from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #---crawler---#
    url('^crawler_initial$', 'crawler.views.startCrawler'),
    url('^crawler_switch$',  'crawler.views.switchCrawler'),
    url('^crawler$',         'crawler.views.crawler'),
    
    #---parser---#
    url(r'^refine$', 'parser.views.refine'),

    #---one page---#
    url(r'^build$',       'onepage.views.build'),    
    url(r'^show$',        'onepage.views.show'),
    url('^makemail$',     'onepage.mail_deliver3.generate_mail'),
    url(r'^send$',        'onepage.mail_deliver3.deliver'),
    url(r'^regist$',      'onepage.views.regist'),
    url(r'^regist_form$', 'onepage.views.regist_form'),    
    url(r'^$',            'onepage.views.show'),

    #---TEST---#
    url(r'^test$', 'onepage.views.testshow'),
    url(r'^testbtn$', 'onepage.views.testbtn'),
    url(r'pre', 'onepage.views.set'),

)
