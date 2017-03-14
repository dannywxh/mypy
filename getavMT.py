#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import random
import requests
import threading
import Queue
import StringIO

from bs4 import BeautifulSoup


reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('gbk')
print sys.getdefaultencoding()



class getUrlThread(threading.Thread):
    def __init__(self,url,sid,queue):
        threading.Thread.__init__(self)
        self.sid=sid
        self.queue=queue

        self.url=url
      
    def download(self,url):

        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "download from "+url+"\n"
        response = requests.get(url=self.url,headers=headers,timeout=5)    # �������GET����

        if response.ok:
            #print response.content
            #return StringIO.StringIO(response.content)
            return response.content


    def run(self):
        data=self.download(self.url)
        self.queue.put((self.sid,data))

class downloadThread(threading.Thread):
    def __init__(self,sid,queue_url):
        threading.Thread.__init__(self)
        self.sid=sid
        self.queue_url=queue_url


    def downfile(self,url):
        headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, compress',
           'Accept-Language': 'en-us;q=0.5,en;q=0.3',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}

        print "start download...",url
        r=requests.get(url,headers=headers,stream=True)
        filename=url.split('/')[-1].strip().replace("?","")
        
        #filename+=str(random.random());
        

        with open(filename,'wb')as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    f.flush()
            print filename,"download ok!"


    def run(self):
        #time.sleep(3)  #����5sһ�£�����̫��ȡ����queue�����ݾͽ�����
        while True:
            if not self.queue_url.empty():
                url=self.queue_url.get()
                if url:
                    print "queue size:",self.queue_url.qsize()
                    self.downfile(url)
                    #print('-----%s------'%(self.name))  
                    #os.system('wget '+url))  
            else:
                break
                
                
class parseThread(threading.Thread):
    def __init__(self,in_queue,out_list,type="jav"):
        threading.Thread.__init__(self)
        self.in_queue=in_queue
        self.out_list=out_list
        self.type=type

    def parseHTML(self,data):
        soup = BeautifulSoup(data,"html.parser")

        divs=soup.find_all('div',class_='video')

        #print divs
        res=[]
        for div in divs:
            a=div.find('a',class_="")
            img=a.find('img')
            res.append((a.get("title"),a.get("href"),img.get("src")))

        #print res
        return res


    def parseHTML2(self,data):
        soup = BeautifulSoup(data,"html.parser")

        divs=soup.find_all('a')

        #print divs
        res=[]
        res.append(soup.title.string )
        for a in divs:
            #res.append((a.string,a['href']))
            res.append(a['href'])

        #print res
        return res

    def parseHTML_btbt(self,data):
        soup = BeautifulSoup(data,"html.parser")

        divs=soup.find_all('a',class_='subject_link')

        #print divs
        res=[]
       
        for a in divs:
            #res.append((a.string,a['href']))
            res.append((a.get_text(),a['href']))

        #print res
        return res

    def parseHTML_cl(self,data):
        soup = BeautifulSoup(data,"html.parser")

        #table=soup.find('table',id='ajaxtable')
        tds=soup.find_all('td',class_='tal')

        #print divs
        res=[]
       
        for td in tds:
            a=td.find('a')
            #res.append((a.string,a['href']))
            res.append((a.get_text(),"http://cl.o3c.me/"+a['href']))

        #print res
        return res

    def parseHTML_cl_detail(self,data):
        soup = BeautifulSoup(data,"html.parser")

        title=soup.title.string
          
        
        div=soup.find('div',class_='tpc_content do_not_catch') #tpc_content do_not_catch
        
        #print div 
        #print divs
        res=[]
       
        img=div.find('img')
        a=div.find('a')
         
        res.append((title,a.get_text(),img['src']))

        return res

          
                                      
    def run2(self):
        while True:
            sid,data=self.in_queue.get()
            if sid==-1:
                break
            if data:
                res=self.parseHTML2(data)
                
                for x,y,z in res:
                    #self.out_queue.put(y.replace("./","http://www.jav11b.com/cn/"))
                    self.out_list.append((x,y,z)) 

    def run(self):
        while True:
            sid,data=self.in_queue.get()
            if sid==-1:
                break
            if data:
                if self.type=='jav':
                    res=self.parseHTML(data)
                    for x,y,z in res:
                         self.out_list.append((x,y))
                elif self.type=='cl':
                    res=self.parseHTML_cl(data)
                    for x,y in res:
                         self.out_list.append((x,y))
                else:
                    res=self.parseHTML(data)
                    for x,y,z in res:
                         self.out_list.append((x,y))


                        
                        
    def run_test(self):
        pass
        #self.downfile("http://10.166.2.206/tool/qd/VCruntimes.zip")


