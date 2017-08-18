#coding:utf-8
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import os
import time
import common

def searchbt(keywd_list):

    driver = webdriver.Chrome()

    driver.get('https://btso.pw/search')

    mgs=[]
    for keywd in keywd_list:
        print  "start "+keywd
        time.sleep(1)
        #elem=driver.find_element_by_name('keyword')
        try:

            elem = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('// form[ @class ="form-inline hidden-xs search fullsearch-form"]/div /input'))
            #elem=driver.find_element_by_xpath('// form[ @class ="form-inline hidden-xs search fullsearch-form"]/div /input')
            elem.clear()
            elem.send_keys(keywd)
            elem.send_keys(Keys.RETURN)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            urls = soup.select('div.data-list > div.row > a')
            for url in urls:
                p,f=os.path.split(url['href'])
                magnet='magnet:?xt=urn:btih:'+f+'&dn='+url['title']
                mgs.append(magnet)
        except Exception, e:
            print e.message


    #print  mgs

    filename = "d:\\mg.txt"


    with open(filename, 'w')as f:
        for m in mgs:
            #print m
            f.write(m.encode('utf8')+"\n")

    print filename, "write file ok!"




if __name__ == "__main__":
    #phantomjs()
    #firefox()
    #chrome()

    #k=['soe345','soe346','soe347','soe348','soe349']

    path="d:\\avstore"
    files = [x for x in os.listdir(path) if all([os.path.splitext(x)[1] == '.txt', not os.path.isdir(path + "\\" + x)])]

    k = []
    for txtfile in files:
        for line in open(path + "/" + txtfile):
            p, f = os.path.split(line)
            k.append(common.format_rule2(f.replace("\n", "")))

    print  k

    searchbt(k)

