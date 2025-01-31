from sympy import *
import math
import random


def keys_RSA():
    p, q = 0, 0
    while isprime(int(p)) == False:
        p = random.randint(1,1000)
    while isprime(int(q)) == False:
        q = random.randint(1,1000)
    N = p * q
    # print('Модуль N = ',N)
    FN = (p-1)*(q-1)
    e = random.randint(2,N)
    while math.gcd(e,FN) != 1 :
        e = random.randint(2,N)
    # print('Открытый ключ e = ',e)
    i = 2
    while (e * i) % FN != 1 and i < N:
        i+=1
        d = i
    # print('Закрытый ключ d = ',d)
    return N, e, d

def cript_rsa(e, N, st):
    kok = []
    out = ''
    for i in st:
        kok.append(ord(i))
    for i in kok:
        c = i**e % N
        out += str(hex(c))
    return out

def encript_rsa(d, N, st):
    kok = []
    out = ''
    for i in range(1,st.count('0x')):
        st = st[2:len(st)]
        j = '0x' + st[:st.find('0x')]
        kok.append(int(j,16))
        st = st[st.find('0x'):len(st)]
    kok.append(int(st,16))      
    for i in kok:
        c = i**d % N
        out += chr(c)
    return out

# choice = int(input('0 - для генерация ключей, 1 - для зашифровки, 2 - для расшифровки :'))
# if choice == 0:
#     keys_RSA()
# elif choice == 1:
#     cript()
# elif choice == 2:
#     encript()
# else:
#     print('введите 0, 1 или 2 блин(')
        
