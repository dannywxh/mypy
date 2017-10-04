#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
from bs4 import BeautifulSoup
'''
功能：基于http的可目录浏览网站文件的递归下载

'''

reload(sys)
#print sys.getdefaultencoding()
#sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

def getpginfo(url):                  
       headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}


       response = requests.get(url=url,headers=headers,timeout=5)    # 最基本的GET请求

       ret= parse(response.content)
       #print ret

def parse_letv(html):
        soup = BeautifulSoup(html,"html.parser")

        #lis=soup.find_all('li', attrs={'k-name':'send-click-stat'})

        lis=soup.find_all('li')
 
        print lis
        
        ret=[]
        for li in lis:
            a=li.find("a")

            vid=a['data-vid']

            ret.append("http://www.le.com/ptv/vplay/"+vid+".html")

        return ret

#TLF ed2k
def parse1(html):
    soup = BeautifulSoup(html, "lxml")

    # lis=soup.find_all('li', attrs={'k-name':'send-click-stat'})

    lis = soup.find_all('input',attrs={"name": "em0"})

    print lis

    ret = []
    for a in lis:
        print a["value"]
        try:
            ret.append(a["value"])
        except Exception,e:
            print e

    with open("d:\\urls1.txt","w") as f:
        for x in ret:
            f.write(x.encode('utf8')+"\n")



def parse_bjjt(html):
    soup = BeautifulSoup(html, "lxml")
    lis = soup.select('div.text > a')
    print lis

    with open("d:\\urls_bjjt.txt","w") as f:
        for a in lis:
            f.write(a['href']+"\t"+a.get_text().encode('utf8')+"\n")


if __name__ == '__main__' :    
  
    #baseurl="chttp://www.le.com/ptv/vplay/20029893.html#vid=20029893"
    #getpginfo(baseurl)

    htmlfile = open("d:\\2.html", 'r')  #以只读的方式打开本地html文件
    html = htmlfile.read()

    ret=parse1(html)


    
