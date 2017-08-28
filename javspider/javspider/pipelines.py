# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import json

reload(sys)
sys.setdefaultencoding('utf-8')


class JavspiderPipeline(object):
    # __init__方法是可选的，做为类的初始化方法
    def __init__(self):
        # 创建了一个文件
        self.filename = open("jav_detail.json", "w")

    def process_item(self, item, spider):
        jsontext = json.dumps(dict(item), ensure_ascii=False) + ",\n"
        #print  jsontext
        self.filename.write(jsontext.encode("utf-8"))
        return item

        # close_spider方法是可选的，结束时调用这个方法
        def close_spider(self, spider):
            self.filename.close()