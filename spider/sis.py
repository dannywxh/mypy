#coding:utf-8
import unittest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import requests

def phantomjs():
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Linux; Android 5.1.1; Nexus 6 Build/LYZ28E) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.23 Mobile Safari/537.36"
        )

        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        #driver = webdriver.PhantomJS()

        driver.get('http://174.127.195.166/forum/forumdisplay.php?fid=230')
        # print driver.page_source

        soup = BeautifulSoup(driver.page_source, 'lxml')

        for i in range(1, 10):

            titles = soup.title

            nums = soup.find_all('span', {'class': 'dy-num fr'})
            for title, num in zip(titles, nums):
                print title.get_text(), num.get_text()
            if driver.page_source.find('shark-pager-disable-next') != -1:
                break

            all = soup.select('div.pages > a')
            print all
            # elem=driver.find_element_by_xpath('//div[@id="wrapper"]/div[1]/div[8]/div/a[3]')
            # elem=driver.find_element_by_link_text(str(i))

            elem = driver.find_element_by_id('thread_7238025')

            print elem.text

            # raw_input()
            elem.click()
            soup = BeautifulSoup(driver.page_source, 'lxml')


def firefox():

    driver = webdriver.Firefox()
    driver.get('http://174.127.195.166/forum/forumdisplay.php?fid=230')
    # print driver.page_source

    soup = BeautifulSoup(driver.page_source, 'lxml')

    for i in range(1, 10):

        titles = soup.title

        nums = soup.find_all('span', {'class': 'dy-num fr'})
        for title, num in zip(titles, nums):
            print title.get_text(), num.get_text()
        if driver.page_source.find('shark-pager-disable-next') != -1:
            break

        all = soup.select('div.pages > a')
        print all
        # elem=driver.find_element_by_xpath('//div[@id="wrapper"]/div[1]/div[8]/div/a[3]')
        # elem=driver.find_element_by_link_text(str(i))

        elem = driver.find_element_by_id('thread_7238025')

        print elem.text

        # raw_input()
        elem.click()
        soup = BeautifulSoup(driver.page_source, 'lxml')

def chrome():

    driver = webdriver.Chrome()

    for i in range(1, 10):
        driver.get('http://174.127.195.166/forum/forum-230-'+str(i)+'.html')
        # print driver.page_source

        soup = BeautifulSoup(driver.page_source, 'lxml')

        titles = soup.title
        # thread_7238020 > a
        urls = soup.select('tr > th.new > span > a')

        for url in urls:
            print  url['href'],url.get_text()


        #all = soup.select('div.pages > a')
        #print all
        #elem=driver.find_element_by_xpath('//div[@id="wrapper"]/div[1]/div[8]/div/a['+str(i)+']')

        #driver.page_source.find('shark-pager-disable-next')
        #elem=driver.find_element_by_link_text(str(i))

        #elem = driver.find_element_by_id('thread_7238025')

        #print elem.text

        # raw_input()
        #elem.click()
        #soup = BeautifulSoup(driver.page_source, 'lxml')


def gettor(url):

    driver = webdriver.Chrome()

    driver.get(url)
        # print driver.page_source

    soup = BeautifulSoup(driver.page_source, 'lxml')

    urls = soup.select('div.box.postattachlist > dl.t_attachlist > dt > a')

    url='http://174.127.195.166/forum/'+urls[0]['href']
    name=urls[0].get_text()

    downfile(url,name)


def downfile(url,name):
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Encoding': 'gzip, deflate, compress',
       'Accept-Language': 'en-us;q=0.5,en;q=0.3',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    print "start download...",name
    r=requests.get(url,headers=headers,timeout=5,stream=True)

    print "status-code:",r.status_code

    #filename=url.split('/')[-1].strip().replace("?","")
    filename="d:\\"+name;

    try:
        with open(filename,'wb')as f:
            f.write(r.content)

            print filename,"download ok!"
    except Exception,e:
        print e.message


if __name__ == "__main__":
    #phantomjs()
    #firefox()
    #chrome()
    gettor('http://174.127.195.166/forum/thread-7238012-1-1.html')

