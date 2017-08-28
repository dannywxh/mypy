#coding:utf-8
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
import os
import time
import common

def searchbt(keywd_list):

    driver = webdriver.Chrome()

    #driver.implicitly_wait(10)  #
    #driver.set_page_load_timeout(10)
    #driver.set_script_timeout(10)  # 这两种设置都进行才有效

    url="http://zhainanbt.com/"
    driver.get(url)

    mgs=[]
    for keywd in keywd_list:
        print  "start:"+keywd

        try:
            elem = WebDriverWait(driver, 5,0.5, ignored_exceptions=None).until(
                lambda x: x.find_element_by_xpath('// input[ @ id = "kwd"]'))

            #elem = WebDriverWait(driver, 5, 0.5, ignored_exceptions=None).until(
            #EC.presence_of_element_located((By.ID, "kwd")))

            elem.clear()
            elem.send_keys(keywd)
            elem.send_keys(Keys.RETURN)

            elem_btn=driver.find_element_by_xpath('// form[ @ id = "searchFrom"] / div / div[1] / button');
            if elem_btn:
                print "click!"
                print elem_btn
                #elem_btn.click()


            #elem_btn = WebDriverWait(driver, 5, 0.5, ignored_exceptions=None).until(
            #    lambda x: x.find_element_by_xpath('// form[ @ id = "searchFrom"] / div / div[1] / button'))

        except NoSuchElementException as e:
            print e.message
            driver.refresh()

        except TimeoutException as e:
            print e.message
            driver.refresh()

        else:
            soup = BeautifulSoup(driver.page_source, 'lxml')

            names = soup.select('dl.item > dt > a')
            print names

            urls = soup.select('dl.item > dd.attr > span:nth-of-type(6) > a')
            print urls

            speeds = soup.select('dl.item > dd.attr > span:nth-of-type(5)')
            print speeds

            counts = soup.select('dl.item > dd.attr > span:nth-of-type(4)')
            print counts

            for name,url,speed,count in zip(names,urls,speeds,counts):
                mgs.append(name.get_text()+"\t"+url['href']+"\t"+speed.get_text()+"\t"+count.get_text())

        driver.close()
        mgs.append("----------------------------------------------\n")

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


    path=u"e:\\倉多まお"
    files = [x for x in os.listdir(path) if all([os.path.splitext(x)[1] == '.txt', not os.path.isdir(path + "\\" + x)])]

    k = []
    for txtfile in files:
        for line in open(path + "/" + txtfile):
            p, f = os.path.split(line)
            k.append(common.format_rule2(f.replace("\n", "")))

    print  k

    #k=["agemix350","aka002", "atid277","avop057","avop263","awt066","awtb009","bban134","bcv011","bcv035"]
    #k = [ "aka002", "atid277"]
    searchbt(k)

