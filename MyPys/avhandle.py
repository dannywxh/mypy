#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import hashlib, bencode
import common

from bs4 import BeautifulSoup
from test.warning_tests import outer


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
 

def format_name(oriname):
    print oriname 
    mode=re.compile(r'\d+')
    d=mode.findall(oriname)[0]
    c=oriname.split(d)[0]

    fmtname=c+d
    print fmtname

    return fmtname

#计数
#sequence的格式是list：[1,2,3,4...]
def get_count1(sequence):
    counts={}
    for x in sequence:
        if x in counts:
            counts[x]+=1
        else:
            counts[x]=1
    return counts

#获取计数大于1的数据
#sequence的格式是元组：(x,y)
def get_dup_dic(sequence):
    counts={}
    for x,y,z in sequence:
        if x in counts:
            counts[x]+=1
        else:
            counts[x]=1
            
    kv_pairs=[(count,tz) for count,tz in counts.items() if tz>1]
    return kv_pairs
            


#top 10
def top_counts(dic_counts,n=10):
    kv_pairs=[(count,tz) for count,tz in dic_counts.items()]
    kv_pairs.sort()
    return kv_pairs[-n:]


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
def format_vcode(path):
    vcodes=[(format_rule2(x)) for x in os.listdir(path) if not os.path.isdir(path+"\\"+x)]
    print vcodes
     
     
#r=1 表示同时搜索子目录
def finddup2(path,r=0):

    files=[(format_rule2(x),x,path) for x in os.listdir(path) if not os.path.isdir(path+"\\"+x)]
            
    if r==1:
        allfiles=walkpath(path)
        files=[(format_rule2(x),x,p) for x,p in allfiles]
   
    #print files     #files的格式为
    #[(u'030117_004', u'030117_004-FHD.torrent', u'd:\\new\\torrent'), (u'030317_038', u'030317_038.torrent', u'd:\\new\\torrent')]
   
    
    #for txtf in os.listdir(txtPath):
    #     files=[line for line in open(txtPath+"/"+txtf)]

    #获取计数大于1（即重复）的元素
    dup_dic=get_dup_dic(files)
    #print dic
    
    from collections import defaultdict
    #元组转字典          
    d=defaultdict(list)          
    for k,v,p in files:
        d[k].append((v,p))
    
    #print d
    
    savefile=path+"\\dup.txt"
    
    with open(savefile,"w") as fs: 
        #获取重复的文件名
        for it in dup_dic:
            for x in d[it[0]]:
                 #print x
                 fs.write(x[0]+"\t"+x[1]+"\n")
                 
    print "save found dup file done!",savefile             
    
    
def walkpath(path):
    #files= [(dirpath,filenames) for dirpath,dirname,filenames in os.walk(path)]
    files= []
    for dirpath,dirname,filenames in os.walk(path.decode('utf-8')):
        for filename in filenames:
            files.append((filename,dirpath))
        
    return files  

def path_code_format(path,only_code=True):
    
    files=[x for x in os.listdir(path.decode('utf-8')) if not os.path.isdir(path.decode('utf-8')+"\\"+x)]
 
    vids=[] 
    
    for f in files:
        try:
            if only_code:
                vids.append(common.format_rule2(f))
            else:        
                vids.append((common.format_rule2(f),f.replace("\n","").decode('utf-8')))
                #store.append((common.format_rule2(f),f.replace("\n",""),txtfile))
                #store.append((format_rule2(f),f.replace("\n","").decode("unicode_escape"),txtfile))    
        except Exception:
            print "Error %s"%f
        
    return vids  

#txt文件需要先存为utf-8格式
def walk_txtstore_file(path,only_code=False):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            p,f=os.path.split(line)
            
            ext=f[-4:-1]
            if ext=="jpg":
                print "jpg"
                continue
            
            try:
                if only_code:
                    store.append(common.format_rule2(f))
                else:        
                    store.append((common.format_rule2(f),f.replace("\n","").decode('utf-8'),txtfile))
                    #store.append((common.format_rule2(f),f.replace("\n",""),txtfile))
                    #store.append((format_rule2(f),f.replace("\n","").decode("unicode_escape"),txtfile))    
            except Exception,e:
                print txtfile,f

    return store  

