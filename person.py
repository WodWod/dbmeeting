# -*- coding: utf-8 -*-
# robots.txt
from html.parser import HTMLParser
from urllib import request
import re
import time

# movie_person book_person music_person
# subject_num 25853071 name 庆余年 person_name 闲不住的小绵羊 person_id  rating 5 timestamp  1:-2 2:-1 3:0 4:+1 5:+2

#subject
# num 25853071 name 庆余年 type movie

#person
#name 闲不住的小绵羊 sex 1


class Person(object):
    def __init__(self,href):
        self.__href = href
        self.__movie_href = 'https://movie.' + href[8:] + 'collect'
        self.__book_href = 'https://book.' + href[8:] + 'collect'
        self.__music_href = 'https://music.' + href[8:] + 'collect'

    
        