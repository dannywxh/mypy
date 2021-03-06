#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import hashlib, bencode
import requests

from os.path import getsize

from bs4 import BeautifulSoup


reload(sys)
#print sys.getdefaultencoding()
#sys.setdefaultencoding('utf-8')
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
 
#提取无码的格式，如  082516-001
def format_rule1(s):
 
    pattern="\d{6}-\d{3}|\d{6}-\d{2}|\d{6}_\d{3}|\d{6}_\d{2}"
    
    rs=re.findall(pattern, s);
    
    if len(rs)>=1:
        return rs[0]
    else:
        return ""
    
    
 
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

#提取番号部分
def format_rule3(s):
    rs = ''
    # 匹配开头是数字,判断是非wm编号
    wm = re.findall(r'^\d+', s)

    if len(wm) == 1:  # 是wm
        rs = s[0:10]
        return rs

    # 如:mide-267FHD_ok_0001.mp4
    # 查找所有的非数字,['mide-', 'FHD_ok_', '.mp']
    # 第一个元素就是"mide-"
    alpha_list = re.findall(r'\D+', s)

    if len(alpha_list) > 0:
        rs += alpha_list[0]

    # 查找所有的数字,['267', '0001', '4']
    # 第一个元素就是"267"
    num_list = re.findall(r'\d+', s)

    if len(num_list) > 0:
        rs += num_list[0]

    if rs == '':
        rs = s

    return rs


#for test
def format_torrent(path):
    for x in  os.listdir(path):
        print format_rule2(x)

    # 两个list对比核心功能，其他功能调用
    def comparelist(src, des):
        # src: ["file"]
        # des:[("file","path")]

        from collections import defaultdict

        dic = defaultdict(list)

        for x in src:
            for a, b in des:
                # print x,a,b
                if format_rule2(x) == format_rule2(a):
                    dic[x].append(os.path.join(b, a))

        return dic

    # 计数
# sequence的格式是list：[1,2,3,4...]
def get_count1(sequence):
    counts = {}
    for x in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1
    return counts


# 获取计数大于1的数据
# sequence的格式是元组：(x,y)
def get_dup_dic(sequence):
    counts = {}
    for x, y, z in sequence:
        if x in counts:
            counts[x] += 1
        else:
            counts[x] = 1

    kv_pairs = [(count, tz) for count, tz in counts.items() if tz > 1]
    return kv_pairs


# top 10
def top_counts(dic_counts, n=10):
    kv_pairs = [(count, tz) for count, tz in dic_counts.items()]
    kv_pairs.sort()
    return kv_pairs[-n:]


def walkpath(path):
    #files= [(dirpath,filenames) for dirpath,dirname,filenames in os.walk(path)]
    files= []
    for dirpath,dirname,filenames in os.walk(path.decode('utf-8')):
        for filename in filenames:
            files.append((filename,dirpath))

    print "files count:%d"%len(files)
    return files


def walkpath_withFileSize(path):
    # files= [(dirpath,filenames) for dirpath,dirname,filenames in os.walk(path)]
    files = []
    for fulldirpath, dirnameList, filenameList in os.walk(path.decode('utf-8')):
        for filename in filenameList:
            ext = filename[-3:].lower()
            #print ext
            exts = ['mkv', 'wmv', 'mp4', 'avi','rmvb']
            if ext in exts:
                #print dirname,dirpath
                size=getsize(os.path.join(fulldirpath, filename)) / (1024.0 * 1024.0)
                if size>1024:
                    size=round(size/1024.0,2)
                else:
                    size=round(size,1)

                #print filename, size, fulldirpath
                files.append((filename,size, fulldirpath))

    print len(files)
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


def getFormated_vcode_walkpath_txtfile(path):
    files = [x for x in os.listdir(path) if all([os.path.splitext(x)[1] == '.txt', not os.path.isdir(path + "\\" + x)])]

    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store = []
    for txtfile in files:
        for line in open(path + "/" + txtfile):
            p, f = os.path.split(line)
            ff,ext = os.path.splitext(f)
            store.append(format_rule2(ff.replace('\n','')))

    return store


# txt文件需要先存为utf-8格式
def walk_txtstore_file(path, only_code=False):
    files = [x for x in os.listdir(path) if all([os.path.splitext(x)[1] == '.txt', not os.path.isdir(path + "\\" + x)])]

    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store = []
    for txtfile in files:
        for line in open(path + "/" + txtfile):
            p, f = os.path.split(line)

            ext = f[-4:-1]
            if ext == "jpg":
                print "jpg"
                continue

            try:
                if only_code:
                    store.append(format_rule2(f))
                else:
                    store.append((format_rule2(f), f.replace("\n", "").decode('utf-8'), txtfile))
                    # store.append((common.format_rule2(f),f.replace("\n",""),txtfile))
                    # store.append((format_rule2(f),f.replace("\n","").decode("unicode_escape"),txtfile))
            except Exception, e:
                print txtfile, f

    return store


#����list�ԱȺ��Ĺ��ܣ������ܵ���
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
    

def download(url):

    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Encoding': 'gzip, deflate, compress',
       'Accept-Language': 'en-us;q=0.5,en;q=0.3',
       'Cache-Control': 'max-age=0',
       'Connection': 'keep-alive',
       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

    print "download from "+url+"\n"
    try:
        response = requests.get(url=url,headers=headers,timeout=5)    # 最基本的GET请求
        return response
    except Exception,e:
        print e
    #print "status_code",response.status_code


if __name__ == '__main__':

    """
    a=["DOKS-023","DOKS-055","DOKS-078","DOKS-123","DOKS-125","DOKS-139","DOKS-140",
    "DOKS-150","DOKS-155","DOKS-168","DOKS-187","DOKS-189","DOKS-217","DOKS-232","DOKS-234"]

    b=[format_rule2(x) for x in a]

    print b
    """

    walkpath_withFileSize("g:\\av\\achive")

