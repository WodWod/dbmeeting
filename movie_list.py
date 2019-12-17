# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib import request
import re
import time

class MyHTMLParser(HTMLParser):
    
    def isEnd(self):
        return self.isEndPage

    def handle_starttag(self, tag, attrs):
        # print('<%s>' % tag)
        limit_a=False
        limit_span=False
        limit_p=False
        
        if(tag=='li' and str(attrs).find('is-user') !=-1):
            self.isEndPage=False


        if(tag=='a'): 
            for attr in attrs:
                if(attr[0]=='href'and re.match(r'^/biyou/user',attr[1])):
                    limit_a=True
                elif(attr[0]=='class'):
                    limit_a=False    
        if(tag=='span'):
            for attr in attrs:
                if(attr[0]=='class'and re.match(r'^item',attr[1])):
                    limit_span=True  
                elif(attr[0]=='class'and re.match(r'str',attr[1])):
                    limit_p=False          
    
        self.limit_a,self.limit_span,self.limit_p=limit_a,limit_span,limit_p
                    

    def handle_endtag(self, tag):
        pass
        # print('</%s>' % tag)

    def handle_startendtag(self, tag, attrs):
        pass
        # print('<%s/>' % tag)

    def handle_data(self, data):
        # pass
        if(self.limit_a):
            print('用户名:%s'% data)
        elif(self.limit_span):
            print('信息:%s'% data)
        elif(self.limit_p):
            print('签名:%s'% data)
        
        self.limit_a,self.limit_span,self.limit_p=False,False,False


    def handle_comment(self, data):
        pass
        # print('<!--', data, '-->')

    def handle_entityref(self, name):
        pass
        # print('&%s;' % name)

    def handle_charref(self, name):
        pass
        # print('&#%s;' % name

parser = MyHTMLParser()

class Movie_List(object):
    def __init__(self,href):
        self.__href=href
    def write_data(self):
        for x in range(0,1000):
            time.sleep(2)
            with request.urlopen(self.__href+'?start=%s&sort=time&rating=all&filter=all&mode=grid' % str(x*15)) as f:
                data=f.read()
                parser.feed(data.decode('utf-8'))
                if(parser.isEnd()):
                    print('最后一页:%s' % x)
                    break
                # print('Data:', data.decode('utf-8'))


