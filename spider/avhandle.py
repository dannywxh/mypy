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



  
#for test                          
def format_vcode(path):
    vcodes=[(common.format_rule2(x)) for x in os.listdir(path) if not os.path.isdir(path+"\\"+x)]
    print vcodes
     
     
#r=1 表示同时搜索子目录
def finddup2(path,r=0):

    files=[(common.format_rule2(x),common.format_rule3(x),path) for x in os.listdir(path.decode('utf-8')) if not os.path.isdir(path+"\\"+x)]
            
    if r == 1:
        allfiles=common.walkpath(path)
        files=[(common.format_rule2(x),common.format_rule3(x),p) for x,p in allfiles]
   
    #print files     #files的格式为
    #[(u'030117_004', u'030117_004-FHD.torrent', u'd:\\new\\torrent'), (u'030317_038', u'030317_038.torrent', u'd:\\new\\torrent')]
   
    
    #for txtf in os.listdir(txtPath):
    #     files=[line for line in open(txtPath+"/"+txtf)]

    #获取计数大于1（即重复）的元素
    dup_dic=common.get_dup_dic(files)
    print dup_dic
    
    from collections import defaultdict
    #元组转字典          
    d=defaultdict(list)          
    for k,v,p in files:
        d[k].append((v,p))
    
    print len(dup_dic)
    
    savefile=path+"\\dup.txt"
    
    with open(savefile,"w") as fs: 
        #获取重复的文件名
        for it in dup_dic:
            for x in d[it[0]]:
                 #fs.write(x[0]+"\t"+x[1]+"\n")
                 fs.write('move "{0}\{1}*" ..\ \n'.format(x[1],x[0]))

                 
    print "Save found dup file done!",savefile
    


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
    

                        
                 
#对比torrent 库文件                 
def cmp_tor_store(src):
    #src=["a","b","c"]
    #des=[("a","c:\\"),("b","c:\\"),("c","c:\\"),("a","d:\\"),("b","e:\\"),("c","e:\\"),("a","c:\\")]    
    src_vids=[]
    if os.path.isdir(src):
        src_vids=[x for x in os.listdir(src) if not os.path.isdir(src+"\\"+x)]
        savefile = src + "\\tor_dup.txt"
    else:
        for line in open(src):
            p,f=os.path.split(line)
            ff,ext=os.path.splitext(f)

            src_vids.append(common.format_rule2(ff.replace("\n","")))

        p, f = os.path.split(src)
        savefile = p + "\\tor_dup.txt"

    print src_vids

    des=walkpath(TOR_STORE_PATH)

    print len(des)
   
    found_dict=comparelist(src_vids,des)

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
    except Exception as e:
        print e.message
        return file



#把本地页面格式化后存为新文件
#适用于cl的页面
def create_html_format_2(path,file):

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
        #cmp_tor_store("e:\\notexist.txt")
        #create_htmls("d:\\dd")
        #finddup2("D:\\torrents",1)
        finddup2(r"D:\\vv\\ok", 1)
        
        #format_vcode(u"H:\\av\\ok")

        #arrange_txt()