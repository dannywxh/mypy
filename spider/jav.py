#!/usr/bin/env python
# -*- coding: utf-8 -*-

import Queue
import threading
import time
from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException

from parser_callback import parse_JAVLIB_Index

from parser_callback import parse_JAVLIB_Detail


import csv

import codecs

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class downloader():
    def __init__(self):
        pass

    def getContent(self, url, num_retries=2):

        userAgent='Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding': 'gzip, deflate, compress',
                   'Accept-Language': 'en-us;q=0.5,en;q=0.3',
                   'Cache-Control': 'max-age=0',
                   'Connection': 'keep-alive',
                   'User-Agent': userAgent}

        print "downloading from:%s"%(url)

        try:
            response = requests.get(url=url, headers=headers, timeout=5)  # 最基本的GET请求
            #response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # r.content  # 字节方式的响应体，会自动为你解码 gzip 和 deflate 压缩
            if response.status_code >= 400:
                msg = "Failed to downloading: {0}: {1}".format(
                    response.status_code, response.text)
                raise RequestException(msg)
            html=response.text
        except RequestException as e:
            #raise
            print "Downloading error:{0}:{1}".format(url,e)
            html=None
            if num_retries>0:
                return self.getContent(url,num_retries-1)

        return html

def hasNext(html):
    soup = BeautifulSoup(html, "lxml")

    nextpage = soup.select("div.page_selector > a.page.next")

    if len(nextpage)>0:
        return True
    else:
        return False




def threaded_crawler(seed_urls, scrape_callback=None, max_threads=10,checkPage=False):

    mutex = threading.Condition()

    q = Queue.Queue()

    crawl_queue = seed_urls


    out=[]

    d = downloader()

    def process_queue():
        while True:
            try:
                url = crawl_queue.pop()
                if not q.empty():
                    if q.get() == -1:
                        break
                #url = crawl_queue.get()
            except IndexError:
                # crawl queue is empty
                break
            else:
                html = d.getContent(url)

                if checkPage:
                    if not hasNext(html):
                        print "Last page is %s"%url
                        q.put(-1)
                        q.task_done()

                if scrape_callback:
                    try:
                        links=scrape_callback(url,html)
                    except Exception as e:
                        print 'Error in callback for: {}: {}'.format(url, e)
                    else:
                        if type(links) is list:
                            out.extend(links)
                        else:
                            out.append(links)


    # wait for all download threads to finish
    threads = []
    while threads or crawl_queue:
        # the crawl is still active
        for thread in threads:
            if not thread.is_alive():
                # remove the stopped threads
                threads.remove(thread)

        while len(threads) < max_threads and crawl_queue:
            # can start some more threads
            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True) # set daemon so main thread can exit when receives ctrl-c
            thread.start()
            threads.append(thread)
        # all threads have been processed
        # sleep temporarily so CPU can focus execution on other threads
        time.sleep(1)

    return out


def getDetailByindex():
    urlb = "http://www.ja14b.com/cn/vl_update.php?&mode=&page="
    scrape_callback = parse_JAVLIB_Index()

    urls=[]

    for i in range(12, 0, -1):
        urls.append(urlb.format('afark',i))

    out1=threaded_crawler(urls,scrape_callback,max_threads=5)#1,checkPage=True)

    print out1
    print len(out1)

    scrape_callback = parse_JAVLIB_Detail()

    urls2 = []
    for dic in out1:
        urls2.extend(dic.values())

    #print urls2
    out2 = threaded_crawler(urls2, scrape_callback)

    print out2
    print len(out2)


def getDetailByCast(cast_code,cast_name,page=10):
    urlb = "http://www.ja14b.com/cn/vl_star.php?s={0}&page={1}"
    # urlb = "http://www.ja14b.com/cn/vl_star.php?s=afark&page=20"

    scrape_callback = parse_JAVLIB_Index()

    urls = []

    for i in range(page, 0, -1):
        urls.append(urlb.format(cast_code, i))

    out1 = threaded_crawler(urls, scrape_callback, max_threads=5,checkPage=True)

    print out1
    print len(out1)

    scrape_callback = parse_JAVLIB_Detail(cast_name)

    urls2 = []
    for dic in out1:
        urls2.extend(dic.values())

    # print urls2
    out2 = threaded_crawler(urls2, scrape_callback)

    print out2
    print len(out2)

def getDetailByIds(ids_list):

    scrape_callback = parse_JAVLIB_Detail("jav_ids")

    urlb = "http://www.ja14b.com/cn/vl_searchbyid.php?keyword={0}"
    # urlb = "http://www.ja14b.com/cn/vl_star.php?s=afark&page=20"

    urls=[]
    for vid in ids_list:
        urls.append(urlb.format(vid))

    out1 = threaded_crawler(urls, scrape_callback, max_threads=5)  # 1,checkPage=True)


if __name__ == '__main__':

    ids = ['soe386']
    #getDetailByIds(ids)

    #getDetailByCast('afark', u"三島奈津子")

    #getDetailByCast('azacm', u"仓多真央",page=20)
    getDetailByCast('ayrck', u"水咲あかね", page=5)

    #getDetailByindex()

