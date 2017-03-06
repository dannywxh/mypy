#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import requests
import threading
import Queue
import StringIO

from bs4 import BeautifulSoup


class downloadThread(threading.Thread):
    def __init__(self,sid,queue):
        threading.Thread.__init__(self)
        self.sid=sid
        self.queue=queue

        #self.url="http://10.166.7.151/docs/nutz1.56/index.html?id="+str(sid)
        self.url="http://www.jav11b.com/cn/vl_update.php?&mode=&page="+str(sid)

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



class dlsavefileThread(threading.Thread):
    def __init__(self,queue_url):
        threading.Thread.__init__(self)
        self.queue_url=queue_url


    def downfile(self,url):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "start dwonload...",url
        r=requests.get(url,headers=headers,stream=True)
        filename=url.split('/')[-1].strip().replace("?","")

        with open(filename,'wb')as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            print filename,"is ok!"

    def run(self):
        while True:
            if not self.queue_url.empty():
                url=self.queue_url.get()
                if url:
                    data=self.downfile(url)
                    #print('-----%s------'%(self.name))  
                    #os.system('wget '+url))  
            else:
                break
    

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

        print res
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

    def run(self):
        while True:
            sid,data=self.queue.get()
            if sid==-1:
                break
            if data:
                res=self.parseHTML(data)

                with open("c:\\"+str(sid)+".txt","w") as f:
                    for x,y,z in res:
                        #y=y.replace("./?",baseurl+"?")
                        f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+"\n")
                        self.out_queue.put(y.replace("./","http://www.jav11b.com/cn/"))


    def run_test(self):
        pass
        #self.downfile("http://10.166.2.206/tool/qd/VCruntimes.zip")



if __name__ == '__main__' :
    q=Queue.Queue()
    q_urls=Queue.Queue()

    dts=[downloadThread(i,q) for i in xrange(1,3)]

    ct=parseThread(q,q_urls)

    for t in dts:
        t.start()

    ct.start()

    for t in dts:
        t.join()

    #通知ct退出
    q.put((-1,None))

    #开启下载文件线程 
    
    dfts=[dlsavefileThread(q_urls) for i in xrange(1,11)]

    for t in dfts:
        t.start()


    for t in dfts:
        t.join()

    q_urls.put(-1)
    

    print "download file complete!"