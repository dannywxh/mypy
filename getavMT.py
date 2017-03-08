#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import random
import requests
import threading
import Queue
import StringIO

from bs4 import BeautifulSoup


reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('gbk')
print sys.getdefaultencoding()



class getUrlThread(threading.Thread):
    def __init__(self,sid,queue):
        threading.Thread.__init__(self)
        self.sid=sid
        self.queue=queue

        self.url="http://10.166.7.151/docs/nutz1.56/index.html?id="+str(sid)
        #self.url="http://www.jav11b.com/cn/vl_update.php?&mode=&page="+str(sid)

    def download(self,url):

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "download from "+url+"\n"
        response = requests.get(url=self.url,headers=headers,timeout=5)    # 最基本的GET请求

        if response.ok:
            #print response.content
            #return StringIO.StringIO(response.content)
            return response.content


    def run(self):
        data=self.download(self.url)
        self.queue.put((self.sid,data))


class parseThread(threading.Thread):
    def __init__(self,queue,out_queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.out_queue=out_queue

    def parseHTML(self,data):
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

    def run2(self):
        while True:
            sid,data=self.queue.get()
            if sid==-1:
                break
            if data:
                res=self.parseHTML2(data)
                
                for x,y,z in res:
                    self.out_queue.put(y.replace("./","http://www.jav11b.com/cn/"))
                    urls.append((x,y,z)) 

    def run(self):
        while True:
            sid,data=self.queue.get()
            if sid==-1:
                break
            if data:
                res=self.parseHTML2(data)

                for x in res:
                     self.out_queue.put("http://10.166.7.151/docs/nutz1.56/"+x)
                     urls.append(("aaa","bbb","http://10.166.7.151/docs/nutz1.56/"+x))
                        
                        
    def run_test(self):
        pass
        #self.downfile("http://10.166.2.206/tool/qd/VCruntimes.zip")


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
        r=requests.get(url,headers=headers,stream=True)
        filename=url.split('/')[-1].strip().replace("?","")
        
        filename+=str(random.random());
        

        with open(filename,'wb')as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            print filename,"download ok!"


    def run(self):
        time.sleep(3)  #休眠5s一下，否则太快取不到queue的数据就结束了
        while True:
            if not self.queue_url.empty():
                url=self.queue_url.get()
                if url:
                    self.downfile(url)
                    #print('-----%s------'%(self.name))  
                    #os.system('wget '+url))  
            else:
                break
    





if __name__ == '__main__' :
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    uts=[getUrlThread(i,q) for i in xrange(1,4)]

    pt=parseThread(q,q_urls)

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
    print "size of q_urls:",q_urls.qsize()

                     
    urlfile="c:\\javurls.txt"                 
    with open(urlfile,"w") as f:
         for x,y,z in  urls:
             #y=y.replace("./?",baseurl+"?")
             f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+"\n")
      
    print "url file saved!",urlfile
                                          
    print "##############################################"
    
    #开启下载文件线程 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,11)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()


    print "File download complete!"