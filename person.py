# -*- coding: utf-8 -*-
# robots.txt
from html.parser import HTMLParser
from urllib import request
import re
import time

# movie 
# subject 25853071 name 庆余年 person 闲不住的小绵羊 rating 5 
class Person(object):
    def __init__(self,href):
        self.__href = href
        self.__movie_href = 'https://movie.' + href[8:] + 'collect'
        self.__book_href = 'https://book.' + href[8:] + 'collect'
        self.__music_href = 'https://music.' + href[8:] + 'collect'

    
        