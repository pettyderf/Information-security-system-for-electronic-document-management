from sympy import *
import math
import random
from hashlib import sha256
from tkinter import Tk
from tkinter.filedialog import askopenfilename

def extendEvklid(N, m):
    if N == 0:
        return m, 0, 1
    mod, x1, y1 = extendEvklid(m % N, N)
    x = y1 - (m // N) * x1
    y = x1
    return mod, x, y

def invE(N, m):
    nod, x, y = extendEvklid(N, m)
    if nod == 1:
        z = (x % m + m) % m
        return z
    else:
        return -1

def keys():
    p = 0
    q = 0
    while isprime(int(p)) == False:
        p = random.getrandbits(256)
    while isprime(int(q)) == False:
        q = random.getrandbits(256)
    N = p * q
    print('N = ',N)
    FN = (p-1)*(q-1)
    e = random.randint(2,FN-1)
    while math.gcd(e,FN) != 1 :
        e = random.randint(2,FN-1)
    print('e = ',e)
    d = invE(e,FN)
    print('d = ',d)

def DS():
    Tk().withdraw()
    filename = askopenfilename()
    bit = sha256(open(filename,'rb').read()).hexdigest()
    bitdec = int(bit,16)
    d = int(input('Введите закрытый ключ: '))
    N = int(input('Введите модуль: '))
    s = st_mod(bitdec,d,N)
    print(hex(s))

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

def proverka():
    Tk().withdraw()
    filename = askopenfilename()
    bit = sha256(open(filename, 'rb').read()).hexdigest()
    bitdec = int(bit, 16)
    podpis = str(input('Введите ЭЦП: '))
    podpis = int(podpis,16)
    e = int(input('Введите открытый ключ: '))
    N = int(input('Введите модуль: '))
    h = st_mod(podpis,e,N)
    if bitdec == h:
        print('Подпись действительна')
    else:
        print('Подпись недействительна')

keys()
DS()
proverka()
