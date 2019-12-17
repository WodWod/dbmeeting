# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib import request
import re
import time

class MyHTMLParser(HTMLParser):
    def init(self):
        self.limit_a=False
        self.limit_span=False
        self.limit_p=False
        self.isEndPage=True

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


for x in range(80,90):
    time.sleep(2)
    with request.urlopen('https://www.ai9475.com/biyou/search?&nickname=&gender=-1&age=0&province=430000&liveCity=430100&p='+ str(x)) as f:
        data=f.read()
        parser.init()
        parser.feed(data.decode('utf-8'))
        if(parser.isEnd()):
            print('最后一页:%s' % x)
            break
        # print('Data:', data.decode('utf-8'))

