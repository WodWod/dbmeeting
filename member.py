# -*- coding: utf-8 -*-
from html.parser import HTMLParser
from urllib import request
import re
import time
from person import Person
from proxy_address import ProxyAddress
#浏览器头
from user_agent import Agent
agent= Agent()
# import mysql.connector 

# conn = mysql.connector.connect(user='root', password='123456', database='dbmeeting')
# cursor = conn.cursor()

#代理地址
address_list =  ProxyAddress()
# address_list.get_init_data()
# address_list.filter()

class MyHTMLParser(HTMLParser):
    def init(self):
        self.__isEndPage=True
    
    def isEnd(self):
        return self.__isEndPage

    def handle_starttag(self, tag, attrs):
        if(tag=='a'):
            if len(attrs) == 2 and str(attrs).find('nbg') != -1:
                for attr in attrs:
                    if attr[0]=='href' and re.match(r'^https://www.douban.com/people/',attr[1]): 
                        self.__isEndPage=False    
                        global person_list
                        person_list =  Person(attr[1])   
                        person_list.write_data()     

    def handle_endtag(self, tag):
        pass

    def handle_startendtag(self, tag, attrs):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_entityref(self, name):
        pass

    def handle_charref(self, name):
        pass

parser = MyHTMLParser()


class Member_List(object):
    def __init__(self,href):
        self.__href=href
        
    def write_data(self):
        print('开始抓取...')
        search_list = list(range(20,100))
        for x in search_list:
            try:
                time.sleep(5)
                ProxyHandler = request.ProxyHandler(address_list.get_data())
                Opener = request.build_opener(ProxyHandler)
                request.install_opener(Opener)
                req=request.Request(self.__href+'/members?start=%s' % str(x*35))
                req.add_header('User-Agent',agent.get_data())
                # req.add_header('Cookie','ll="118267"; bid=2Gkun4aXaEg; __utma=30149280.325389959.1576659520.1576659520.1576659520.1; __utmc=30149280; __utmz=30149280.1576659520.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1576659543%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F45453613%2F%22%5D; _pk_id.100001.3ac3=dc97f5b5f0771093.1576659543.1.1576659543.1576659543.; _pk_ses.100001.3ac3=*; __utmt_douban=1; __utmb=30149280.2.10.1576659520; __utma=81379588.2124264048.1576659543.1576659543.1576659543.1; __utmc=81379588; __utmz=81379588.1576659543.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/45453613/; __utmb=81379588.1.10.1576659543')
                with request.urlopen(req,timeout=10) as f:
                    parser.init()
                    data=f.read()
                    # print('data:', data.decode('utf-8'))
                    parser.feed(data.decode('utf-8'))
                    if(parser.isEnd() or x == search_list[-1]):
                        print('小组成员最后一页:%s' ,x*35)
                        person_list.close_link()
                        break
            except BaseException as e:
                print('Member Error:',e)  
                if address_list.next():
                    self.write_data()
                else:
                    break
                  
            finally:
                pass
        
                
test=Member_List('https://www.douban.com/group/changsha')
test.write_data()


