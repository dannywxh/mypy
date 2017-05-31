#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import random
import requests
import threading
import Queue
import StringIO
from bs4 import BeautifulSoup

import common

reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()



class getUrlThread(threading.Thread):
    def __init__(self,url,sid,queue):
        threading.Thread.__init__(self)
        self.sid=sid
        self.queue=queue

        self.url=url
      
    def download(self,url):

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "download from "+url+"\n"
        response = requests.get(url=self.url,headers=headers,timeout=5)    # 最基本的GET请求

        #print "status_code",response.status_code

        if response.ok:
            #print response.content.encode("gbk")
            #return StringIO.StringIO(response.content)
            return response.content


    def run(self):
        data=self.download(self.url)
        self.queue.put((self.sid,data))

class downloadThread(threading.Thread):
    def __init__(self,sid,queue_url):
        threading.Thread.__init__(self)
        self.sid=sid
        self.queue_url=queue_url


    def downfile(self,url):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "start download...",url
        r=requests.get(url,headers=headers,timeout=5,stream=True)

        print "status-code:",r.status_code

        filename=url.split('/')[-1].strip().replace("?","")
        #filename+=str(random.random());
        
        try:
            with open(filename,'wb')as f:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
                        f.flush()
                print filename,"download ok!"
        except Exception,e:
            print e.message


    def run(self):
        time.sleep(1)  #休眠1s一下
        while True:
            if not self.queue_url.empty():
                url=self.queue_url.get()
                if url:
                    print "queue size:",self.queue_url.qsize()
                    self.downfile(url)
                    #print('-----%s------'%(self.name))  
                    #os.system('wget '+url))  
            else:
                break
                
                
class parseThread(threading.Thread):
    def __init__(self,in_queue,out_list,mtype="jav"):
        threading.Thread.__init__(self)
        self.in_queue=in_queue
        self.out_list=out_list
        self.type=type

    def parseHTML(self,data): #for jav parse
        soup = BeautifulSoup(data,"html.parser")

        divs=soup.find_all('div',class_='video')

        #print divs
        res=[]
        for div in divs:
            a=div.find('a',class_="")
            img=a.find('img')
            res.append((a.get("title"),a.get("href"),img.get("src")))

        #print res
        return res


    def parseHTML_jav_detail(self,data):
        soup = BeautifulSoup(data,"html.parser")

        title=soup.title.string
        
        try:
            div=soup.find('div',{"id":'video_info'})
            div_cast=div.find('div',{"id":'video_cast'})
            a=div_cast.find('a');
            vcast=a.string
        except:
            print "vcast not found!"
            vcast=""
        
        try:
            div=soup.find('div',{"id":'video_date'})
            td_date=div.find('td',class_="text")
            vdate=td_date.string
        except:
            print "vdate not found!"
            vdate=""   

        try:
            div=soup.find('div',{"id":'video_review'})
            span=div.find('span',class_="score") 
            score=span.string
        except:
            print "score not found!"
            score=""

        try:
            #print title,cast,vdate,score
            return u'%s\t%s\t%s\t%s'%(title,vcast,vdate,score)
            #return title+"\t"+cast+"\t"+vdate+"\t"+score
        except:
            print "encode error!"
        return "error"


    def parseHTML2(self,data):
        soup = BeautifulSoup(data,"html.parser")

        divs=soup.find_all('a')

        #print divs
        res=[]
        res.append(soup.title.string )
        for a in divs:
            #res.append((a.string,a['href']))
            res.append(a['href'])

        #print res
        return res

    def parseHTML_btbt(self,data):
        soup = BeautifulSoup(data,"html.parser")

        divs=soup.find_all('a',class_='subject_link')

        #print divs
        res=[]
       
        for a in divs:
            #res.append((a.string,a['href']))
            res.append((a.get_text(),a['href']))

        #print res
        return res

    def parseHTML_cl(self,data):
        soup = BeautifulSoup(data,"html.parser")

        #table=soup.find('table',id='ajaxtable')
        tds=soup.find_all('td',class_='tal')

        #print divs
        res=[]
       
        for td in tds:
            a=td.find('a')
            #res.append((a.string,a['href']))
            res.append((a.get_text(),a['href']))

        #print res
        return res

    def parseHTML_cl_detail(self,data):
        soup = BeautifulSoup(data,"html.parser")

        title=soup.title.string
          
        
        div=soup.find('div',class_='tpc_content do_not_catch') #tpc_content do_not_catch
        
        #print div 
        #print divs
        res=[]
       
        img=div.find('img')
        a=div.find('a')
         
        res.append((title,a.get_text(),img['src']))

        return res

      
                                      
    def run2(self):
        while True:
            sid,data=self.in_queue.get()
            if sid==-1:
                break
            if data:
                res=self.parseHTML2(data)
                
                for x,y,z in res:
                    #self.out_queue.put(y.replace("./","http://www.jav11b.com/cn/"))
                    self.out_list.append((x,y,z)) 

    def run(self):
        while True:
            sid,data=self.in_queue.get()
            if sid==-1:
                break
            if data:
                if self.mtype=='jav':
                    print "parse by jav!\n"
                    res=self.parseHTML(data)
                    for x,y,z in res:
                        self.out_list.append((x,y))
                elif self.mtype=='jav_detail':
                    #print "parse by jav_detail\n"
                    x=self.parseHTML_jav_detail(data)
                    self.out_list.append(x)
                elif self.mtype=='cl':
                    print "parse by cl!\n"
                    res=self.parseHTML_cl(data)
                    for x,y in res:
                        self.out_list.append((x,y))
                else:
                    res=self.parseHTML(data)
                    for x,y,z in res:
                        self.out_list.append((x,y))


                        
                        
    def run_test(self):
        pass
        #self.downfile("http://10.166.2.206/tool/qd/VCruntimes.zip")



   
