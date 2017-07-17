#coding=utf8

# -*- coding: utf-8 -*-

import bencode
import sys
import os


reload(sys)
#print sys.getdefaultencoding()
sys.setdefaultencoding('gbk')
print sys.getdefaultencoding()



def torrent2dict(filename):
    f = open(filename, 'rb')
    s = f.read()
    f.close()
    try: 
        d = bencode.bdecode(s)
        return d
    except Exception,e:
        print "bdecode error!"
        return filename


def get_files(filename):
    f = open(filename, 'rb')
    s = f.read()
    f.close()
    
    stream_files=[]
    try: 
        metainfo = bencode.bdecode(s)
        if 'files' in metainfo['info']:  
            dict=metainfo['info']['files']
            
            for d in dict:
                list_info=d["path"]
                #print type(name)
                
                if list_info[1]=='STREAM':
                    stream_files.append(list_info[2])
                    
        for name in stream_files:
            print name
                     
    except Exception,e:
        print "bdecode error!"
   


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

def parse_info(d):
    ''' 
        for k in d.keys():
            if k == 'info':
                continue            
            print k , ' : ' , d[k]

        raw_input()

        info = d.get('info')
        for k in info.keys():
            if k == 'pieces':
                print k, ' : ...'
                continue
            print k, ' : ', info[k]
            raw_input()
    '''
    name=''

    #print type(d)
    if isinstance(d,str):
        name=d

    else:
        info = d.get('info')
       
        for k in info.keys():
            if k == 'name':
                #print k, ':',info[k]
                name=info[k]
                break

    return name


if __name__ == "__main__":
    #fdat = raw_input('please input the torrent file path:')
    #fdat="c:/1.torrent"

    if len(sys.argv) ==2:
        path= sys.argv[1]

        files=[x for x in os.listdir(path) if not os.path.isdir(path+"\\"+x)]
            
        for f in files:
            print '=========== ', f , '===================='

            d = torrent2dict(path+"/"+f)
 
            name=parse_info(d)

            print name.decode('utf-8')

            try:
                os.rename(path+"/"+f,path+"/"+name.decode('utf-8')+'.torrent')
            except Exception,e:
                print e
                #print "rename error!"
    else:
        get_files("c:\\tmp\\1.torrent")           
        
         