'''
def get_torrents_by_vids(vid_list,tor_path):
    files=[x for x in os.listdir(tor_path.decode('utf-8')) if not os.path.isdir(tor_path.decode("utf-8")+"\\"+x)]
    
    dups=[]
    for vid in vid_list:
        for tfile in files:
            if vid==common.format_rule2(tfile):
                dups.append(tfile)
    
    print dups
    savefile=tor_path+"\\dup.txt"
    with open(savefile,"w") as fs:
        for f in dups:
            fs.write('move "{0}" d:\\\n'.format(f))
'''

def walkfile1(path):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            
            vid,cast,vdate,score=line.split("\t")
            if u"识别码搜寻结果" in vid:
                print vid.encode("gbk")
            else:
                store.append((common.format_rule2(vid),vid,cast,vdate,score.replace("\n","")))
            #store.append((format_rule2(vid.encode("utf8")),vid.encode('utf-8'),url))
            #store.append((format_rule2(f),f.replace("\n","").decode("unicode_escape"),txtfile))            

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
    
                        
                 
#对比torrent 库文件                 
def cmp_tor_store(src_path):
    #src=["a","b","c"]
    #des=[("a","c:\\"),("b","c:\\"),("c","c:\\"),("a","d:\\"),("b","e:\\"),("c","e:\\"),("a","c:\\")]    
   
    src=[x for x in os.listdir(src_path) if not os.path.isdir(src_path+"\\"+x)]
    
    des=walkpath(TOR_STORE_PATH)
   
    found_dict=comparelist(src,des)     
    
    savefile=src_path+"\\tor_dup.txt"
     
    with open(savefile,"w") as fs:
        for k,files in found_dict.items():
            fs.write('move "{0}" c:\\\n'.format(k))
            for f in files:
                fs.write('rem "{0}" \n'.format(f))
                 
    print savefile,"save complete!"    
    
                
#对比txt 库文件                 
def cmp_txt_store(src_path):
    #src=["a","b","c"]
    #des=[("a","c:\\"),("b","c:\\"),("c","c:\\"),("a","d:\\"),("b","e:\\"),("c","e:\\"),("a","c:\\")]    
   
    src=[x for x in os.listdir(src_path) if not os.path.isdir(src_path+"\\"+x)]
    
    des=common.walkfile(TXT_STORE_PATH)
   
    found_dict=comparelist(src,des)     
    
    savefile=src_path+"\\txt_dup.txt"
    
    with open(savefile,"w") as fs:
        for k,files in found_dict.items():
             fs.write('move "{0}" c:\\tmp \n'.format(k))
             for f in files:
                fs.write('rem "{0}" \n'.format(f))
                 
    print savefile,"save complete!"    



#把本地页面格式化后存为新文件
#适用于jav的页面
def create_html_format_l(path,file):

    html="" 
    with open(path+"\\"+file,"rb") as f:
        html=f.read()

    soup = BeautifulSoup(html,"html.parser")

    title=soup.title.string.replace("/"," ").replace("?"," ")


    try:  
        div=soup.find('div',id='video_title')
        table=soup.find('table',id='video_jacket_info')

        body=soup.body

        body.clear()

        body.append(div)
        body.append(table)
      
        [s.extract() for s in soup.find_all('script')]
        [s.extract() for s in soup.find_all('link')]
        #[s.extract() for s in soup.find_all('meta')]
        
        with open(path+"\\new"+title+".html","w") as f:
             f.write(soup.prettify().encode('utf8'))

        print "new file created!"
        return ""
    except Exception,e:
        print e.message
        return file



