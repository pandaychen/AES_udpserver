#!/usr/bin/env/python
#coding=utf-8

###常用函数的封装

__author__='pandaychen'

import sys
import os
import time
import re
import subprocess

wan_addr_regex=re.compile(r'inet addr:(\S+)\s+')

def GetCmdRetUnix(args, stderr=None):
    #一般获取命令执行结果
    return subprocess.Popen(args, stdout=subprocess.PIPE, stderr=stderr).communicate()[0]


def GetETH0Ip(ethname):
    if ethname == None:
        ethname='eth0'

    msg=GetCmdRetUnix(["/sbin/ifconfig",ethname])
    for line in msg.split("\n"):
        if wan_addr_regex.search(line)!=None:
            return wan_addr_regex.search(line).group(1)

    return None

def LoggingFun(t_filename,t_logcontent):
    logpath = './log/'
    curdate = time.strftime("%Y%m%d")
    newpath = './log/'+t_filename+'_'+curdate

    if os.path.exists(logpath):
        pass
    else:
        os.mkdir(logpath)

    try:
        filehd = open(newpath,'a+')
        newcontent = '['+str(time.strftime("%Y-%m-%d %H:%M:%S"))+']'+t_logcontent+'\n'
        filehd.writelines(newcontent)
        filehd.close()
    except Exception,e:
        pass
"""
uint32_t time33(char const *str, int len)
    {
        unsigned long  hash = 0;
        for (int i = 0; i < len; i++) {
            hash = hash *33 + (unsigned long) str[i];
        }
        return hash;
    }
"""
def Str2int(t_str):
    if t_str == None:
        return None

    hash =0
    for i in range(len(t_str)):
        hash=hash*33+int(ord(t_str[i]))

    return hash