## class end ############################


def down_jav():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

 
    url="http://www.jav11b.com/cn/vl_update.php?&mode=&page="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,4)]

    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!等待geturl Thread 完成
    for t in uts:
        t.join()

    #通知pt退出
    q.put((-1,None))

    #!等待parse Thread 完成    
    pt.join()
    
    print "size of urls:",len(urls)

                     
    urlfile="c:\\javurls.txt"                 
    with open(urlfile,"w") as f:
        for x,y,z in  urls:
            #y=y.replace("./?",baseurl+"?")
            q_urls.put(z)   
            f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+"\n")
      
    print "File saved!",urlfile

    print "size of q_urls:",q_urls.qsize()

                                          
    print "##############################################"
    
    #开启下载文件线程 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,11)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()


    print "All files download complete!"


def down_btbt():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    url="http://localhost:8080/KManage/btbt.html?id="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,4)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!等待geturl Thread 完成
    for t in uts:
        t.join()

    #通知pt退出
    q.put((-1,None))

    #!等待parse Thread 完成    
    pt.join()
    
    print "size of urls:",len(urls)
                     
    urlfile="c:\\btbt.txt"                 
    with open(urlfile,"w") as f:
        for x,y in  urls:
            #y=y.replace("./?",baseurl+"?")
            q_urls.put(y)
            f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\n")
      
    print "url file saved!",urlfile

    print "size of q_urls:",q_urls.qsize()
                                          
    print "##############################################"

    
            
def down_cl():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    url="http://cl.o3c.me/thread0806.php?fid=15&search=&page="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,20)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!等待geturl Thread 完成
    for t in uts:
        t.join()

    #通知pt退出
    q.put((-1,None))

    #!等待parse Thread 完成    
    pt.join()
    
    print "size of urls:",len(urls)
                     
    urlfile="c:\\cl.txt"                 
    with open(urlfile,"w") as f:
        for x,y in  urls:
            q_urls.put(y)
            #y=y.replace("./?",baseurl+"?")
            f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\n")
      
    print "url file saved!",urlfile
 
    print "size of q_urls:",q_urls.qsize()
                                          
    print "##############################################"    
 
    #开启下载文件线程 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,5)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()


    print "All files download complete!"


