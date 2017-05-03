#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import hashlib, bencode


from bs4 import BeautifulSoup


reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('utf-8')
print sys.getdefaultencoding()



def parse_tor(file):
    bt_path = {}

    bt_file = open(file, 'rb')
    bt_info = bencode.bdecode(bt_file.read()).get('info')
    bt_info_hash_hex = hashlib.sha1(bencode.bencode(bt_info)).hexdigest()
  
    bt_file_size = bt_info.get('length')
    bt_file_name = bt_info.get('name')
    
    bt_path[bt_file_name]=bt_file_size

    print bt_path 

    bt_file.close()
 


def format_rule2(s):
        rs=''
        #匹配开头是数字,判断是非wm编号 
        wm=re.findall(r'^\d+',s)
     
        if len(wm)==1:  #是wm
            rs=s[0:10]
            return rs

        # 如:mide-267FHD_ok_0001.mp4
        #查找所有的非数字,['mide-', 'FHD_ok_', '.mp']
        #第一个元素就是"mide-"
        alpha_list=re.findall(r'\D+', s)
        
        if len(alpha_list)>0: 
            rs+=alpha_list[0]

        #查找所有的数字,['267', '0001', '4']
        #第一个元素就是"267"
        num_list=re.findall(r'\d+', s)

        if len(num_list)>0:
            rs+=num_list[0]

        if rs=='':
            rs=s

        rs=rs.replace("-","")
        rs=rs.replace(" ","")
        rs=rs.replace("_","")
        rs=rs.lower()
        return rs

  
#for test                          
def format_torrent(path):
    for x in  os.listdir(path):
        print format_rule2(x)
     
    
def walkpath(path):
   #files= [(dirpath,filenames) for dirpath,dirname,filenames in os.walk(path)]
   files= []
   for dirpath,dirname,filenames in os.walk(path.decode('utf-8')):
       for filename in filenames:
           files.append((filename,dirpath))
       
   return files  


def walkfile(path):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            p,f=os.path.split(line)
            store.append((f.replace("\n",""),txtfile))
            
    return store  
    
#两个list对比核心功能，其他功能调用
def comparelist(src,des):
    #src: ["file"]    
    #des:[("file","path")]
    
    from collections import defaultdict

    dic=defaultdict(list)       

    for x in src:
        for a,b in des:
            #print x,a,b
            if format_rule2(x)==format_rule2(a):
                 dic[x].append(os.path.join(b,a))       

    return dic    
    
                        
                 
