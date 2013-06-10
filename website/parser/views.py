#-*- coding:utf-8 -*-

from django.http import HttpResponse
from django.template import Template, Context
from django.template.loader import get_template

# test
from django.views.static import * 
from django.conf import settings

# mine
import article_refiner

def refine(request):
    article_refiner.refine()
    return HttpResponse('Refined !')
