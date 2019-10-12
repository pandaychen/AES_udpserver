from array import array

"""
from array import array
>>> a="a b c d e f g \0 0 1 2 3 \n"
>>> print array('B',a)
array('B', [97, 32, 98, 32, 99, 32, 100, 32, 101, 32, 102, 32, 103, 32, 0, 32, 48, 32, 49, 32, 50, 32, 51, 32, 10])
>>> print array('B',a)[0]
"""

append_char='\0'

def galois_multiply(a, b):
    p = 0
    while b:
        if b & 1:
            p ^= a
        a <<= 1
        if a & 0x100:
            a ^= 0x1b
        b >>= 1

    return p & 0xff

def sbox():
    sbox = array('B',
        '637c777bf26b6fc53001672bfed7ab76'
        'ca82c97dfa5947f0add4a2af9ca472c0'
        'b7fd9326363ff7cc34a5e5f171d83115'
        '04c723c31896059a071280e2eb27b275'
        '09832c1a1b6e5aa0523bd6b329e32f84'
        '53d100ed20fcb15b6acbbe394a4c58cf'
        'd0efaafb434d338545f9027f503c9fa8'
        '51a3408f929d38f5bcb6da2110fff3d2'
        'cd0c13ec5f974417c4a77e3d645d1973'
        '60814fdc222a908846eeb814de5e0bdb'
        'e0323a0a4906245cc2d3ac629195e479'
        'e7c8376d8dd54ea96c56f4ea657aae08'
        'ba78252e1ca6b4c6e8dd741f4bbd8b8a'
        '703eb5664803f60e613557b986c11d9e'
        'e1f8981169d98e949b1e87e9ce5528df'
        '8ca1890dbfe6426841992d0fb054bb16'.decode('hex'))
    return sbox

def inv_sbox():
    inv_sbox = array('B',
        '52096ad53036a538bf40a39e81f3d7fb'
        '7ce339829b2fff87348e4344c4dee9cb'
        '547b9432a6c2233dee4c950b42fac34e'
        '082ea16628d924b2765ba2496d8bd125'
        '72f8f66486689816d4a45ccc5d65b692'
        '6c704850fdedb9da5e154657a78d9d84'
        '90d8ab008cbcd30af7e45805b8b34506'
        'd02c1e8fca3f0f02c1afbd0301138a6b'
        '3a9111414f67dcea97f2cfcef0b4e673'
        '96ac7422e7ad3585e2f937e81c75df6e'
        '47f11a711d29c5896fb7620eaa18be1b'
        'fc563e4bc6d279209adbc0fe78cd5af4'
        '1fdda8338807c731b11210592780ec5f'
        '60517fa919b54a0d2de57a9f93c99cef'
        'a0e03b4dae2af5b0c8ebbb3c83539961'
        '172b047eba77d626e169146355210c7d'.decode('hex'))
    return inv_sbox

def rcon_table():
    rcon_table = array('B',
         '8d01020408102040801b366cd8ab4d9a'
         '2f5ebc63c697356ad4b37dfaefc59139'
         '72e4d3bd61c29f254a943366cc831d3a'
         '74e8cb8d01020408102040801b366cd8'
         'ab4d9a2f5ebc63c697356ad4b37dfaef'
         'c5913972e4d3bd61c29f254a943366cc'
         '831d3a74e8cb8d01020408102040801b'
         '366cd8ab4d9a2f5ebc63c697356ad4b3'
         '7dfaefc5913972e4d3bd61c29f254a94'
         '3366cc831d3a74e8cb8d010204081020'
         '40801b366cd8ab4d9a2f5ebc63c69735'
         '6ad4b37dfaefc5913972e4d3bd61c29f'
         '254a943366cc831d3a74e8cb8d010204'
         '08102040801b366cd8ab4d9a2f5ebc63'
         'c697356ad4b37dfaefc5913972e4d3bd'
         '61c29f254a943366cc831d3a74e8cb'.decode('hex'))
    return rcon_table


"""
#define ROUNDUP2(X, Y) (((X) + ((Y) - 1)) & ~((Y) - 1))
printf("%d\n",ROUNDUP2(79,16));
"""

def _str_roundto16(data):
    old_len=len(data)
    block_len=16

    if len(data)%block_len==0:
        return data
    new_len= old_len + (block_len - 1) & ~(block_len - 1)

    return data+append_char*(new_len-old_len)