#把本地页面格式化后存为新文件
#适用于cl的页面
def create_html_format_2(path,file):

    html="" 
    with open(path+"\\"+file,"rb") as f:
        html=f.read()

    print html
    soup = BeautifulSoup(html,"html.parser")

    title=soup.title.string.replace("/"," ").replace("?"," ")

    try:
        
        [s.extract() for s in soup.find_all('script')]
        [s.extract() for s in soup.find_all('link')]
        #[s.extract() for s in soup.find_all('meta')]

        div=soup.find('div',class_='tpc_content do_not_catch') #tpc_content do_not_catch
         
        print div

        a=div.find('a')
        img=div.find('img')
        
        a["href"]=a.get_text() #替换标签属性
        del a['onmouseout']    #删除标签属性
        del a['onmouseover']
        del img['onclick']

        body=soup.body

        body.clear()

        body.append(div)

        with open(path+"\\new\\"+title+".html","w") as f:
            try:
                f.write(soup.prettify().encode('utf8'))
            except Exception:
                f.write(soup.prettify().encode('gbk'))
        
        print "new file created!"
        return ""

    except Exception,e:
        print e.message
        return file

   
    
def create_htmls(path):

    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.html', not os.path.isdir(path+"\\"+x)])]
 
    if not os.path.exists(path+"//new"):
        os.chdir(path)
        os.mkdir("new")
     
    errors=[]
    for file in files:
        print "start handle ",file
        ret=create_html_format_2(path,file)

        if ret!='':
           errors.append(ret)  

    with open(path+"\\error.txt","w") as f:
        for err in errors:
            f.write(err+"\n")

    print errors 
       


def parseHTML_jav_detail(data):
    soup = BeautifulSoup(data,"html.parser")

    title=soup.title.string.strip()
    try:
        print title
    except:
        print title.encode('utf-8')
    
    try:
        div=soup.find('div',{"id":'video_info'})
        div_cast=div.find('div',{"id":'video_cast'})
        a=div_cast.find('a');
        vcast=a.string.strip()
    except:
        #print "vcast not found!"
        vcast=""
    
    try:
        div=soup.find('div',{"id":'video_date'})
        td_date=div.find('td',class_="text")
        vdate=td_date.string.strip()
    except:
        #print "vdate not found!"
        vdate=""   

    try:
        div=soup.find('div',{"id":'video_review'})
        span=div.find('span',class_="score") 
        score=span.string.strip()
    except:
        #print "score not found!"
        score=""

    try:
        #print title,cast,vdate,score
        return u'%s\t%s\t%s\t%s'%(title,vcast,vdate,score)
        #return title+"\t"+cast+"\t"+vdate+"\t"+score
    except:
        print "encode error!"
        return "error"


def arrange_txt():
    path="D:\\avstore\\jav-2\\"
    files=[x for x in os.listdir(path.decode("utf-8")) if not os.path.isdir(path.decode("utf-8")+"\\"+x)]

    perror=[] 
    out=[] 

    for f in files:
        data=open(path.decode("utf-8")+f,'r').read()
        ret=parseHTML_jav_detail(data)
        if ret=="error":
            perror.append(f)
        else:
            out.append(ret)


    with open(path+"\\out.txt","w") as fo:
        for msg in out:
            fo.write(msg+"\n")
    print "out file created!"    

    with open(path+"\\err.txt","w") as fo:
        for err in perror:
            fo.write('move "'+err+'" tmp\\'+'\n')
    print "err file created!"

#txtfile format need tab split
def get_mvname_from_txt(txtfile):
    out=[] 
    for line in open(txtfile):
        out.append(line.split("\t")[0])
        
    return out    

    
if __name__ == '__main__' :
    TXT_STORE_PATH="d:\\avstore\\"
    TOR_STORE_PATH="d:\\torrents\\"
    
    if len(sys.argv) ==2:
        path= sys.argv[1]

        #walkfile("d:\\new\\")
        #create_htmls(path)
        #finddup2(d:\\new\\torrent\\")
        #cmp_txt_store(path)
        cmp_tor_store(path)
        
    else:
        #cmp_txt_store("c:\\torrent")
        #cmp_tor_store("c:\\torrent")   
        #create_htmls("d:\\dd")
        #finddup2("d:\\new\\torrent",1)
        
        format_vcode(u"H:\\av\\ok")

        #arrange_txt()