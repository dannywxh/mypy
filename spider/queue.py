#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import threading
import time
from bs4 import BeautifulSoup
import requests



g_mutex=threading.Condition()
g_pages=[] #从中解析所有url链接

queue = Queue.Queue()
out_queue = Queue.Queue()

class ThreadUrl(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, queue, out_queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.out_queue = out_queue

    def getContent(self, url):

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, compress',
                   'Accept-Language': 'en-us;q=0.5,en;q=0.3',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "get content from " + url + "\n"

        try:

            response = requests.get(url=url, headers=headers, timeout=5)  # 最基本的GET请求

            if response.ok:
                # print response.content.encode("gbk")
                # return StringIO.StringIO(response.content)
                return response.content
            else:
                return None
        except Exception,e:
            print e
            return None

    def test(self,data):
        time.sleep(0.1)
        return data

    def run(self):
        while True:
            #grabs host from queue
            host = self.queue.get()

            #grabs urls of hosts and then grabs chunk of webpage
            chunk=self.getContent(host)
            #chunk = self.test(host)

            #place chunk into out queue
            if chunk!=None:
                self.out_queue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()

class ParseThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue):
        threading.Thread.__init__(self)
        self.out_queue = out_queue

    def parseContent(self,data):
        urls=[]
        soup = BeautifulSoup(data, "lxml")

        #links=soup.select("#ajaxtable > tbody > tr > td.tal > h3 > a")
        # thread_7247690 > a
        links = soup.select("table#forum_230 > tbody > tr > th > span > a")

        # thread_7247595 > a
        for x in links:
           urls.append((x.getText(),x['href']));

        return urls

    def run(self):
        global g_pages
        while True:
            #grabs host from queue
            chunk = self.out_queue.get()

            #parse the chunk
            links=self.parseContent(chunk)

            #g_mutex.acquire()
            g_pages +=links
            #g_mutex.release()

            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()

def main():


    #populate queue with data
    #for host in hosts:
    #    queue.put(host)
    #urlb="http://ns.ddder.us/thread0806.php?fid=7&search=&page="

    urlb = "http://174.127.195.166/forum/forum-230-"

    for i in range(10):
        queue.put(urlb+str(i+1)+".html")

    #spawn a pool of threads, and pass them queue instance
    for i in range(5):
        t = ThreadUrl(queue, out_queue)
        t.setDaemon(True)
        t.start()


    for i in range(3):
        dt = ParseThread(out_queue)
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed

    out_queue.join()
    queue.join()  #阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。



hosts = ["http://yahoo.com", "http://baidu.com", "http://amazon.com",
         "http://ibm.com", "http://apple.com"]

main()

print "Elapsed Time: %s" % (time.time() - start)

print g_pages
print len(g_pages)


with open("d:\\cl_index.txt", 'w')as f:
     for b,a in g_pages:
         f.write(a+","+b.encode('utf-8')+"\n")
print "done!"

