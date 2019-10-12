#coding=utf-8

"""
实现简单的AES加密-CBC模式
"""

__author__='pandaychen'

from array import array
from aes_utils import sbox, inv_sbox, rcon_table, galois_multiply

sbox = sbox()
inv_sbox = inv_sbox()
rcon_table = rcon_table()
key_size = None

class AES(object):
    block_size = 16

    def __init__(self, key):
        self.key_expansion(key)

    def key_expansion(self, key):
        self.key = key
        self.key_size = len(key)
        if self.key_size == 16:
            self.rounds = 10
        elif self.key_size == 24:
            self.rounds = 12
        elif self.key_size == 32:
            self.rounds = 14
        else:
            raise ValueError

        expanded_key = array('B', self.key)
        keypart = expanded_key[-4:]
        for cycle in xrange(1, 11):
            keypart = keypart[1:4] + keypart[0:1]
            for byte in xrange(4):
                keypart[byte] = sbox[keypart[byte]]
            keypart[0] ^= rcon_table[cycle]
            for z in xrange(4):
                for j in xrange(4):
                    keypart[j] ^= expanded_key[-self.key_size + j]
                expanded_key.extend(keypart)
            if len(expanded_key) >= (self.rounds + 1) * self.block_size:
                break
		
        self.exkey = expanded_key

    def add_round_key(self, data, round):
        offset = round * 16
        exkey = self.exkey
        for i in xrange(16):
            data[i] ^= exkey[offset + i]

    def sub_bytes(self, data, sbox):
        for i in xrange(16):
            data[i] = sbox[data[i]]

    def shift_rows(self, data):
        data[1], data[5], data[9], data[13]     = data[5], data[9], data[13], data[1]
        data[2], data[6], data[10], data[14]    = data[10], data[14], data[2], data[6]
        data[3], data[7], data[11], data[15]    = data[15], data[3], data[7], data[11]

    def shift_rows_inv(self, data):
        data[5], data[9], data[13], data[1]     = data[1], data[5], data[9], data[13]
        data[10], data[14], data[2], data[6]    = data[2], data[6], data[10], data[14]
        data[15], data[3], data[7], data[11]    = data[3], data[7], data[11], data[15]

    def mix_columns(self, data):
        mul_by_2 = array('B', [galois_multiply(x, 2) for x in range(256)])
        mul_by_3 = array('B', [galois_multiply(x, 3) for x in range(256)])
        for column in xrange(0, 16, 4):
            v0, v1, v2, v3 = data[column:column + 4]
            data[column] = mul_by_2[v0] ^ v3 ^ v2 ^ mul_by_3[v1]
            data[column + 1] = mul_by_2[v1] ^ v0 ^ v3 ^ mul_by_3[v2]
            data[column + 2] = mul_by_2[v2] ^ v1 ^ v0 ^ mul_by_3[v3]
            data[column + 3] = mul_by_2[v3] ^ v2 ^ v1 ^ mul_by_3[v0]

    def mix_columns_inv(self, data):
        mul_by_9 = array('B', [galois_multiply(x, 9) for x in range(256)])
        mul_by_11 = array('B', [galois_multiply(x, 11) for x in range(256)])
        mul_by_13 = array('B', [galois_multiply(x, 13) for x in range(256)])
        mul_by_14 = array('B', [galois_multiply(x, 14) for x in range(256)])
        for column in xrange(0, 16, 4):
            v0, v1, v2, v3 = data[column:column + 4]
            data[column] = mul_by_14[v0] ^ mul_by_9[v3] ^ mul_by_13[v2] ^ mul_by_11[v1]
            data[column + 1] = mul_by_14[v1] ^ mul_by_9[v0] ^ mul_by_13[v3] ^ mul_by_11[v2]
            data[column + 2] = mul_by_14[v2] ^ mul_by_9[v1] ^ mul_by_13[v0] ^ mul_by_11[v3]
            data[column + 3] = mul_by_14[v3] ^ mul_by_9[v2] ^ mul_by_13[v1] ^ mul_by_11[v0]

    def encrypt_block(self, data):
        self.add_round_key(data, 0)
        for round in xrange(1, self.rounds):
            self.sub_bytes(data, sbox)
            self.shift_rows(data)
            self.mix_columns(data)
            self.add_round_key(data, round)

        self.sub_bytes(data, sbox)
        self.shift_rows(data)
        self.add_round_key(data, self.rounds)

    def decrypt_block(self, data):
        self.add_round_key(data, self.rounds)
        for round in xrange(self.rounds-1, 0, -1):
            self.shift_rows_inv(data)
            self.sub_bytes(data, inv_sbox)
            self.add_round_key(data, round)
            self.mix_columns_inv(data)

        self.shift_rows_inv(data)
        self.sub_bytes(data, inv_sbox)
        self.add_round_key(data, 0)

class CBCMode(object):
    def __init__(self, cipher, IV):
        self.cipher = cipher
        self.block_size = cipher.block_size
        self.IV = array('B', IV)

    def encrypt(self, data):
        block_size = self.block_size
        if len(data) % block_size != 0:
            raise ValueError

        data = array('B', data)
        IV = self.IV
        for offset in xrange(0, len(data), block_size):
            block = data[offset:offset+block_size]
            for i in xrange(block_size):
                block[i] ^= IV[i]
            self.cipher.encrypt_block(block)
            data[offset:offset+block_size] = block
            IV = block

        self.IV = IV
        return data.tostring()

    def decrypt(self, data):
        block_size = self.block_size
        if len(data) % block_size != 0:
            raise ValueError

        data = array('B', data)
        IV = self.IV
        for offset in xrange(0, len(data), block_size):
            ctext = data[offset:offset+block_size]
            block = ctext[:]
            self.cipher.decrypt_block(block)
            for i in xrange(block_size):
                block[i] ^= IV[i]
            data[offset:offset+block_size] = block
            IV = ctext

        self.IV = IV
        return data.tostring()


#####################################################
################USE FOR TEST########################


