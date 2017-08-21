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

    driver.get('http://btkitty.pet/')

    mgs=[]
    for keywd in keywd_list:
        print  "start "+keywd
        time.sleep(1)
        #elem=driver.find_element_by_name('keyword')
        try:
            # kwd/html/body/div[1]/div[3]/div[2]/form/div/div[2]
            #elem = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_xpath('// form[ @name ="search"]/div /div /input#kwd'))
            elem = WebDriverWait(driver, 10).until(
                lambda x: x.find_element_by_xpath('// input[ @ id = "kwd"]'))

            #elem=driver.find_element_by_xpath('// form[ @class ="form-inline hidden-xs search fullsearch-form"]/div /input')
            elem.clear()
            elem.send_keys(keywd)
            elem.send_keys(Keys.RETURN)

            soup = BeautifulSoup(driver.page_source, 'lxml')

            names = soup.select('dl.list-con > dt > a')
            #print names

            urls = soup.select('dl.list-con > dd.option > span:nth-of-type(1) > a')
            #print urls

            speeds = soup.select('dl.list-con > dd.option > span:nth-of-type(5) ')
            #print speeds

            counts = soup.select('dl.list-con > dd.option > span:nth-of-type(6) ')
            #print counts

            for name,url,speed,count in zip(names,urls,speeds,counts):
                mgs.append(name.get_text()+"\t"+url['href']+"\t"+speed.get_text()+"\t"+count.get_text())

        except Exception as e:
            print e.message

        mgs.append("-----------------------------------\n")

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

    """
    path="d:\\avstore"
    files = [x for x in os.listdir(path) if all([os.path.splitext(x)[1] == '.txt', not os.path.isdir(path + "\\" + x)])]

    k = []
    for txtfile in files:
        for line in open(path + "/" + txtfile):
            p, f = os.path.split(line)
            k.append(common.format_rule2(f.replace("\n", "")))

    print  k
    """
    #k=["agemix350","aka002", "atid277","avop057","avop263","awt066","awtb009","bban134","bcv011","bcv035"]
    k = [ "aka002", "atid277"]
    searchbt(k)

