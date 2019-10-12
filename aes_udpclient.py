#!/usr/bin/python
#-*- coding:utf-8 -*-

#funtion: a simple udp client
__author__ = 'pandaychen'

import socket
import logging
import select
import errno
import socket
import sys
import time
import signal
import sys
import json
import base64


from aes_main import CBCMode, AES
from aes_utils import _str_roundto16
from trans import *

g_key_128="1234567812345678"

g_IV="1234567812345678"

g_serverip = "127.0.0.1"
g_serverport = "8001"

def new(key, IV=None):
    if IV is None:
        raise ValueError
    return CBCMode(AES(key), IV)

g_serverhost = "127.0.0.1"
g_serverport = 8888

#packet receive counter
g_pktcount=0

def UserExit(t_signum, t_stack):
    global pktcount
    print "recv signal:",t_signum,";total count:",g_pktcount
    sys.exit(1)

def UdpPacketEnc(data_str):
    if data_str==None:
        return
    new_data_str=_str_roundto16(data_str)
    #b64key=base64.b64encode(g_key_128)

    encryptor = CBCMode(AES(g_key_128), g_IV)
    encrypted_str = encryptor.encrypt(new_data_str)

    b64en_str=base64.b64encode(encrypted_str)

    print "Encrypted: {}, {} bytes".format(b64en_str, len(b64en_str))

    return b64en_str

def UdpClient(t_serverip,t_serverport):
    global g_pktcount
    server_addr = (t_serverip,t_serverport)

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        port = int(t_serverport)
    except ValueError:
        port = socket.getservbyname(port, 'udp')

    sock.connect((t_serverip, port))

    while True:
        g_pktcount = g_pktcount+1
        data = "the "+str(g_pktcount)+"st packet"
        data=UdpPacketEnc(data)
        sock.sendto(data, server_addr)
        #time.sleep(1)

if __name__ == "__main__":
    #register
    signal.signal(signal.SIGINT, UserExit)
    UdpClient(g_serverhost,g_serverport)
