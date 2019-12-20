# -*- coding: utf-8 -*-
#头像地址 https://img3.doubanio.com/icon/u45453613.jpg

import mysql.connector 
import json
import math

conn = mysql.connector.connect(user='root', password='123456', database='dbmeeting')
cursor = conn.cursor()

class Recommend(object):
    def __init__(self,param):
        post_data=json.loads(param)
        self.__movie_list=post_data['movie']
        self.__book_list=post_data['book']
        self.__music_list=post_data['music']
        self.__person_list=[]

    def __serach_person(self):
        for item in self.__movie_list:
            cursor.execute('select person_id,person_name,rating from movie_person where  subject_num =%s',[item])
            values = cursor.fetchall()
            for value in values:
                has_data = False
                for person in self.__person_list:
                    if person['person_id'] == value[0]:
                        person['score'] += value[2]-3
                        has_data = True
                if not has_data:
                    self.__person_list.append({'person_id':value[0],'person_name':value[1],'score':value[2]-3})

        for item in self.__book_list:
            cursor.execute('select person_id,person_name,rating from book_person where  subject_num =%s',[item])
            values = cursor.fetchall()
            for value in values:
                has_data = False
                for person in self.__person_list:
                    if person['person_id'] == value[0]:
                        person['score'] += value[2]-3
                        has_data = True
                if not has_data:
                    self.__person_list.append({'person_id':value[0],'person_name':value[1],'score':value[2]-3})

        for item in self.__music_list:
            cursor.execute('select person_id,person_name,rating from music_person where  subject_num =%s',[item])
            values = cursor.fetchall()
            for value in values:
                has_data = False
                for person in self.__person_list:
                    if person['person_id'] == value[0]:
                        person['score'] += value[2]-3
                        has_data = True
                if not has_data:
                    self.__person_list.append({'person_id':value[0],'person_name':value[1],'score':value[2]-3})

    def __filter_data(self):
        self.__serach_person()
        self.__person_list = list(filter(lambda x:x['score']>0,self.__person_list))
        if len(self.__person_list)>0:
            if len(self.__person_list)>3:
                self.__person_list = self.__person_list[0:3]
            self.__person_list= sorted(self.__person_list,key=lambda x: x['score'],reverse=True)
            total_score = (len(self.__movie_list)+len(self.__book_list)+len(self.__music_list))*2
            for person in  self.__person_list:
                person['rate'] = math.ceil((person['score']/total_score)*100)
                person['img_src'] = 'https://img3.doubanio.com/icon/u%s.jpg' % person['person_id']

    def get_data(self):
        self.__filter_data()
        print(self.__person_list)

test= Recommend('{"movie":["25934014","3824274","27610855","26874505","27594217","10512661"],"book":[],"music":[]}')
test.get_data()



