#coding=utf-8

import array
import binascii
import os


def str_to_hexarray(t_str):
    if t_str==None:
        return

    tlist=array.array('B',t_str)

    return [hex(i) for i in tlist]

def str_to_binarray(t_str):
    if t_str==None:
        return

    tlist=array.array('B',t_str)
    return [i for i in tlist]




if __name__=='__main__':
    print str_to_hexarray("abcdefghijkmno!@#$%^&*()")
    print str_to_binarray("abcdefghijkmno!@#$%^&*()")