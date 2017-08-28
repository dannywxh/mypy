#!/usr/bin/env python
# -*- coding:utf-8 -*-

# 使用了线程库
import threading
# 队列
from Queue import Queue
# 解析库
from lxml import etree

from bs4 import BeautifulSoup
# 请求处理
import requests
# json处理
import json
import time

import sys

from common import format_rule2

reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')


class ThreadCrawl(threading.Thread):
    def __init__(self, threadName, pageQueue, dataQueue):
        #threading.Thread.__init__(self)
        # 调用父类初始化方法
        super(ThreadCrawl, self).__init__()
        # 线程名
        self.threadName = threadName
        # 页码队列
        self.pageQueue = pageQueue
        # 数据队列
        self.dataQueue = dataQueue
        # 请求报头
        self.headers = {"User-Agent" : "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def run(self):
        print "启动 " + self.threadName
        while not CRAWL_EXIT:
            try:
                # 取出一个数字，先进先出
                # 可选参数block，默认值为True
                #1. 如果对列为空，block为True的话，不会结束，会进入阻塞状态，直到队列有新的数据
                #2. 如果队列为空，block为False的话，就弹出一个Queue.empty()异常，
                url = self.pageQueue.get(False)
                content = requests.get(url, headers = self.headers).text
                time.sleep(1)
                self.dataQueue.put(content)
                #print len(content)
            except Exception as e:
                print "page queue empty!"+e.message

        print "结束 " + self.threadName

class ThreadParse(threading.Thread):
    def __init__(self, threadName, dataQueue, parseType,filename, lock):
        super(ThreadParse, self).__init__()
        # 线程名
        self.threadName = threadName
        # 数据队列
        self.dataQueue = dataQueue
        # 解析类型
        self.parseType=parseType
        # 保存解析后数据的文件名
        self.filename = filename
        # 锁
        self.lock = lock

    def run(self):
        print "启动" + self.threadName

        while not PARSE_EXIT:
            try:
                html = self.dataQueue.get(False)

                if  self.parseType=='jav_index':
                    self.parse(html)
                elif self.parseType=='jav_detail':
                    self.parse_detail(html)
            except:
                pass
        print "退出" + self.threadName

    def parse(self, html):
        # 解析为HTML DOM
        soup = BeautifulSoup(html, "lxml")

        vurls = soup.select("div.video > a")
        vids = soup.select("div.video > a > div.id")

        links = ['http://www.ja14b.com/cn' + x['href'][1:] for x in vurls]
        for vid, link in zip(vids, links):
            items = {
                    "url" : link,
                    "vid" : format_rule2(vid.get_text())
                }

            # with 后面有两个必须执行的操作：__enter__ 和 _exit__
            # 不管里面的操作结果如何，都会执行打开、关闭
            # 打开锁、处理内容、释放锁
            with self.lock:
                # 写入存储的解析后的数据
                self.filename.write(json.dumps(items, ensure_ascii = False).encode("utf-8") + "\n")

    def parse_detail(self, html):
        # 解析为HTML DOM
        soup = BeautifulSoup(html, "lxml")

        vimg = soup.select("div#video_jacket > img#video_jacket_img")
        vid = soup.select("div#video_info > div#video_id td.text")
        vdate = soup.select("div#video_info > div#video_date td.text")
        score = soup.select("div#video_review td.text > span.score")
        genres_list = soup.select("div#video_genres  td.text > span.genre > a")
        genres = ""
        for a in genres_list:
            genres += a.get_text().encode('utf-8') + " "

        genres_list = []
        genres_list.append(genres)

        cast_list = soup.select("div#video_cast td.text > span.cast > span.star > a")
        vcast = ""
        for a in cast_list:
            vcast += a.get_text().encode('utf-8') + " "
        cast_list = []
        cast_list.append(vcast)

        wanted = soup.select("div#video_favorite_edit > span#subscribed > a")
        owned = soup.select("div#video_favorite_edit > span#owned > a")

        for a_id, a_img, a_date, a_score, a_wanted, a_owned, cast, genres in zip(vid, vimg, vdate, score, wanted, owned,
                                                                                 cast_list, genres_list):


            items = {
                     "vid":a_id.get_text(),
                     "vimg":a_img['src'],
                     "vdate":a_date.get_text(),
                     "score": a_score.get_text(),
                     "wanted": a_wanted.get_text(),
                     "owned": a_owned.get_text(),
                     "casts": cast,
                     "genress": genres
                }

            print  items
                # with 后面有两个必须执行的操作：__enter__ 和 _exit__
                # 不管里面的操作结果如何，都会执行打开、关闭
                # 打开锁、处理内容、释放锁
            with self.lock:
                # 写入存储的解析后的数据
                try:
                    self.filename.write(json.dumps(items, ensure_ascii = False).encode("utf-8") + "\n")
                except Exception as e:
                    print e.message


CRAWL_EXIT = False
PARSE_EXIT = False


def main():
    url = "http://www.ja14b.com/cn/vl_update.php?&mode=&page="
    # 页码的队列，表示20个页面
    pageQueue = Queue(20)
    # 放入1~10的数字，先进先出
    for i in range(1, 21):
        pageQueue.put(url+str(i))

    # 采集结果(每页的HTML源码)的数据队列，参数为空表示不限制
    dataQueue = Queue()

    filename = open("duanzi.json", "a")
    # 创建锁
    lock = threading.Lock()

    # 三个采集线程的名字
    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号"]
    # 存储三个采集线程的列表集合
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)


    # 三个解析线程的名字
    parseList = ["解析线程1号","解析线程2号","解析线程3号"]
    # 存储三个解析线程
    threadparse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue,'jav_index',filename, lock)
        thread.start()
        threadparse.append(thread)

    # 等待pageQueue队列为空，也就是等待之前的操作执行完毕
    while not pageQueue.empty():
        pass

    # 如果pageQueue为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True

    print "pageQueue为空"

    for thread in threadcrawl:
        thread.join()
        print "1"

    while not dataQueue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT = True

    for thread in threadparse:
        thread.join()
        print "2"

    with lock:
        # 关闭文件
        filename.close()
    print "谢谢使用！"


