#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, time, sys

from bs4 import BeautifulSoup
from pymongo import MongoClient, DESCENDING


import avhandle
import common


reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()



class  MyMongodb(object):
    """docstring for  MyMongodb"""
    def __init__(self, db_name,collection_name):
        super( MyMongodb, self).__init__()
        self.client=MongoClient('127.0.0.1',27017)
        self.db=client[db_name]
        self.collection=self.db[collection_name]


    def jsonsave(self,json):
        data = dict(json)
        # 向指定的表里添加数据
        self.collection.insert(data)
        

    def find_dup_id(self):
        dup=self.collection.aggregate([{"$group": {"_id": "$code","count": {"$sum": 1 } } },{"$match": {"count": {"$gt": 1 } } }] )

        dup_id=[]
        for x in dup: 
            #print x
            dup_id.append(x["_id"])

        #print dup_id
        return dup_id
       
    def remove_dup(self):

        dup=self.find_dup_id()

        for x in self.collection.find({"code":{"$in":dup}}).sort([("name", 1)]):
            print str(x["_id"])+"\t"+x["code"]

    #input src dict
    #output dup file dict
    #return tuple :(code,filename)
    def find_dup(self,dict_files):

        id_list=dict_files.keys() 
        #value_list= dict_files.values()
        
        dups=[]

        for x in self.collection.find({"code":{"$in":id_list}}).sort([("code", 1)]):
            print x["disk"] +"\t"+x["name"]
            dups.append((x["code"],x["disk"],x["name"],dict_files[x["code"]]))

        return dups
     
        #for d in dup:
        #    for x in db.jav.find({"code":d}):
        #        print x["disk"] +"\t"+x["name"]



    def addtodb(self,slist):
        for vid,vname,cast,vdate,score in slist:
            try:
                self.collection.insert({"code":vid,"name":vname,"cast":cast,"date":vdate,"score":score})
            except Exception,e:
                print e

    def txtstore_addtodb(slef,slist):
        for vid,vname,disk in slist:
            try:
                self.collection.insert({"code":vid,"name":vname,"disk":disk})
            except Exception,e:
                print e
            
    def update_one(self,id,fullname,url):
        #db.jav.update({"code":id}, {"$inc":{"age":10}}, multi=True) # update users set age = age + 10

        u1 = self.collection.find_one({"code":id})
        u1['fullname'] = fullname
        u1['url'] = url
        self.collection.save(u1)


    def update_multi(self,id,name,cast,vdate,score):

        self.collection.update({"code":id}, {"$set":{"fullname":name,"cast":cast,"date":vdate,"score":score}},upsert=True, multi=True) # update jav set url ="new url1"

    def query_like(self,val):
        for x in self.collection.find({"fullname":{"$regex": val}}):
            try:
                print x["fullname"]
            except Exception,e:
                print e


'''
db.jav.aggregate([{ $group: {_id: "$code",count: { $sum: 1 } } },   { $match: { count: { $gt: 1 } } }] )


 db.jav.find({"fullname":/本田/})
 
 db.jav.find().count()
  
 db.jav.find({"code":{"$in":["soe385","jux959", "soe386"]}})
 
 db.jav.find( { "fullname": { $exists: true } } ).count()
 

'''

    def findmv(self):
        while True:
            print "please input search keyword:\n"
            val=raw_input()
            #query_like(u"本田")
            query_like(val.decode("gbk").encode("utf-8"))


    def update_fullname(self,path):
        
        files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
        
        # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
        store=[]
        for txtfile in files:
            for line in open(path+"/"+txtfile):
                
                info=line.split("\t")
                vid=common.format_rule2(info[2].strip())
                name=info[2].strip()
                cast=info[3].strip()
                vdate=info[4].strip()

                if u"识别码搜寻结果" in name:
                    print name.encode("gbk")
                else:
                    store.append((vid,name,cast,vdate))

        print len(store)

        for a,b,c,d in store: 
            self.collection.update({"code":a}, {"$set":{"fullname":b,"cast":c,"date":d}},upsert=True, multi=True) # update jav set url ="new url1"

#目录下已经在mgdb存在的文件
    def find_path_dup_from_mgdb(self,path):
        #src_files=[avhandle.format2(x):x for x in os.listdir(path) if not os.path.isdir(path+"\\"+x)]

        #生成（{code：name}）字典 
        src_files=dict((avhandle.format_rule2(x), x) for x in os.listdir(path.decode("utf-8")) if not os.path.isdir(path.decode("utf-8")+"\\"+x))
     
        #print src_files
        
        dups=find_dup(src_files)
        
        savefile=path+"\\dup.txt"
        
        with open(savefile,"w") as fs: 
            #获取重复的文件名
            for code,disk,name,src_filename in dups:
                fs.write('move "%s" c:\\tmp \n'%src_filename)
                fs.write('rem %s \t %s \t %s \n'%(code,disk,name))
                
                     
        print "save found dup file done!",savefile          
 
    

if __name__ == '__main__' :
    TXT_STORE_PATH="d:\\avstore\\"
    TXT_INFO_PATH="d:\\avinfo\\"


    mm=MyMongodb("mv","jav") 
#增加新片到库      
#     des=avhandle.walk_txtstore_file(u"G:\\3",only_code=False)
#     print len(des)
#     print des
#     txtstore_addtodb(des)
    
    #update_fullname(TXT_INFO_PATH)
    
    #for a,b,c,d,e in des:
    #    update_multi(a,b,c,d,e)
    

    #for a,b,c in des:
    #    update_multi(a,b,c)

    #print "update done!"
    
#查找目录下已经存在的片子。与mgdb库比较
    #find_path_dup_from_mgdb("d:\\torrents")
    mm.find_path_dup_from_mgdb("h:\\0710")

   
    
#查找已存在的片子，
    #1，先根据javlib获取全部片子，并保存在txt文件里
    #2，通过读取txt获取影片名称
    #3,影片名称传给find_dup进行mongodb查找，得到disk位置 

    #mvname=avhandle.get_mvname_from_txt(u"D:\\avstore\\cast_info\\奥田咲.txt")
    #mvname=avhandle.get_mvname_from_txt(u"D:\\avstore\\cast_info\\三島奈津子.txt")
    #mvname=avhandle.get_mvname_from_txt(u"D:\\avstore\\cast_info\\三好亚矢.txt")
    
    #print len(mvname)
    #find_dup(mvname)

    #update_multi("pppd413")
    #findmv()
    #arrange_txt()

    #remove_dup()

   
