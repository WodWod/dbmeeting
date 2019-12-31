# -*- coding: utf-8 -*-
#代理地址 https://www.xicidaili.com/nn/1
from html.parser import HTMLParser
from urllib import request
import re
import time
from config import config
import mysql.connector 


conn = mysql.connector.connect(host=config['host'],user=config['user'], password=config['password'], database=config['database'])
cursor = conn.cursor()
cursor.execute('SET NAMES utf8mb4;')

class MyHTMLParser(HTMLParser):
    def init(self):
        self.__dataList=[]  
        self.__limit_tr,self.__limit_td= False,0
        self.__tr_2,self.__tr_3,self.__tr_6 = '','',''

    def get_data(self):
        return self.__dataList

    def handle_starttag(self, tag, attrs):

        if tag=='tr':
            for attr in attrs:
                if attr[0] == 'class':
                    self.__limit_tr = True

        if tag == 'td':
            if self.__limit_tr:
                self.__limit_td += 1
               
            

    def handle_endtag(self, tag):
        if tag == 'tr':
            self.__limit_tr,self.__limit_td= False,0
            self.__tr_2,self.__tr_3,self.__tr_6 = '','',''
        if tag == 'html':
            # print(self.__dataList)
            for data in self.__dataList:
                cursor.execute('insert into proxy (type,address) values (%s,%s)',[data[0],data[1]])
            conn.commit()
            # cursor.close()
            # conn.close()

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        if self.__limit_td == 2:
            if not re.match(r'^\n',data):
                self.__tr_2 = data
        elif self.__limit_td == 3:
            if not re.match(r'^\n',data):
                self.__tr_3 = data
        elif self.__limit_td == 6:
            if not re.match(r'^\n',data):
                self.__tr_6 = data
                self.__dataList.append([self.__tr_6,self.__tr_2+':'+self.__tr_3])
                self.__tr_2,self.__tr_3,self.__tr_6 = '','',''

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

parser = MyHTMLParser()
parser.init()