#txt里未下完的部分
def down_cl_remainder(all_txt,downed_path):
    
    q_urls=Queue.Queue()

    downeds=[x for x in os.listdir(downed_path) if not os.path.isdir(downed_path+"\\"+x)]

    all_urls=[]
    #fullpath_files=[]
    for line in open(all_txt):
        url=line.split("\t")[1]
        p,f=os.path.split(url)
        
        all_urls.append(f.replace("\n",""))

            
    diff=set(all_urls)-set(downeds)

    for x in diff:
        q_urls.put("http://cl.o3c.me/htm_data/15/1703/"+x)

    print q_urls.qsize()


    #开启下载文件线程 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,3)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()

    print "Diff files download complete!"

#分析cl 打开的detail页面
def down_cl_detail():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    url="http://localhost:8080/KManage/cl_detail.html?id="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,4)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!等待geturl Thread 完成
    for t in uts:
        t.join()

    #通知pt退出
    q.put((-1,None))

    #!等待parse Thread 完成    
    pt.join()
    
    print "size of urls:",len(urls)
                     
    urlfile="c:\\cl_detail.txt"                 
    with open(urlfile,"w") as f:
        for x,y,z in  urls:
            q_urls.put(z)
            #y=y.replace("./?",baseurl+"?")
            f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+"\n")
      
    print "url file saved!",urlfile

    print "size of q_urls:",q_urls.qsize()
    
    print "##############################################"    
    

#比较两个list的差异部分
def comparelist_diff(src,des):
    #src: [("name_str","url")]
    #des: ["url"]  
    
    ret=[] 
    for x,y in src:
        flag=0
        for a in des:
            if y.replace("\n","")==a.replace("\n",""):
                flag=1
        if flag==0:
            ret.append((x,y)) 

    return ret    

#读取目录下的txt文件到list
def walkcl(path):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            url=line.split("\t")[1].replace("\n","")
            store.append(url)
    #print store        
    return store  
                               
#对比cl库文件,得到差集，并写入cl库                 
def cmp_cl_store(store_path,src):
    #src=[("a","c:\\"),("b","c:\\"),("c","c:\\"),("a","d:\\"),("b","e:\\"),("c","e:\\"),("a","c:\\")]    
    #des=["a","b","c"]

    des=walkcl(store_path)
   
    print "cl store total count=",len(des)

    diff=comparelist_diff(src,des)     
    
    if len(diff)==0:
        print "no found diff!"
        return 
  
    sdate=time.strftime('%Y-%m-%d',time.localtime(time.time()))
    savefile=store_path+"\\cl_"+sdate+ str(random.randint(10,100))+".txt"  
    with open(savefile,"w") as fs:
        for name,url in diff:
            fs.write(name.encode("utf-8")+"\t"+url.encode("utf-8")+"\n")

    print "Found %s url File saved!"%len(diff)
    
    return diff


#下载cl库里不存在的部分
def down_store_diff(type):
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    if type=='jav': 
        url="http://www.jav11b.com/cn/vl_update.php?&mode=&page="
        url_detail="http://www.jav11b.com/cn/"
        store_path="D:\\avstore\\jav_store\\"
    elif type=='cl':
        url="http://cl.o3c.me/thread0806.php?fid=15&search=&page="
        url_detail="http://cl.o3c.me/"
        store_path="D:\\avstore\\CL_STORE\\"

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,10)]
    
    for t in uts:
        t.start()

    pt=parseThread(q,urls,type)

    pt.start()

    #等待geturl Thread 完成
    for t in uts:
        t.join()

    #通知pt退出
    q.put((-1,None))

    #!等待parse Thread 完成    
    pt.join()


    print "For down urls=",len(urls)

    diff=cmp_cl_store(store_path,urls)

    if len(diff)>0: 
        for name,url in diff:
            q_urls.put(url_detail+url)

        print "q_urls size:",q_urls.qsize()

        #开启下载文件线程 
        
        dts=[downloadThread(i,q_urls) for i in xrange(1,3)]

        for t in dts:
            t.start()

        for t in dts:
            t.join()

        print "Diff files download complete!"
        
    
