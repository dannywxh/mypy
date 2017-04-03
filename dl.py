#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

from bs4 import BeautifulSoup
'''
功能：基于http的可目录浏览网站文件的递归下载

'''
#baseurl="http://10.166.7.151/docs/powerui2"
baseurl="http://10.166.7.151/docs/jquery-easyui-1.4.2"
   
def getpginfo(url,path):                  
       headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}


       response = requests.get(url=url,headers=headers,timeout=5)    # 最基本的GET请求

       ret= parse(response.content,path)
       #print ret

       for a,b,c in ret:
           if a=='[DIR]':
                print b
                getpginfo(url+"/"+b,path+b)
                #baseurl=url+"/"+b
           else:
                print baseurl+c+b
                downfile(baseurl+c+b,c)
                        
def parse(html,path):
        soup = BeautifulSoup(html,"html.parser")

        [s.extract() for s in soup.find_all('th')]
        
        soup = BeautifulSoup(soup.prettify(),"html.parser")
        
        trs=soup.find_all('tr')
        
        #print trs
        
        ret=[]
        for tr in trs:
            if tr.get_text()=="\n":
                continue
                
            tds=tr.find_all("td")
            
            #print tds

            x=''
            y=''  
            for td in tds:
                 img=td.find("img")
                 #print "img",img
                 
                 a=td.find("a")
                 #print "a",img
        
                 if img:
                     if img!=-1:
                        x=img.get("alt")
                 if a:
                     if a!=-1:
                         if a.get_text()!='Parent Directory':
                            y=a.get("href")
                        
            ret.append((x,y,path))
            
        return ret

def downfile(url,path):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "start download...",url
        r=requests.get(url,headers=headers,stream=True)
        filename=url.split('/')[-1].strip().replace("?","")
        
        filename=path.replace("/","-")+filename;
        

        with open(filename,'wb')as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            print filename,"download ok!"


if __name__ == '__main__' :    
  
    getpginfo(baseurl,"/")
    
    
                
