import random
from sympy import *
import hashlib
S_block = [[1,15,13,0,5,7,10,4,9,2,3,14,6,11,8,12],
           [13,11,4,1,3,15,5,9,0,10,14,7,6,8,2,12],
           [4,11,10,0,7,2,1,13,3,6,8,5,9,12,15,14],
           [6,12,7,1,5,15,13,8,4,10,9,14,0,3,11,2],
           [7,13,10,1,0,8,8,15,14,4,6,12,11,2,5,3],
           [5,8,1,13,10,3,4,2,14,15,12,7,6,0,9,11],
           [14,11,4,12,6,13,15,10,2,3,8,1,0,7,5,9],
           [4,10,9,2,13,8,0,14,6,11,1,12,7,15,5,3]]

S_block_magma = [[1,7,14,13,0,5,8,3,4,15,10,6,9,12,11,2],
                 [8,14,2,5,6,9,1,12,15,4,11,0,13,10,3,7],
                 [5,13,15,6,9,2,12,10,11,7,8,1,4,3,14,0],
                 [7,15,5,10,8,1,6,13,0,9,3,14,11,4,2,12],
                 [12,8,2,1,13,4,15,6,7,0,10,5,3,14,9,11],
                 [11,3,5,8,2,15,10,13,14,1,7,4,12,9,6,0],
                 [6,8,2,3,9,10,5,12,1,14,4,7,11,13,0,15],
                 [12,4,6,2,10,5,11,9,14,8,13,7,0,3,15,1]]

def xor(x,y):
    if x == y:
        return '0'
    else:
        return '1'

def F(L,R,X):
    mod = (int(R,base = 2) + int(X,base = 2)) % 2**32
    mod_2 = bin(mod)[2:]
    if len(mod_2) < 32:
        mod_2 = ('0' * (32-len(mod_2))) + mod_2
    new_mod, output = '',''
    i,k = 0,0
    while i != 32:
        _4_mod = bin(S_block_magma[k][int(mod_2[i] + mod_2[i+1] + mod_2[i+2] + mod_2[i+3],base = 2)])[2:]
        if len(_4_mod) < 4:
            new_mod += ('0' * (4 - len(_4_mod))) + _4_mod
        else:
            new_mod += _4_mod
        i += 4
        k += 1
    new_mod = new_mod[11:] + new_mod[:11]
    for i in range(0,len(new_mod)):
        output += xor(new_mod[i],L[i])
    return R,output

def magma_cript(open_txt,key):
    st_ascii = []
    key_ascii = []
    K = []
    output = ''
    for i in open_txt:
        i_bi = bin(ord(i))[2:]
        while len(i_bi) < 16:
            i_bi = '0' + i_bi
        st_ascii.append(i_bi)
    while (len(st_ascii) * 16) % 64 != 0:
        st_ascii.append('0' * 16)
    for i in range(0, 256, 8):
        key_ascii.append(key[i] + key[i + 1] + key[i + 2] +
                         key[i + 3] + key[i + 4] + key[i + 5] +
                         key[i + 6] + key[i + 7])
    i = 0
    while i < 32:
        K.append(key_ascii[i] + key_ascii[i + 1] + key_ascii[i + 2] + key_ascii[i + 3])
        i += 4
    i = 0
    while len(st_ascii) != i:
        L,R = '',''
        L += st_ascii[i] + st_ascii[i+1]
        R += st_ascii[i+2] + st_ascii[i+3]
        for j in range(0,3):
            for k in range(0,8):
                L,R = F(L,R,K[k])
        for k in range(7,-1,-1):
            L,R = F(L,R,K[k])
        i += 4
        output += L + R

    return output
    # output_mass = []
    # for i in range(0,len(output),16):
    #     output_mass.append(output[i:i+16])
    # close_txt = ''
    # for i in output_mass:
    #     close_txt += chr(int(i,2))
    # return close_txt

def magma_encript(close_txt, key):
    st_ascii = []
    key_ascii = []
    K = []
    output = ''
    for i in range(0,len(close_txt), 16):
        st_ascii.append(close_txt[i:i+16])
    # for i in close_txt:
    #     i_bi = bin(ord(i))[2:]
    #     while len(i_bi) < 16:
    #         i_bi = '0' + i_bi
    #     st_ascii.append(i_bi)
    # while (len(st_ascii) * 16) % 64 != 0:
    #     st_ascii.append('0' * 16)
    for i in range(0, 256, 8):
        key_ascii.append(key[i] + key[i + 1] + key[i + 2] +
                         key[i + 3] + key[i + 4] + key[i + 5] +
                         key[i + 6] + key[i + 7])
    i = 0
    while i < 32:
        K.append(key_ascii[i] + key_ascii[i + 1] + key_ascii[i + 2] + key_ascii[i + 3])
        i += 4
    i = 0
    while len(st_ascii) != i:
        L,R = '',''
        L += st_ascii[i] + st_ascii[i+1]
        R += st_ascii[i+2] + st_ascii[i+3]
        for k in range(0,8):
            R,L = F(R,L,K[k])
        for j in range(0,3):
            for k in range(7,-1,-1):
                R,L = F(R,L,K[k])
        i += 4
        output += L + R
    output_mass = []
    for i in range(0, len(output), 16):
        output_mass.append(output[i:i + 16])
    open_txt = ''
    for i in output_mass:
        open_txt += chr(int(i, 2))
    return open_txt

