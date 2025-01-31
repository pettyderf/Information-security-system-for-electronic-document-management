from sympy import *
import random
from hashlib import sha256

def gost_ep_keys():
    p = 0
    q = random.randint(2**254,2**256)
    while isprime(q) == False:
        q = random.randint(2**254,2**256)
    k = 2**509//q+1
    while isprime(p) == False:
        k += 1
        p = q * k + 1
    print('p = ', p)
    a = 1
    while a == 1:
        d = random.randint(2, p - 2)
        a = st_mod(d,k,p)
    x = random.randint(2, q-1)
    y = st_mod(a,x,p)
    return q,p,a,x,y

def DS_gost(bit,q,p,a,x):
    bitdec = int(bit,16)
    q = int(q)
    p = int(p)
    a = int(a)
    x = int(x)
    if bitdec % q == 0:
        bitdec = 1
    k = random.randint(1,q-1)
    r = (st_mod(a,k,p)) % q
    while r == 0:
        k = random.randint(2, q - 1)
        r = (st_mod(a, k, p)) % q
    s = ((x * r) + (k * bitdec)) % q
    return str(hex(r)) + ' ' + str(hex(s))

def st_mod(bit,d,n):
    d_bit = bin(d)[2:]
    d_bit = d_bit[::-1]
    bit_j = bit
    y = 1
    for i in d_bit:
        if i == '1':
            y = y * bit_j
        bit_j = (bit_j * bit_j) % n
    return y % n

def check_gost_ep(bit, r, s, q, p, a, y):
    bitdec = int(bit, 16)
    r = str(r)
    s = str(s)
    r = int(r, 16)
    s = int(s, 16)
    q = int(q)
    p = int(p)
    a = int(a)
    y = int(y)

    v = st_mod(bitdec, q - 2, q)
    z_1 = (s * v) % q
    z_2 = ((q - r) * v) % q
    u = ((st_mod(a,z_1,p) * st_mod(y,z_2,p)) % p) % q

    if u == r:
        return True
    else:
        return False