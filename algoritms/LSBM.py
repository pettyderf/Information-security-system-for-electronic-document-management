from PIL import ImageTk, Image
from random import randint
import numpy as np

def matching(x,ms,rate,iteration):
    x_p, x_m = x, x
    while (bin(x_p)[2:])[-1 * rate:] != ms[iteration:iteration + rate]:
        x_p += 1
    while (bin(x_m)[2:])[-1 * rate:] != ms[iteration:iteration + rate]:
        x_m -= 1
    if x_p > 255:
        return x_m
    elif x_m < 0:
        return x_p
    if x_p - x == x - x_m:
        rand = randint(0,1)
        if rand == 0:
            return x_m
        else:
            return x_p
    elif x_p - x < x - x_m:
        return x_p
    else:
        return x_m

def Encode_LSBM(src, message):
    img = Image.open(src, 'r')
    width, height = img.size
    rate = 3

    message += " end.message."
    b_message = ''.join([format(ord(i), "08b") for i in message])
    pixels = img.load()

    out_img = Image.new("RGB", (width, height))
    new_pixels = out_img.load()
    while len(b_message) % rate != 0:
        b_message += "0"

    if rate * width * height * 3 < len(b_message):
        return "big message"
    else:
        iteration = 0

        for i in range(width):
            for j in range(height):
                r,g,b = pixels[i,j]
                if iteration < len(b_message):
                    r = matching(r,b_message,rate,iteration)
                    iteration += rate
                if iteration < len(b_message):
                    g = matching(g, b_message, rate, iteration)
                    iteration += rate
                if iteration < len(b_message):
                    b = matching(b, b_message, rate, iteration)
                    iteration += rate
                new_pixels[i,j] = (r,g,b)

        return out_img
        # out_img.save(str(src)[:-4] + "_authorship.bmp", format="BMP")

def Decode(src):

    img = Image.open(src, 'r')
    width, height = img.size

    rate = 3

    pixels = img.load()
    hidden_bits = ""

    for i in range(width):
        for j in range(height):
            r, g, b = pixels[i, j]
            r_n = bin(r)[2:]
            if len(r_n) < 8:
                r_n = ("0" * (8 - len(r_n))) + r_n
            g_n = bin(g)[2:]
            if len(g_n) < 8:
                g_n = ("0" * (8 - len(g_n))) + g_n
            b_n = bin(b)[2:]
            if len(b_n) < 8:
                b_n = ("0" * (8 - len(b_n))) + b_n
            hidden_bits += r_n[rate*-1:] + g_n[rate*-1:] + b_n[rate*-1:]

    message = ""
    iter = 1
    if len(hidden_bits) % 8 != 0:
        hidden_bits += "0" * (len(hidden_bits) % 8)
    for i in range(0,len(hidden_bits),8):
        message += chr(int(hidden_bits[i:i+8],2))
        if len(message) / 17 == iter:
            ind = message.find(" end.message.")
            iter += 1
            if ind > 0:
                return message[:ind]

    return "Не обнаружено авторства."

# Encode_LSBM("C:/Users/rem12/Desktop/akon.bmp", 'Autor - Mihalichev Oleg')
# print(Decode("C:/Users/rem12/Desktop/akon_authorship.bmp"))