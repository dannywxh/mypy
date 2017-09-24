# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import pymongo

reload(sys)
sys.setdefaultencoding('utf-8')


class JavspiderPipeline(object):
    # __init__方法是可选的，做为类的初始化方法
    def __init__(self):
        # 获取setting主机名、端口号和数据库名
        host = "127.0.0.1"
        port = 27017
        dbname = 'mv'
        client = pymongo.MongoClient(host=host, port=port)
        mdb = client[dbname]
        self.post = mdb['test']

    def process_item(self, item, spider):
        data=dict(item)
        data['_id']=item['id']
        self.post.insert(data)
        return item

        # close_spider方法是可选的，结束时调用这个方法
        def close_spider(self, spider):
            self.filename.close()