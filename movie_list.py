# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib import request
import re
import time
import mysql.connector 
from config import config 
#浏览器头
from user_agent import Agent
agent= Agent()

conn = mysql.connector.connect(host=config['host'],user=config['user'], password=config['password'], database=config['database'])
cursor = conn.cursor()
cursor.execute('SET NAMES utf8mb4;')

#代理地址
from proxy_address import ProxyAddress
address_list =  ProxyAddress()
# address = address_list.get_data()

class MyHTMLParser(HTMLParser):
    def init(self,person_id):
        self.__isEndPage=True
        self.__dataList=[]
        self.__nameData,self.__subjectData,self.__ratingData,self.__personData,self.__img_src,self.__personId = '','','','','',person_id
        self.limit_img_src,self.limit_em_end,self.limit_name,self.limit_subject,self.limit_rating,self.limit_person = False,False,False,False,False,False
    
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
            if len(attrs)>2:
                for attr in attrs:
                    if attr[0]=='href':     
                        self.__subjectData = attr[1][len('https://music.douban.com/subject/'):-1]
                    if(attr[0]=='class'and re.match(r'^nbg',attr[1])):
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
                item['person_name']=self.__personData
                cursor.execute('insert into movie_person (subject_num,name,person_name,rating,person_id,img_src) values (%s, %s,  %s, %s , %s ,%s)', [item['subject_num'],item['name'],item['person_name'],item['rating'],self.__personId,item['img_src']])  
        # print(str(self.__dataList))

        if tag =='em':
            self.limit_em_end = True
        else:
            self.limit_em_end = False

    def handle_startendtag(self, tag, attrs):
        if tag == 'img':
            for attr in attrs:
                if attr[0]=='src' and attr[1].find('doubanio.com/icon/u') !=-1:
                    self.limit_img_src=True
                    self.__img_src = attr[1]

    def handle_data(self, data):
        if self.limit_name:
            self.__nameData=data.replace('\n','').strip()
        elif self.limit_em_end:
            self.__nameData += data.replace('\n','').strip()
        elif self.limit_subject:
            pass
        elif self.limit_rating : #不打分则不计入
            self.__dataList.append({'subject_num':self.__subjectData,'name':self.__nameData,'rating':self.__ratingData,'person_name':self.__personData,'img_src':self.__img_src,'timestamp':time.time()})
        elif  self.limit_person:
            self.__personData=data[0:data.find('看过的电影')]
        elif self.limit_img_src:
            pass
        self.limit_name,self.limit_em_end,self.limit_subject,self.limit_rating,self.limit_person,self.limit_img_src = False,False,False,False,False,False


    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

parser = MyHTMLParser()


class Movie_List(object):
    def __init__(self,href):
        self.__href=href
        self.__personId = href[len('https://movie.douban.com/people/'):href.find('/collect')]
        self.__count=0
        
    def write_data(self):
        for x in range(0,100):
            try:
                time.sleep(2)
                ProxyHandler = request.ProxyHandler(address_list.get_data())
                Opener = request.build_opener(ProxyHandler)
                request.install_opener(Opener)
                req=request.Request(self.__href+'?start=%s&sort=time&rating=all&filter=all&mode=grid' % str((x-self.__count)*15))
                req.add_header('User-Agent',agent.get_data())
                with request.urlopen(req,timeout=10) as f:
                    parser.init(self.__personId)
                    data=f.read()
                    # print('data:', data.decode('utf-8'))
                    parser.feed(data.decode('utf-8'))
                    if(parser.isEnd()):
                        print('%s-电影最后一页:%s' % (self.__personId,(x-self.__count)*15))
                        conn.commit()
                        break
            except BaseException as e:
                        # 发生错误时回滚
                        # conn.rollback() 
                        print('Movie Error:',e)  
                        if hasattr(e,'code'):
                            if not e.code == 404:
                                address_list.next()
                                self.__count+=1    
                            else:
                                break
                        else:
                            address_list.next()
                            self.__count+=1  

    def close_link(self):
        cursor.close()
        conn.close()
     
# test=Movie_List('https://movie.douban.com/people/79614632/collect?start=0&sort=time&rating=all&filter=all&mode=grid',{'HTTPS': '223.199.23.216:9999'})
# test.write_data()
# test.close_link()