class ProxyAddress(object):
    def __init__(self):
        self.__address_list=[]
        self.__index=0
        self.__offset=0
        self.__limit=10
        self.__proxy_list=[]
        self.__filter_end=False
    def get_data(self):
        if len(self.__address_list)==0:
            cursor.execute('select type,address from proxy where status=1 order by id') 
            values = cursor.fetchall()
            for value in values:
                self.__address_list.append({value[0]:value[1]})
        return self.__address_list[self.__index]
    def next(self):
        if self.__index == len(self.__address_list)-1:
            print('代理地址用完了')
            self.__index=0
            return False
        else:
            self.__index += 1
            print('由%s切换至%s' %(self.__address_list[self.__index-1],self.__address_list[self.__index]))
            return True
    
    def get_init_data(self):
        time.sleep(5)
        req=request.Request('https://www.xicidaili.com/wn/')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        with request.urlopen(req) as f:
            data=f.read()
            # print('data:', data.decode('utf-8'))
            parser.feed(data.decode('utf-8'))
            # self.__address_list = parser.get_data()

    def filter(self):
        print('开始过滤现存数据...')
        while True:
            cursor.execute('select id,type,address from proxy where status is not null order by id limit %s offset %s ',(self.__limit,self.__offset))   
            self.__proxy_list = cursor.fetchall()
            if len(self.__proxy_list)<10:
                self.__filter_end=True
            for item in self.__proxy_list:
                time.sleep(1)
                try:
                    ProxyHandler = request.ProxyHandler({item[1]:item[2]})
                    Opener = request.build_opener(ProxyHandler)
                    request.install_opener(Opener)
                    req=request.Request('https://www.douban.com/group/changsha/members?start=0')
                    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
                    # req.add_header('Cookie','ll="118267"; bid=2Gkun4aXaEg; __utma=30149280.325389959.1576659520.1576659520.1576659520.1; __utmc=30149280; __utmz=30149280.1576659520.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1576659543%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F45453613%2F%22%5D; _pk_id.100001.3ac3=dc97f5b5f0771093.1576659543.1.1576659543.1576659543.; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utmb=30149280.2.10.1576659520; __utma=81379588.2124264048.1576659543.1576659543.1576659543.1; __utmc=81379588; __utmz=81379588.1576659543.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/45453613/; __utmb=81379588.1.10.1576659543')
                    with request.urlopen(req,timeout=10) as f:
                        if f.code == 200:
                            print('Success:%s' % item[1]+':'+item[2] )
                            cursor.execute('update proxy set status=1 where id =%s',(item[0],))
                except BaseException as e:
                    print('Error:%s|%s' %(item[1]+':'+item[2],e))
                    cursor.execute('update proxy set status=0  where id =%s',(item[0],))
            if self.__filter_end:
                print('现存数据过滤完毕')
                conn.commit()
                # cursor.close()
                # conn.close()
                break
            else:
                self.__offset+=10
        
        print('开始过滤新增数据...')
        self.__filter_end=False
        self.__offset=0
        while True:
            cursor.execute('select id,type,address from proxy where status is null limit %s offset %s',(self.__limit,self.__offset))   
            self.__proxy_list = cursor.fetchall()
            if len(self.__proxy_list)<10:
                self.__filter_end=True
            for item in self.__proxy_list:
                time.sleep(1)
                try:
                    ProxyHandler = request.ProxyHandler({item[1]:item[2]})
                    Opener = request.build_opener(ProxyHandler)
                    request.install_opener(Opener)
                    req=request.Request('https://www.douban.com/group/changsha/members?start=0')
                    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
                    # req.add_header('Cookie','ll="118267"; bid=2Gkun4aXaEg; __utma=30149280.325389959.1576659520.1576659520.1576659520.1; __utmc=30149280; __utmz=30149280.1576659520.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1576659543%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F45453613%2F%22%5D; _pk_id.100001.3ac3=dc97f5b5f0771093.1576659543.1.1576659543.1576659543.; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utmb=30149280.2.10.1576659520; __utma=81379588.2124264048.1576659543.1576659543.1576659543.1; __utmc=81379588; __utmz=81379588.1576659543.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/45453613/; __utmb=81379588.1.10.1576659543')
                    with request.urlopen(req,timeout=10) as f:
                        if f.code == 200:
                            print('Success:%s' % item[1]+':'+item[2] )
                            cursor.execute('update proxy set status=1 where id =%s',(item[0],))
                except BaseException as e:
                    print('Error:%s|%s' %(item[1]+':'+item[2],e))
                    cursor.execute('update proxy set status=0  where id =%s',(item[0],))
            if self.__filter_end:
                print('新增数据过滤完毕')
                cursor.execute('delete from proxy where status=0')
                conn.commit()
                # cursor.close()
                # conn.close()
                break

test= ProxyAddress()
# test.get_init_data()
test.filter()

# 手动写入
# data=[{
# 	"HTTP": "115.211.228.92:9999"
# }, {
# 	"HTTP": "219.159.38.197:56210"
# }, {
# 	"HTTP": "47.107.175.190:8000"
# }, {
# 	"HTTP": "183.146.157.54:9999"
# }, {
# 	"HTTP": "163.204.242.181:9999"
# }, {
# 	"HTTP": "125.92.100.51:9999"
# }, {
# 	"HTTP": "113.195.17.125:9999"
# }, {
# 	"HTTP": "117.94.183.214:9999"
# }, {
# 	"HTTP": "115.211.229.240:9999"
# }, {
# 	"HTTP": "118.25.13.185:8118"
# }, {
# 	"HTTP": "106.85.128.2:9999"
# }, {
# 	"HTTP": "120.79.193.230:8000"
# }, {
# 	"HTTP": "118.24.246.249:80"
# }, {
# 	"HTTP": "171.35.168.68:9999"
# }, {
# 	"HTTP": "183.154.49.62:9999"
# }]
# for item in data:
#     for key,value in item.items():
#         cursor.execute('insert into proxy (type,address) values (%s,%s)',[key,value])
# conn.commit()
# cursor.close()
# conn.close()