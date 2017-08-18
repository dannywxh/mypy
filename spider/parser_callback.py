# -*- coding: utf-8 -*-

import csv
import re
import urlparse
import lxml.html
from bs4 import BeautifulSoup

from common import format_rule2

import sys
reload(sys) # Python2.5 初始化后会删除 sys.setdefaultencoding 这个方法，我们需要重新载入
sys.setdefaultencoding('utf-8')

class parse_JAVLIB_Index:
    def __init__(self):
        self.writer = csv.writer(open('d:\\javs_index.csv', 'w'))
        #self.writer = csv.DictWriter(open('d:\\javs_index.csv', 'w'))
        #self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
        #self.writer.writerow(self.fields)

    def __call__(self, url,html):
        soup = BeautifulSoup(html, "lxml")
        dic = {}
        vurls = soup.select("div.video > a")
        vids = soup.select("div.video > a > div.id")

        links = ['http://www.ja14b.com/cn' + x['href'][1:] for x in vurls]
        for vid,link in zip(vids,links):
            dic[format_rule2(vid.get_text())]=link

        print dic

        for k, v in dic.iteritems():
            self.writer.writerow([k, v])

        return dic


class parse_JAVLIB_Detail():
    def __init__(self,cast_name):
        self.writer = csv.writer(open(u'd:\\{0}.csv'.format(cast_name.encode('utf8')), 'w'))
        self.cast_name=cast_name
        #self.fields = ('area', 'population', 'iso', 'country', 'capital', 'continent', 'tld', 'currency_code', 'currency_name', 'phone', 'postal_code_format', 'postal_code_regex', 'languages', 'neighbours')
        #self.writer.writerow(self.fields)

    def __call__(self, url, html):
        soup = BeautifulSoup(html, "lxml")

        vimg = soup.select("div#video_jacket > img#video_jacket_img")
        vid = soup.select("div#video_info > div#video_id td.text")
        vdate = soup.select("div#video_info > div#video_date td.text")
        score = soup.select("div#video_review td.text > span.score")
        genres_list = soup.select("div#video_genres  td.text > span.genre > a")
        genres = ""
        for a in genres_list:
            genres += a.get_text() + " "

        genres_list = []
        genres_list.append(genres.encode('gbk'))

        cast_list = soup.select("div#video_cast td.text > span.cast > span.star > a")
        vcast = ""
        for a in cast_list:
            vcast += a.get_text() + " "
        cast_list = []
        cast_list.append(vcast.encode('gbk'))

        wanted = soup.select("div#video_favorite_edit > span#subscribed > a")
        owned = soup.select("div#video_favorite_edit > span#owned > a")

        info = ()
        for a_id, a_img, a_date, a_score, a_wanted, a_owned, cast, genres in zip(vid, vimg, vdate, score, wanted, owned,
                                                                                 cast_list, genres_list):
            info = url,a_id.get_text(), a_date.get_text(), a_score.get_text(), a_wanted.get_text(), a_owned.get_text(), cast, genres, \
                   a_img['src']

        self.writer.writerow(info)

        return info


if __name__ == '__main__':
    link_crawler('http://example.webscraping.com/', '/(index|view)', scrape_callback=ScrapeCallback())
