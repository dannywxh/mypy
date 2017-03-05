#coding=utf8

# -*- coding: utf-8 -*-

import bencode
import sys
import os


reload(sys)
#print sys.getdefaultencoding()
#sys.setdefaultencoding('gbk')
print sys.getdefaultencoding()



def torrent2dict(filename):
    f = open(filename, 'rb')
    s = f.read()
    f.close()
    d = bencode.bdecode(s)
    return d


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
    info = d.get('info')
    name=''
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
        root_path= sys.argv[1]

        for f in os.listdir(root_path):
            print '=========== ', f , '===================='

            d = torrent2dict(root_path+"/"+f)

            name=parse_info(d)

            print name.decode('utf-8')

            os.rename(root_path+"/"+f,root_path+"/"+name.decode('utf-8')+'.torrent')