#应该使用线程池
def search_jav(val):
    q=Queue.Queue()  #存放requests获取的html data：self.queue.put((self.sid,data))
    
    out_urls=[] #存放解析好的结果

    url ="http://www.j12lib.com/cn/vl_searchbyid.php?keyword="+val

    ut=getUrlThread(url,1,q)  #输出q

    pt=parseThread(q,out_urls,'jav_detail') #输入q,输出out_urls

    #for t in uts:
    ut.start()

    pt.start()

    #!等待geturl Thread 完成
    ut.join()

    #通知pt退出
    q.put((-1,None))

    #!等待parse Thread 完成    
    pt.join()
    
    #print "size of urls:",len(out_urls)

    return out_urls
'''
    urlfile="d:\\javurls.txt"                 
    with open(urlfile,"w") as f:
         for x in  out_urls:
             f.write(x+"\n")      

    print "File saved!",urlfile
'''

#应该使用线程池
def search_jav1(slist):

    q=Queue.Queue()  #存放requests获取的html data：self.queue.put((self.sid,data))
    
    out=[] #存放解析好的结果
    url ="http://www.j12lib.com/cn/vl_searchbyid.php?keyword="
    uts=[]

    allinfo=[] 
    for i in range(len(slist)):
        print "------Add %s\n"%(url+slist[i])
        print "------Allinfo count %s\n"%(len(allinfo))
        uts.append(getUrlThread(url+slist[i],i,q))  #输出q
        out=[]
        if i%10==0:
            print "get start %s\n"%(i)
            pt=parseThread(q,out,'jav_detail') #输入q,输出out_urls

            for ut in uts:
                ut.start()

            pt.start()

            #!等待geturl Thread 完成
            ut.join()

            #通知pt退出
            q.put((-1,None))

            #!等待parse Thread 完成    
            pt.join()
            uts=[]
            allinfo+=out


    urlfile="d:\\javurls.txt"                 
    with open(urlfile,"w") as f:
        for x in  allinfo:
            f.write(x+"\n")      

    print "File saved!",urlfile
                           

def walkfile(path):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            p,f=os.path.split(line)
            vid=common.format_rule2(f.replace("\n",""))

            wm=re.findall(r'^\d+',vid)
            if len(wm)==0:  #不是wm
                store.append(vid)
    
    return store  


def search_jav_by_cast(cast,cname):
    
    res=[]
  
    baseurl="http://www.j12lib.com/cn/vl_star.php?&mode=&s="+cast+"&page="

    page=0 
    for i in xrange(1,10):
        url=baseurl+str(i)
        #print url
        
        response=common.download(url)
        if response.ok:
              
            soup = BeautifulSoup(response.content,"html.parser")
    
            divs=soup.find_all('div',class_='video')
    
            if divs==None or len(divs)==0:
                print "Total page=%s"%page
                break
            else:
                for div in divs:
                    a=div.find('a',class_="")
                    img=a.find('img')
                    res.append((a.get("title"),a.get("href"),img.get("src")))
                
                page+=1
    
    urlfile='d:\\'+cname+'.txt'                 
    with open(urlfile,"w") as f:
        for x,y,z in res:
            f.write(x+"\t"+y+"\t"+z+"\n")      

    print "File saved!%s"%urlfile            
  
    

if __name__ == '__main__' :
    TXT_STORE_PATH="d:\\avstore\\"
    #down_jav()
    #down_btbt()
    #down_cl()
    #down_cl_detail()

    #down_store_diff("cl")
    #down_store_diff("jav")

    #down_cl_remainder("d:\\cl.txt","d:\\dd")

    #st=walkfile(TXT_STORE_PATH)
    #search_jav(st)
    #vl_star.php?s=afark 三島奈津子
    #search_jav_by_cast('afark',r'三島奈津子'.decode("utf-8"))
    search_jav_by_cast('azoce',r'三好亚矢'.decode("utf-8"))


'''
    urlfile="d:\\javurls.txt"                 
    with open(urlfile,"w") as f:
         for x in  out_urls:
             f.write(x+"\n")      

'''