# -*- coding: utf-8 -*-
# robots.txt
from html.parser import HTMLParser
from urllib import request
import re
import time
from movie_list import Movie_List
from book_list import Book_List
from music_list import Music_List

import mysql.connector 

conn = mysql.connector.connect(user='root', password='123456', database='dbmeeting')
cursor = conn.cursor()

# movie_person book_person music_person
# subject_num 25853071 name 庆余年 person_name 闲不住的小绵羊 person_id  rating 5 timestamp  1:-2 2:-1 3:0 4:+1 5:+2

#subject
# num 25853071 name 庆余年 type movie

#person
#person_id 45453613 sex 1
#71098717


movie,book,music=None,None,None

class Person(object):
    def __init__(self,href):
        self.__wrote = True
        self.__href = href.replace('www.','')
        self.__movie_href = 'https://movie.' + self.__href[len('https://'):] + 'collect'
        self.__book_href = 'https://book.' + self.__href[len('https://'):] + 'collect'
        self.__music_href = 'https://music.' + self.__href[len('https://'):] + 'collect'

    def write_data(self):
        movie=Movie_List(self.__movie_href)
        book=Book_List(self.__book_href)
        music=Music_List(self.__music_href)

        self.__is_wrote()
        if not self.__wrote:
            movie.write_data()
            book.write_data()
            music.write_data()

    def __is_wrote(self):
        try:
            cursor.execute('select * from person where person_id = %s',(self.__href[len('https://douban.com/people/'):-1],))   
            values = cursor.fetchall()
            if len(values)== 0:
                self.__wrote = False
                cursor.execute('insert into person (person_id) values (%s)',[self.__href[len('https://douban.com/people/'):-1]])     

        except BaseException as e:
            print('Error:',e)
        finally:
            if not self.__wrote:
                conn.commit()
            # cursor.close()
            # conn.close()

    def close_link(self):
        movie.close_link()
        book.close_link()
        music.close_link()
        cursor.close()
        conn.close()
        

test=Person('https://www.douban.com/people/willow/')
test.write_data()
    
        