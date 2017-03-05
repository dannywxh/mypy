#coding=gbk

import os
from os.path import join, getsize
import sys

import re



'''
get_exist_byfile:
    实现文件里的名称与txt库里比较,
    得到已存在的list

get_exist_bypath:
   实现目录下的torrent文件与txt库里比较,
    得到重复的torrrent list

find_mv_from_store:
    根据vid 查找
     
arrange_name功能:
    实现wm番号的整理,
    得到整理后的文件wm.txt

'''



reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('gbk')
print sys.getdefaultencoding()


#####for wm ############################################33

def format_str(str):
        #str = '100713_110-ipon-high'
        split_str="_" 

        ls=str.split(split_str)

        date=ls[0]
        year=date[4:]
        md=date[0:4]

        new_str=year+md+split_str+"".join(ls[1:])

        #print new_str

        return new_str 


def arrange_name(filelist):
    arranged=[]

    for old_name in filelist:
        fn,ext=os.path.splitext(old_name)
        new_name=format_str(fn)+ext

        arranged.append((old_name,new_name))

    print arranged
   

    dup_file=open("c:/wm.txt","w")
    try:
        for file in arranged:
            ls=list(file) #touple转list

            dup_file.write("\t".join(ls))

            dup_file.write("\n")

            #html_file.write('<br>')    
    except Exception,e:
        print e

######end  for wm ###################



def format_rule1(s):
        rs=s.strip()
        rs=rs.replace("-","")
        rs=rs.replace(" ","")
        rs=rs[0:7]
        rs=rs.lower()
        return rs


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
        rs=rs.lower()
        return rs



def test_rule2(txtPath):
     v_ids=[]

     for f in os.listdir(txtPath):
         txtf=open(txtPath+"/"+f)
         for line in txtf.readlines():
             p,v_id=os.path.split(line)
             v_id=format_rule2(v_id)
             #print v_id

             v_ids.append((v_id,line))
         txtf.close()

     #print v_ids

     rule_file=open("c:/work/rule_test.txt","w")
     for ff,f in v_ids:
        rule_file.write(f.strip()+'\t'+ff+'\n')
    
     rule_file.close()


'''
  格式 abp471   xxx     ssss
'''

def get_vids_by_text1(txtPath):
     v_ids=[]
     
     for f in os.listdir(txtPath):
         txtf=open(txt_path+"/"+f)
         for line in txtf.readlines():
             v_id=line.split("\t")[0]
             v_id=format_rule2(v_id)
             #print v_id

             v_ids.append(v_id)
         txtf.close()

     return v_ids


'''
  格式: F:\1111\avok\abp471_0001.avi
'''
def get_vids_by_text2(txtPath):
     v_ids=[]
     
     for f in os.listdir(txtPath):
         txtf=open(txtPath+"/"+f)
         for line in txtf.readlines():
             p,v_id=os.path.split(line)
             v_id=format_rule2(v_id)
             #print v_id

             v_ids.append(v_id)
         txtf.close()
     return v_ids



def find_mv_from_store(vid):
    store_info=[] 
    txtPath="c:/work/diskinfo/"
    for f in os.listdir(txtPath):
         txtf=open(txtPath+"/"+f)
         for line in txtf.readlines():
             p,v_id=os.path.split(line)

             v_id=format_rule2(v_id)

             store_info.append((v_id,f,line)) 
    
    flag=0 
    for v in store_info:
        v_id=v[0]

        if v_id==vid:
             
            print "found movie, at {0} {1}".format(v[2].strip(),v[1])
            flag=1
            break

    if flag==0:
        print "Can't find movie!"
         


def check_exist_from_store(flist):
    exist_vids=[]

    txtPath="c:/work/diskinfo/"
    v_ids=get_vids_by_text2(txtPath)

     
    for f in flist:
        for v_id in v_ids:
            
            ff=format_rule2(f)

            if v_id==ff:
                exist_vids.append((ff,f.strip()))
                break


    return exist_vids


#参数为目录名:c:\torrent\
def get_exist_bypath(path):
    flist=[]

    exist_list=[]

    for f in os.listdir(path):
        flist.append(f)

    exist_list=check_exist_from_store(flist)

    dup_file=open(torPath+"/dup.txt","w")
    for ff,f in exist_list:
        dup_file.write('move "'+f+'" c:/\n')
    
    dup_file.close()

    print duplicate_torrents


