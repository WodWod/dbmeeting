# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib import request
import re
import time
import mysql.connector 

conn = mysql.connector.connect(user='root', password='123456', database='dbmeeting')
cursor = conn.cursor()
cursor.execute('SET NAMES utf8mb4;')

class MyHTMLParser(HTMLParser):
    def init(self,person_id):
        self.__isEndPage=True
        self.__dataList=[]
        self.__nameData,self.__subjectData,self.__ratingData,self.__personData,self.__personId = '','','','',person_id
        self.limit_name,self.limit_em_end,self.limit_subject,self.limit_rating,self.limit_person = False,False,False,False,False
    
    def isEnd(self):
        return self.__isEndPage

    def handle_starttag(self, tag, attrs):
        limit_name=False
        limit_subject=False
        limit_rating=False
        limit_person=False

        if(tag=='div' and self.__isEndPage):
            for item in attrs:
                if item[0]=='class' and item[1]=='item':
                    self.__isEndPage=False


        if(tag=='em'): 
            limit_name=True 
        if(tag=='a'):
            if len(attrs) == 1:
                for attr in attrs:
                    if attr[0]=='href' and re.match(r'^https://music.douban.com/subject/',attr[1]):     
                        self.__subjectData = attr[1][len('https://music.douban.com/subject/'):-1]
                        limit_subject=True                 
                     
        if(tag=='span'): 
            for attr in attrs:
                if(attr[0]=='class'and re.match(r'^rating',attr[1])):
                    limit_rating=True   
                    self.__ratingData=int(attr[1][6:7])
        if(tag=='h1'): 
            limit_person=True       
    
        self.limit_name,self.limit_subject,self.limit_rating,self.limit_person = limit_name,limit_subject,limit_rating,limit_person
        self.limit_em_end=False       

    def handle_endtag(self, tag):
        if tag == 'html':
            for item in self.__dataList:
                cursor.execute('insert into music_person (subject_num,name,person_name,rating,person_id) values (%s, %s,  %s, %s , %s)', [item['subject_num'],item['name'],item['person_name'],item['rating'],self.__personId])   
            # print(str(self.__dataList))

        if tag =='em':
            self.limit_em_end = True
        else:
            self.limit_em_end = False

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.limit_name:
            self.__nameData=data.replace('\n','').strip()
        elif self.limit_em_end:
            self.__nameData += data.replace('\n','').strip()
        elif self.limit_subject:
            pass
        elif self.limit_rating :
            self.__dataList.append({'subject_num':self.__subjectData,'name':self.__nameData,'rating':self.__ratingData,'person_name':self.__personData})
        elif  self.limit_person:
            self.__personData=data[0:data.find('听过的音乐')]
            
        self.limit_name,self.limit_em_end,self.limit_subject,self.limit_rating,self.limit_person = False,False,False,False,False


    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

parser = MyHTMLParser()


class Music_List(object):
    def __init__(self,href):
        self.__href=href
        self.__personId = href[len('https://music.douban.com/people/'):href.find('/collect')]
        
    def write_data(self):
        try:
            for x in range(0,100):
                time.sleep(5)
                req=request.Request(self.__href+'?start=%s&sort=time&rating=all&filter=all&mode=grid' % str(x*15))
                req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
                # req.add_header('Cookie','ll="118267"; bid=2Gkun4aXaEg; __utma=30149280.325389959.1576659520.1576659520.1576659520.1; __utmc=30149280; __utmz=30149280.1576659520.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1576659543%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F45453613%2F%22%5D; _pk_id.100001.3ac3=dc97f5b5f0771093.1576659543.1.1576659543.1576659543.; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utmb=30149280.2.10.1576659520; __utma=81379588.2124264048.1576659543.1576659543.1576659543.1; __utmc=81379588; __utmz=81379588.1576659543.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/45453613/; __utmb=81379588.1.10.1576659543')
                with request.urlopen(req) as f:
                    parser.init(self.__personId)
                    data=f.read()
                    # print('data:', data.decode('utf-8'))
                    parser.feed(data.decode('utf-8'))
                    if(parser.isEnd()):
                        print('%s-音乐最后一页:%s' %(self.__personId,x*15))
                        break
        except BaseException as e:
                    print('Error:',e)
                    # 发生错误时回滚
                    conn.rollback()
        else:
            conn.commit()
        finally:
            pass
            # cursor.close()
            # conn.close()

    def close_link(self):
        cursor.close()
        conn.close()
                
# test=Music_List('https://music.douban.com/people/45453613/collect')
# test.write_data()



