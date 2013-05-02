# Create your views here.
from django.core.mail import send_mail
# for HTML mail
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.template.loader import render_to_string

def sendmail(title, content, list):
    r = send_mail(title, content, 'manmadewind@gmail.com', list, fail_silently = False)
    if r == 1:
        print 'Send mail successful!'
    else :
        print 'Send mail failed.'

def send_html_mail(subject, content, list):
    mail = EmailMultiAlternatives(subject, strip_tags(content), 'manmadewind@gmail.com', list)
    mail.attach_alternative(content, "text/html")
    mail.send()

def generateCSSmail():
    content = '\
    <div>\
    <style type="text/css">\
    <h2>Mail Deliver!</h2>\
    <p style="color:#f11">I am supposed to be RED:)</p>\
    </div>\
    '