## class end ############################


def down_jav():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

 
    url="http://www.jav11b.com/cn/vl_update.php?&mode=&page="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,4)]

    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!�ȴ�geturl Thread ���
    for t in uts:
        t.join()

    #֪ͨpt�˳�
    q.put((-1,None))

    #!�ȴ�parse Thread ���    
    pt.join()
    
    print "size of urls:",len(urls)

                     
    urlfile="c:\\javurls.txt"                 
    with open(urlfile,"w") as f:
         for x,y,z in  urls:
             #y=y.replace("./?",baseurl+"?")
             q_urls.put(Z)   
             f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+"\n")
      
    print "File saved!",urlfile

    print "size of q_urls:",q_urls.qsize()

                                          
    print "##############################################"
    
    #���������ļ��߳� 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,11)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()


    print "All files download complete!"


def down_btbt():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    url="http://localhost:8080/KManage/btbt.html?id="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,4)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!�ȴ�geturl Thread ���
    for t in uts:
        t.join()

    #֪ͨpt�˳�
    q.put((-1,None))

    #!�ȴ�parse Thread ���    
    pt.join()
    
    print "size of urls:",len(urls)
                     
    urlfile="c:\\btbt.txt"                 
    with open(urlfile,"w") as f:
         for x,y in  urls:
             #y=y.replace("./?",baseurl+"?")
             q_urls.put(y)
             f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\n")
      
    print "url file saved!",urlfile

    print "size of q_urls:",q_urls.qsize()
                                          
    print "##############################################"

    
            
def down_cl():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    url="http://cl.o3c.me/thread0806.php?fid=15&search=&page="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,20)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!�ȴ�geturl Thread ���
    for t in uts:
        t.join()

    #֪ͨpt�˳�
    q.put((-1,None))

    #!�ȴ�parse Thread ���    
    pt.join()
    
    print "size of urls:",len(urls)
                     
    urlfile="c:\\cl.txt"                 
    with open(urlfile,"w") as f:
         for x,y in  urls:
             q_urls.put(y)
             #y=y.replace("./?",baseurl+"?")
             f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\n")
      
    print "url file saved!",urlfile
 
    print "size of q_urls:",q_urls.qsize()
                                          
    print "##############################################"    
 
     #���������ļ��߳� 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,5)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()


    print "All files download complete!"


#txt��δ����Ĳ���
def down_cl_remainder(all_txt,downed_path):
    
    q_urls=Queue.Queue()

    downeds=[x for x in os.listdir(downed_path) if not os.path.isdir(downed_path+"\\"+x)]

    all_urls=[]
    #fullpath_files=[]
    for line in open(all_txt):
        url=line.split("\t")[1]
        p,f=os.path.split(url)
        
        all_urls.append(f.replace("\n",""))

            
    diff=set(all_urls)-set(downeds)

    for x in diff:
        q_urls.put("http://cl.o3c.me/htm_data/15/1703/"+x)

    print q_urls.qsize()


    #���������ļ��߳� 
    
    dts=[downloadThread(i,q_urls) for i in xrange(1,5)]

    for t in dts:
        t.start()

    for t in dts:
        t.join()

    print "Diff files download complete!"