def main2():

    urls=[]
    with open('duanzi.json') as f:
        for jostr in f.readlines():
            jo = json.loads(jostr)
            urls.append(jo['url'])

    print urls

    pageQueue = Queue(len(urls)+1)
    # 放入1~10的数字，先进先出
    for url in urls:
        pageQueue.put(url)

    # 采集结果(每页的HTML源码)的数据队列，参数为空表示不限制
    dataQueue = Queue()

    filename = open("detail.json", "a")
    # 创建锁
    lock = threading.Lock()

    # 三个采集线程的名字
    crawlList = ["采集线程1号", "采集线程2号", "采集线程3号","采集线程4号","采集线程5号"]
    # 存储三个采集线程的列表集合
    threadcrawl = []
    for threadName in crawlList:
        thread = ThreadCrawl(threadName, pageQueue, dataQueue)
        thread.start()
        threadcrawl.append(thread)


    # 三个解析线程的名字
    parseList = ["解析线程1号","解析线程2号","解析线程3号"]
    # 存储三个解析线程
    threadparse = []
    for threadName in parseList:
        thread = ThreadParse(threadName, dataQueue,'jav_detail', filename, lock)
        thread.start()
        threadparse.append(thread)

    # 等待pageQueue队列为空，也就是等待之前的操作执行完毕
    while not pageQueue.empty():
        pass

    # 如果pageQueue为空，采集线程退出循环
    global CRAWL_EXIT
    CRAWL_EXIT = True

    print "pageQueue为空"

    for thread in threadcrawl:
        thread.join()
        print "1"

    while not dataQueue.empty():
        pass

    global PARSE_EXIT
    PARSE_EXIT = True

    for thread in threadparse:
        thread.join()
        print "2"

    with lock:
        # 关闭文件
        filename.close()
    print "谢谢使用！"


if __name__ == "__main__":
    main2()

