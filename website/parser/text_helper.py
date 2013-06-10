#!/usr/bin/env python
#-*- coding:utf-8 -*-
import os

def isChinese(u_char):
    if u_char >= u'\u3300' and u_char <= u'\u9fff':
        return True
    return False

def isEnglish(u_char):
    # lower char [0061, 007a]
    # upper char [0041, 005a]
    return judge(u_char, u'\u0061', u'\u007a') or \
        judge(u_char, u'\u0041', u'\u005a')


def isDigit(u_char):
    return judge(u_char, u'\u0030', u'\u0039')

# !!!Not implement!!!
def isSymbol(u_char): #TODO:
    #全角符号[fe30, ffa0]
    return False


def judge(u_char, lower, upper):
    if u_char >= lower and u_char <= upper:
        return True
    return False
