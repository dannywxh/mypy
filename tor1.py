#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os, re, time, sys
import hashlib, bencode

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


def checkmv(chksrc):

    mv_path="d:\\"
    txtfiles=[]
    
    files= [x for x in  os.listdir(mv_path) if not os.path.isdir(mv_path+"\\"+x)]

    for x in files:
        ff,ext=os.path.splitext(x)
        if ext=='.txt':
            txtfiles.append(x)

    #txtfiles= [y for y in files if os.path.splitext(mv_path+"\\"+y)==".txt"]

    #print txtfiles

    dd=[] 
    for f in txtfiles:
        print "start handle "+f+"\n"
        with open(mv_path+"\\"+f,"r") as fs: 
            for line in fs.readlines():
                p,filename=os.path.split(line)
                dd.append((filename.replace("\n",""),line.replace("\n",""),f))

    #print dd
    dup=[]
    if os.path.isdir(chksrc):
        src= [x for x in os.listdir(chksrc) if not os.path.isdir(chksrc+"\\"+x)]

        for s in src:
            for a,b,c in dd:
                if a==s:
                    dup.append((a,b,c))

    else:
        for a,b,c in dd:
            if a==chksrc:
                dup.append((a,b,c))

    print "found "+str(len(dup))
    print dup

    with open(mv_path+"\\dup.txt","w") as fs: 
        for a,b,c in dup:
            fs.write(a+"\t"+b+"\t"+c+"\n")


def checktor(chksrc):
    tors_path="d:\\"
    
    files= [x for x in  os.listdir(tors_path) if not os.path.isdir(tors_path+"\\"+x)]

    dup=[]
    if os.path.isdir(chksrc):
        src= [x for x in  os.listdir(chksrc) if not os.path.isdir(chksrc+"\\"+x)]

        for s in src:
            for a in files:
                if a==s:
                    dup.append(format_name(s),s)
    else:
        for a in dd:
            if a==chksrc:
                dup.append(format_name(chksrc),chksrc)

    print "found "+str(len(dup))
    print dup

    with open(path+"\\dup.txt","w") as fs: 
        for a,b in dup:
            fs.write(a+"\t"+b+"\n")


def walktest(path):
    for dirpath,dirname,filenames in os.walk(path):
        print filenames


if __name__ == '__main__' :
    #parse("c:\\1.torrent")
    format_name("dsadsa-3232 fds2321fsa")
    checkmv("10.ËÑË÷·þÎñ-dao.avi")

    walktest("d:\\app\\solr\\")