#����cl �򿪵�detailҳ��
def down_cl_detail():
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    url="http://localhost:8080/KManage/cl_detail.html?id="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,4)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!�ȴ�geturl Thread ���
    for t in uts:
        t.join()

    #֪ͨpt�˳�
    q.put((-1,None))

    #!�ȴ�parse Thread ���    
    pt.join()
    
    print "size of urls:",len(urls)
                     
    urlfile="c:\\cl_detail.txt"                 
    with open(urlfile,"w") as f:
         for x,y,z in  urls:
             q_urls.put(z)
             #y=y.replace("./?",baseurl+"?")
             f.write(x.encode("utf8")+"\t"+y.encode("utf8")+"\t"+z.encode("utf8")+"\n")
      
    print "url file saved!",urlfile

    print "size of q_urls:",q_urls.qsize()
    
    print "##############################################"    
    

#�Ƚ�����list�Ĳ��첿��
def comparelist_diff(src,des):
    #src: [("name_str","url")]
    #des: ["url"]  
    
    ret=[] 
    for x,y in src:
        flag=0
        for a in des:
            if y.replace("\n","")==a.replace("\n",""):
                 flag=1
        if flag==0:
            ret.append((x,y)) 

    return ret    

#��ȡĿ¼�µ�txt�ļ���list
def walkcl(path):
    
    files=[x for x in os.listdir(path) if all([os.path.splitext(x)[1]=='.txt', not os.path.isdir(path+"\\"+x)])]
    
    # txtfile=[f for f in files if os.path.splitext(f)[1]=='.txt']
    store=[]
    for txtfile in files:
        for line in open(path+"/"+txtfile):
            url=line.split("\t")[1].replace("\n","")
            store.append(url)
    #print store        
    return store  
                               
#�Ա�cl���ļ�,�õ������д��cl��                 
def cmp_cl_store(store_path,src):
    #src=[("a","c:\\"),("b","c:\\"),("c","c:\\"),("a","d:\\"),("b","e:\\"),("c","e:\\"),("a","c:\\")]    
    #des=["a","b","c"]

    des=walkcl(store_path)
   
    print "cl store total count=",len(des)

    diff=comparelist_diff(src,des)     
    
    if len(diff)==0:
        print "no found diff!"
        return
  
    savefile=store_path+"\\cl_"+ str(random.randint(10,100))+".txt"  
    with open(savefile,"w") as fs:
        for name,url in diff:
             fs.write(name.encode("utf-8")+"\t"+url.encode("utf-8")+"\n")

    print "Found %s url File saved!"%len(diff)
    
    return diff


#����cl���ﲻ���ڵĲ���
def down_cl_diff(cl_store_path):
    
    q=Queue.Queue()
    q_urls=Queue.Queue()
    
    urls=[]

    #url="http://www.btbtt.co/forum-index-fid-1183-typeid1-8-typeid2-0-typeid3-0-typeid4-0-page-19.htm"
    #url="http://cl.o3c.me/thread0806.php?fid=15&search=&page="
    url="http://www.jav11b.com/cn/vl_update.php?&mode=&page="

    uts=[getUrlThread(url+str(i),i,q) for i in xrange(1,3)]
    
    pt=parseThread(q,urls)

    for t in uts:
        t.start()

    pt.start()

    #!�ȴ�geturl Thread ���
    for t in uts:
        t.join()

    #֪ͨpt�˳�
    q.put((-1,None))

    #!�ȴ�parse Thread ���    
    pt.join()


    print "For down urls=",len(urls)

    diff=cmp_cl_store(cl_store_path,urls)

    if len(diff)>0: 
        for name,url in diff:
            #q_urls.put("http://cl.o3c.me/htm_data/15/1703/"+url)
            q_urls.put("http://www.jav11b.com/cn/"+url)

        print "q_urls size:",q_urls.qsize()

        #���������ļ��߳� 
        
        dts=[downloadThread(i,q_urls) for i in xrange(1,5)]

        for t in dts:
            t.start()

        for t in dts:
            t.join()

        print "Diff files download complete!"
        
    



if __name__ == '__main__' :
    
    #down_jav()
    #down_btbt()
    #down_cl()
    #down_cl_detail()
    #down_cl_remainder("c:\\cl.txt","C:\\script\\cl2")
    #STORE_PATH="D:\\avstore\\CL_STORE\\"
    STORE_PATH="D:\\avstore\\jav_store\\"

    down_cl_diff(STORE_PATH)


