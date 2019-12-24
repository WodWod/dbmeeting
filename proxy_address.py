# -*- coding: utf-8 -*-
#代理地址 https://www.xicidaili.com/nn/1
from html.parser import HTMLParser
from urllib import request
import re
import time

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
            pass


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
                self.__dataList.append({self.__tr_6:self.__tr_2+':'+self.__tr_3})
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
    def get_data(self):
        return self.__address_list[self.__index]
    def next(self):
        if self.__index == len(self.__address_list)-1:
            # self.__index = 0
            # print('由%s切换至%s' %(self.__address_list[self.__index],self.__address_list[0]))
            self.get_init_data()
            self.__index=0
            print('代理地址已重置')
        else:
            self.__index += 1
            print('由%s切换至%s' %(self.__address_list[self.__index-1],self.__address_list[self.__index]))
    
    def get_init_data(self):
        time.sleep(5)
        req=request.Request('https://www.xicidaili.com/nn/1')
        req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36')
        with request.urlopen(req) as f:
            data=f.read()
            # print('data:', data.decode('utf-8'))
            parser.feed(data.decode('utf-8'))
            self.__address_list = parser.get_data()

# test= ProxyAddress()
# test.get_init_data()
# print(test.get_data())