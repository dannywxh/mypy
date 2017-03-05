#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys

import requests

from bs4 import BeautifulSoup

 
def getav(pgcount):
    baseurl= "http://www.jav11b.com/cn/"
    url=baseurl+"vl_update.php?&mode="
    url=url+"&page="+str(pgcount)

    print "start parse "+url+"\n"
    
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    r = requests.get(url=url,headers=headers,timeout=5)    # 最基本的GET请求

    #print(r.text.encode("utf-8"))   
    html=r.content   ##字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩centent避免乱码
    
    #print html

    soup = BeautifulSoup(html,"html.parser")

    divs=soup.find_all('div',class_='video')

    #print divs
    res=[]
    for div in divs:
        a=div.find('a',class_="")
        img=a.find('img')

        res.append((a.get("title"),a.get("href").replace("./?",baseurl+"?"),img.get("src")))

    return res


def getavs(pgcount):
    all_res=[]
    for i in range(1,pgcount):
        all_res+=getav(i)

    print all_res

    with open("c:\\1.txt","w") as f:
        for x,y,z in all_res:
            fn,ext=os.path.splitext(z)
            if fn[-2:]=='ps':
                pl_url=fn[:-2]+'pl'+ext
            f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+'\t'+pl_url.encode("utf8")+"\n")



if __name__ == '__main__' :
        getavs(10)