def cript_gost(open_txt, key):
    # st = (str(open_txt)).encode('cp1251')
    st_ascii = []
    key_ascii = []
    K = []
    output = ''



    for i in str(open_txt):
        i_bi = bin(ord(i))[2:]
        while len(i_bi) < 8:
            i_bi = '0' + i_bi
        st_ascii.append(i_bi)
    while (len(st_ascii) * 8) % 64 != 0:
        st_ascii.append('0' * 8)
    # for i in st:
    #     if len(bin(i)[2:]) == 8:
    #         st_ascii.append(bin(i)[2:])
    #     if len(bin(i)[2:]) < 8:
    #         st_ascii.append(('0'*(8-len(bin(i)[2:])))+bin(i)[2:])
    for i in range(0,256,8):
        key_ascii.append(key[i]+key[i+1]+key[i+2]+key[i+3]+key[i+4]+key[i+5]+key[i+6]+key[i+7])
    i = 0
    while i < 32:
        K.append(key_ascii[i]+key_ascii[i+1]+key_ascii[i+2]+key_ascii[i+3])
        i += 4
    while len(st_ascii) % 8 != 0:
        st_ascii.append('00000000')
    i = 0
    while len(st_ascii) != i:
        L,R = '',''
        L += st_ascii[i] + st_ascii[i+1] + st_ascii[i+2] + st_ascii[i+3]
        R += st_ascii[i+4] + st_ascii[i+5] + st_ascii[i+6] + st_ascii[i+7]
        for j in range(0,3):
            for k in range(0,8):
                L,R = F(L,R,K[k])
        for k in range(7,-1,-1):
            L,R = F(L,R,K[k])
        i += 8
        output += L + R


    output_mass = []
    for i in range(0,len(output),8):
        output_mass.append(output[i:i+8])
    close_txt = ''
    for i in output_mass:
        close_txt += chr(int(i,2))
    return close_txt
    # output = int(output, 2)
    # return str(output.to_bytes((output.bit_length() + 7) // 8, 'big').decode('cp1251'))

def encript_gost(close_txt, key):
    # st = (str(close_txt)).encode('cp1251')
    st_ascii = []
    key_ascii = []
    K = []
    output = ''

    for i in str(close_txt):
        i_bi = bin(ord(i))[2:]
        while len(i_bi) < 8:
            i_bi = '0' + i_bi
        st_ascii.append(i_bi)
    while (len(st_ascii) * 8) % 64 != 0:
        st_ascii.append('0' * 8)
    # for i in st:
    #     if len(bin(i)[2:]) == 8:
    #         st_ascii.append(bin(i)[2:])
    #     if len(bin(i)[2:]) < 8:
    #         st_ascii.append(('0'*(8-len(bin(i)[2:])))+bin(i)[2:])
    for i in range(0, 256, 8):
        key_ascii.append(key[i] + key[i + 1] + key[i + 2] + key[i + 3] + key[i + 4] + key[i + 5] + key[i + 6] + key[i + 7])
    i = 0
    while i < 32:
        K.append(key_ascii[i]+key_ascii[i+1]+key_ascii[i+2]+key_ascii[i+3])
        i += 4
    while len(st_ascii) % 8 != 0:
        st_ascii.append('00000000')
    i = 0
    while len(st_ascii) != i:
        L,R = '',''
        L += st_ascii[i] + st_ascii[i+1] + st_ascii[i+2] + st_ascii[i+3]
        R += st_ascii[i+4] + st_ascii[i+5] + st_ascii[i+6] + st_ascii[i+7]
        for k in range(0,8):
            R,L = F(R,L,K[k])
        for j in range(0,3):
            for k in range(7,-1,-1):
                R,L = F(R,L,K[k])
        i += 8
        output += L + R

    output_mass = []
    for i in range(0, len(output), 8):
        output_mass.append(output[i:i + 8])
    while output_mass[-1] == '00000000':
        del output_mass[-1]
    open_txt = ''
    for i in output_mass:
        open_txt  += chr(int(i, 2))
    return open_txt
    # schet = 0
    # for i in range(len(output)-1,-1,-8):
    #     sum = output[i-7] + output[i-6] + output[i-5] + output[i-4] + output[i-3] + output[i-2] + output[i-1] + output[i]
    #     if sum == '00000000':
    #         schet += 1
    # output = output[:len(output)-(8*schet)]
    # output = int(output,2)
    # return str(output.to_bytes((output.bit_length() + 7) // 8, 'big').decode('cp1251'))

def gen_key_gost(u_name, passwd):
    key_s = str(u_name) + str(passwd)
    key = ''
    for i in key_s: key += str(ord(i))
    key_b = bin(int(key))[2:]
    if len(key_b) > 256:
        key_b = key_b[:256]
    while len(key_b) < 256:
        key_b += key_b + '0'
    return key_b

