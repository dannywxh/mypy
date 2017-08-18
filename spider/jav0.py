#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import threading
import time
from bs4 import BeautifulSoup
import requests

import csv

import codecs


g_mutex=threading.Condition()
g_pages=[] #从中解析所有url链接

err_queue=Queue.Queue()



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

        global err_queue
        try:

            response = requests.get(url=url, headers=headers, timeout=10)  # 最基本的GET请求

            if response.ok:
                # print response.content.encode("gbk")
                # return StringIO.StringIO(response.content)
                return response.content
            else:
                print "response not ok"
                #g_mutex.acquire()
                #err_queue.put("response not ok")
                #g_mutex.release()

                return None
        except Exception,e:
            #g_mutex.acquire()
            #err_queue.put(e.message)
            #g_mutex.release()

            return None

    def test(self,data):
        time.sleep(0.1)
        return data

    def run(self):
        while True:
            #grabs host from queue
            url = self.queue.get()

            #grabs urls of hosts and then grabs chunk of webpage
            chunk=self.getContent(url)

            #place chunk into out queue
            if chunk!=None:
                self.out_queue.put(chunk)

            #signals to queue job is done
            self.queue.task_done()

class ParseThread(threading.Thread):
    """Threaded Url Grab"""
    def __init__(self, out_queue,type="index"):
        threading.Thread.__init__(self)
        self.out_queue = out_queue
        self.type=type

    def parseContent_index(self, data):

        soup = BeautifulSoup(data, "lxml")

        # links=soup.select("#ajaxtable > tbody > tr > td.tal > h3 > a")
        # thread_7247690 > a
        vids = soup.select("div.video > a")

        a=['http://www.ja14b.com/cn'+x['href'][1:] for x in vids]
        #print a

        return a

    def parseContent_detail(self,data):
        #print data

        soup = BeautifulSoup(data, "lxml")

        vimg=soup.select("div#video_jacket > img#video_jacket_img")
        vid = soup.select("div#video_info > div#video_id td.text")
        vdate=soup.select("div#video_info > div#video_date td.text")
        score=soup.select("div#video_review td.text > span.score")
        genres_list=soup.select("div#video_genres  td.text > span.genre > a")
        genres=""
        for a in genres_list:
            genres+=a.get_text()+" "

        genres_list=[]
        genres_list.append(genres.encode('gbk'))

        cast_list = soup.select("div#video_cast td.text > span.cast > span.star > a")
        vcast=""
        for a in cast_list:
            vcast += a.get_text() + " "
        cast_list=[]
        cast_list.append(vcast.encode('gbk'))

        wanted = soup.select("div#video_favorite_edit > span#subscribed > a")
        owned = soup.select("div#video_favorite_edit > span#owned > a")

        info=()
        for a_id,a_img,a_date,a_score,a_wanted,a_owned,cast,genres in zip(vid,vimg,vdate,score,wanted,owned,cast_list,genres_list):
            info= a_id.get_text(),a_date.get_text(),a_score.get_text(),a_wanted.get_text(),a_owned.get_text(),cast,genres,a_img['src']

        print "parse done!"
        return info

    def parseContent_test(self, data):
        # print data

        #soup = BeautifulSoup(data, "lxml")

        print data

        return data



    def run(self):
        global g_pages
        while True:
            #grabs host from queue
            chunk = self.out_queue.get()

            #parse the chunk
            if self.type=='index':
                links=self.parseContent_index(chunk)
            elif self.type=='detail':
                #links = self.parseContent_detail(chunk)
                links = self.parseContent_detail(chunk)

            #g_mutex.acquire()
            if type(links) is list:
                g_pages+=links
            else:
                g_pages.append(links)
            #g_mutex.release()

            #signals to queue job is done
            self.out_queue.task_done()

start = time.time()

def getindex():

    dic = {"doks232": ["2012-12-07", "7.80", "1,2,3", "a,b,c"],
           "doks233": ["2012-12-08", "7.90", "1,2,3", "a,b,c"]
           }

    print dic["doks232"]
    #populate queue with data
    #for host in hosts:
    #    queue.put(host)
    #urlb="http://ns.ddder.us/thread0806.php?fid=7&search=&page="

    #urlb = "http://www.ja14b.com/cn/?v=javlior2ti"
    #urlb = "http://www.ja14b.com/cn/"
    urlb="http://www.ja14b.com/cn/vl_update.php?&mode=&page="

    queue = Queue.Queue()
    out_queue = Queue.Queue()

    for i in range(30):
        queue.put(urlb+str(i+1))

    #spawn a pool of threads, and pass them queue instance
    for i in range(20):
        t = ThreadUrl(queue, out_queue)
        t.setDaemon(True)
        t.start()


    for i in range(1):
        dt = ParseThread(out_queue,'index')
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed



    queue.join()  #阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。

    getdetail()

    out_queue.join()


    with open('d:\\jav_info.txt', 'wb') as f:
        m = len(g_pages)
        for i in range(m):
            f.write(g_pages[i]+"\n")

    print "getIndex done!"




def getdetail():
    queue = Queue.Queue()
    out_queue = Queue.Queue()

    global g_pages
    #g_pages = list(set(g_pages)) #清除重复记录

    for i in range(len(g_pages)):
        queue.put(g_pages[i])

    g_pages=[]

    #spawn a pool of threads, and pass them queue instance
    for i in range(10):
        t = ThreadUrl(queue, out_queue)
        t.setDaemon(True)
        t.start()


    for i in range(2):
        dt = ParseThread(out_queue,'detail')
        dt.setDaemon(True)
        dt.start()

    #wait on the queue until everything has been processed

    queue.join()  #阻塞，直到queue中的数据均被删除或者处理。为队列中的每一项都调用一次。
    out_queue.join()

    print "getDetail done!"

    with open('d:\\jav_info.csv', 'wb') as f:
        writer = csv.writer(f)
        m = len(g_pages)
        for i in range(m):
            writer.writerow(g_pages[i])

getindex()

print len(g_pages)

#raw_input()

#getdetail()


print "Elapsed Time: %s" % (time.time() - start)

g_pages = list(set(g_pages)) #清除重复记录
print len(g_pages)
print g_pages






