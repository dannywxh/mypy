#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys

from bs4 import BeautifulSoup

import common

import requests

reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()

def download_html(url):
    
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, compress',
        'Accept-Language': 'en-us;q=0.5,en;q=0.3',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
    
    print "download from "+url+"\n"
    response = requests.get(url=url,headers=headers,timeout=5)    # 最基本的GET请求
    
    #print "status_code",response.status_code
    
    if response.ok:
        #print response.content.encode("gbk")
        #return StringIO.StringIO(response.content)
        data=response.content
        
        return data  
    
    
#####以下处理 avso ，可以封装成一个类  #################
      

           
def get_cast_onepage_by_avso(cast_name,pagecount=1):
 
    url=r'https://avso.pw/cn/search/'+cast_name+'/page/'+str(pagecount) 
    data=download_html(url)
  
    if data:
        #print response.content.encode("gbk")
          
        soup = BeautifulSoup(data,"html.parser")
        
        ret=[]
        
        try:
            
            notfound=soup.find('div',clasas_="alert alert-danger")
            if notfound!=None:
                print "Not Found!"
                return -1
            
            divs=soup.find_all('div',class_="item")
            
            if divs==None:
                print "divs is None!"
                return
            
            
            for div in divs:
                info=div.find('div',class_="photo-info")

                name=div.find('span')
                #print name.text
                                 
                datas=info.find_all('date')
                ret.append((name.text,datas[0].text,datas[1].text))
                
            return ret    
        except Exception,e:
            print e
            return -1
            #print "vcast not found!"

                        
   
def get_cast_allpage_by_avso(cast_name): 
    all_info=[]
    for i in range(1,10):
        info= get_cast_onepage_by_avso(cast_name,i)
        if info==-1:
            break
        else:
            all_info+=info
    
    print all_info
    
    savefile="d:\\"+cast_name+".txt"  
    with open(savefile,"w") as fs:
        for name,vid,date in all_info:
            fs.write(name.encode("utf-8")+"\t"+vid+"\t"+date+"\n")

    print "file create done!"         


# step:1 
def serch_movie_byvid(vid):
     
    url='https://avso.pw/cn/search/'+vid
    
    #url='https://avso.pw/cn/search/'+vid #110615_185'
    
    
    data=download_html(url)
  
    if data:
        #print response.content.encode("gbk")
          
        soup = BeautifulSoup(data,"lxml")
        
        ret=[]
        
        try:
            
            notfound=soup.find('div',class_="alert alert-danger")
            if notfound!=None:
                print "Not Found!"
                return -1

            types = soup.select('div.item > a')
            items = soup.select('div.item > a > div.photo-info > span')

            for a,item in zip(types,items):
                #print a['class'][1],a['href'],item.get_text() # ['movie-box', 'mcaribbeancom']
                cast=get_movie_cast(a['href'])
                ret.append((item.get_text(),cast,a['class'][1]))

            return ret
        except Exception,e:
            print e
            return -1
            #print "vcast not found!"

#step 2:得到片子的所有演员名
def get_movie_cast(url):
 
    # url=r'  https://avso.pw/cn/movie/yus'
    data=download_html(url)
     
    ret=[]
    if data:
        soup = BeautifulSoup(data,"lxml")
        
        try:
            
            notfound=soup.find('div',clasas_="alert alert-danger")
            if notfound!=None:
                print "Not Found!"
                return -1
            
            actress=soup.find_all('a',class_="avatar-box")
            
            for a in actress:
                span=a.find("span")
                ret.append(span.text)
 
            return " ".join(ret)    
        except Exception,e:
            print e
            return -1
            #print "vcast not found!"      
            
            


#wrapper function
def get_vidlist_full_info():
    
    #idlist=['082516-001','080117_01','062717_110']
    
    idlist= walkpath(r"e:\\avstore")
    print idlist
    
    infos=[]
    for id in idlist:
        info = serch_movie_byvid(id)
        if info!=-1:
            infos+=info

    #print infos

    infofile='d:\\info.txt'        
    with open(infofile,"w") as f:
        for a,b,c in infos:
            print a,b,c
    
            f.write(a+","+b+","+c+"\n")

    print "File saved!%s"%infofile       

def walkpath(path):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            p,f=os.path.split(line)
            id=common.format_rule1(f.replace("\n",""))
            if id!="":
                #store.append((id,txtfile))
                store.append(id)

    return store  



if __name__ == '__main__' :
    #TXT_STORE_PATH="d:\\avstore\\"
    
    get_vidlist_full_info()

    # idlist=['082516-001','080117_01','062717_110']
    #ret=serch_movie_byvid('082516-001')
    #for a,b,c in ret:
    #    print a,b,c