#参数为文件名:c:\test.txt
def get_exist_byfile(txtfile):
    flist=[]

    exist_list=[]

    fp=open(txtfile)
    for f in fp.readlines():
        flist.append(f)

    exist_list=check_exist_from_store(flist)

    print exist_list

    for ff,f in exist_list:
        find_mv_from_store(ff)


# find store's duplicate file
def findDup():
        
        #txtPath="c:/work/diskinfo/"
        txtPath="c:/avstore/"
        stores=[] 
        d = {}

        for txtf in os.listdir(txtPath):
            for line in open(txtPath+"/"+txtf):
                p,f=os.path.split(line)

                ff=format_rule2(f)

                stores.append((ff,f,p,txtf))    #记录文件的原始名和路径

                d[ff] = d.get(ff, 0) + 1 

        dupId=[]  

        for k, v in d.items():
            if v > 1: 
                dupId.append(k)

        while '' in dupId:  #delete 空元素
            dupId.remove('')

        print "found %s record!"%len(dupId)

        dupFiles=[]  
 
        for id in dupId:
            #print "format %s ..."%id
            for s in stores:
                #('ABP-084\tABP-084 \xe5\xb0\x8b\xe5\xb8\xb8\xe3\x81\t2014-01-01\t', 'a-b.txt')
                #now is : ('ABP084','ABP-084.avi','E:\MV\OK','a-b.txt')
                v_id=s[0]

                #print "format %s to %s"%(id,s_id)

                if v_id==id:
                    #print "formated %s"%id
                    dupFiles.append(s)


        fd = open('c:/dup.txt', 'w')
        for data in dupFiles:
            #print data[0].strip()+"\t"+data[1]
            fd.write(data[0].strip()+"\t"+data[1].strip()+"\t"+data[2].strip()+"\t"+data[3].strip()+"\n")
       
        fd.close()

        print "....done! write in c:/dup.txt.."  


def gen_move_dupfile_cmd():

    # dup.txt格式：agemix-144.avi	201602.txt	F:\av2016

    dup_file="c:/dup.txt"

    cmd="" 
    fd = open(dup_file)

    #for line in os.listdir(dup_file):
    for line in fd.readlines():
         f=line.split("\t")[0]
         fullpath=line.split("\t")[2].strip()
         txtfile=line.split("\t")[1]
         drv,path=os.path.splitdrive(fullpath)

         target_file=f
         if fullpath!="":
             target_file=os.path.join(path[1:],f) #path[1:] 删除第一个字符'\'

         cmd+='move "{0}" .'.format(target_file)+"\n"
         
    fd = open('c:/dup_move_cmd.txt', 'w')
    fd.write(cmd)
       
    fd.close()

    print "..gen cmd..done! write in c:/work/c:/work/dup_move_cmd.txt.."  



def get_all_vid():
        
        txtPath="c:/work/diskinfo/"
        stores=[] 
    
        for txtf in os.listdir(txtPath):
            for line in open(txtPath+"/"+txtf):
                p,f=os.path.split(line)
  
                ff=format_rule2(f)

                stores.append((ff,f))


        fd = open('c:/work/vids.txt', 'w')
        for data in stores:
            #print data[0].strip()+"\t"+data[1]
            fd.write(data[0].strip()+"\t"+data[1])
       
        fd.close()

        print "....done! write in c:/work/vids.txt.."  


def search_vid(param):
        
        txtPath="c:/work/diskinfo/"
        stores=[] 
    
        for txtf in os.listdir(txtPath):
            for line in open(txtPath+"/"+txtf):
                p,f=os.path.split(line)
  
                ff=format_rule2(f)

                if ff.startswith(param):
                    stores.append((ff,f))

        print "find {0} count!".format(len(stores))
        
        raw_input()

        print stores  







##########################################################

if __name__ == '__main__' :
    if len(sys.argv) ==2:
        param= sys.argv[1]

        #get_exist_bypath(param)

        #get_exist_byfile(param)
        
        #findDup()

        gen_move_dupfile_cmd()
        
        #find_phyfile_by_dup(param)

        
        #get_all_vid()
        
        #search_vid(param)

        raw_input()
    else:
        while True:
            print "please input vid:"
            vid=raw_input()
            print vid
            find_mv_from_store(vid)
        #print "useage: avhandle.py PATH" 
