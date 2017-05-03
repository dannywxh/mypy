#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient
import os, re, time, sys

from bs4 import BeautifulSoup
import common
import avhandle

reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()




def find_dup():
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]
    dup=db.jav.aggregate([{"$group": {"_id": "$code","count": {"$sum": 1 } } },{"$match": {"count": {"$gt": 1 } } }] )

    dup_id=[]
    for x in dup: 
        #print x
        dup_id.append(x["_id"])

    #print dup_id
    return dup_id
    
       
def remove_dup():
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]

    dup=find_dup()

    for x in db.info.find({"code":{"$in":dup}}).sort([("name", 1)]):
        print str(x["_id"])+"\t"+x["code"]


def stats2():
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]

    dup=find_dup()

    dup_file="d:\\dup.txt"
    with open(dup_file,"w") as fs:
        for x in db.jav.find({"code":{"$in":dup}}).sort([("name", 1)]):
            print x["disk"] +"\t"+x["name"]
            fs.write(x["disk"] +"\t"+x["name"]+"\n")

    #for d in dup:
    #    for x in db.jav.find({"code":d}):
    #        print x["disk"] +"\t"+x["name"]



def addtodb(slist):
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]
    for vid,vname,cast,vdate,score in slist:
        try:
            db.info.insert({"code":vid,"name":vname,"cast":cast,"date":vdate,"score":score})
        except Exception,e:
            print e


def update_one(id,fullname,url):
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]

    #db.jav.update({"code":id}, {"$inc":{"age":10}}, multi=True) # update users set age = age + 10

    u1 = db.jav.find_one({"code":id})
    u1['fullname'] = fullname
    u1['url'] = url
    db.jav.save(u1)


def update_multi(id,name,cast,vdate,score):
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]

    db.jav.update({"code":id}, {"$set":{"fullname":name,"cast":cast,"date":vdate,"score":score}},upsert=True, multi=True) # update jav set url ="new url1"

def query_like(val):
    client=MongoClient('127.0.0.1',27017)
    dbname='mv'
    db=client[dbname]


    for x in db.jav.find({"fullname":{"$regex": val}}):
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

def findmv():
    while True:
        print "please input search keyword:\n"
        val=raw_input()
        #query_like(u"本田")
        query_like(val.decode("gbk").encode("utf-8"))


def update_fullname(path):
    
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

    client=MongoClient('127.0.0.1',27017)
    
    db=client['mv']

    for a,b,c,d in store: 
        db.info.update({"code":a}, {"$set":{"fullname":b,"cast":c,"date":d}},upsert=True, multi=True) # update jav set url ="new url1"


if __name__ == '__main__' :
    TXT_STORE_PATH="d:\\avstore\\"
    TXT_INFO_PATH="d:\\avinfo\\"
      
    #des=walkfile(TXT_STORE_PATH)
    update_fullname(TXT_INFO_PATH)
    
    #for a,b,c,d,e in des:
    #    update_multi(a,b,c,d,e)
    #addtodb(des)

    #for a,b,c in des:
    #    update_multi(a,b,c)

    #print "update done!"
    
    #stats2()

    #update_multi("pppd413")
    #findmv()
    #arrange_txt()

    #remove_dup()

   
