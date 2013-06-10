from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    #---crawler---#
    url('crawler_initial', 'crawler.views.startCrawler'),
    url('crawler_switch', 'crawler.views.switchCrawler'),
    url('^crawler$', 'crawler.views.crawler'),
    #---cleaner---#
    url(r'refine', 'parser.views.refine'),
    url(r'build', 'parser.views.build'),

    #---one page---#
    url(r'show', 'onepage.onepage.show'),
    #url(r'^mail$', 'onepage.mail_deliver.deliver'),
    url('makemail', 'onepage.mail_deliver3.generate_mail'),
    url(r'^send$', 'onepage.mail_deliver3.deliver'),
    url(r'^regist$', 'onepage.views.regist'),
    url(r'^regist_form$', 'onepage.views.regist_form'),    
    url(r'^$', 'onepage.onepage.show'),
    # Examples:
    # url(r'^$', 'website.views.home', name='home'),
    # url(r'^website/', include('website.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
