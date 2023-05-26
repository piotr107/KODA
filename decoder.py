import pickle

import numpy as np
import cv2
import math
import textwrap

from utils import decompress_code


def decode_golomb(code, m):
    code = list(code)
    k1 = math.log(m, 2)
    k = math.ceil(k1)
    c = ((2 ** k) - m)
    q = 0
    for i in range(len(code)):
        if int(code[i]) == 1:
            q = q + 1
        else:
            break
    for i in range(q + 1):
        code.pop(0)
    r1 = []
    for i in range(k - 1):
        r1.append(code[i])
    r2 = [str(i) for i in r1]
    r3 = "".join(r2)
    r = int(r3, 2)
    if r < c:
        return q * m + r
    else:
        r1 = []
        for i in range(k):
            r1.append(code[i])
        r2 = [str(i) for i in r1]
        r3 = "".join(r2)
        rc = int(r3, 2)
        return q * m + rc - c


def loadData() -> list:
    with open('./encoded_data.data', 'rb') as filehandle:
        return pickle.load(filehandle)


if __name__ == '__main__':
    encoded_data = loadData()
    img_shape = encoded_data[0]
    m = encoded_data[1]
    encoded_img = encoded_data[2]
    # list of M values for map function
    m_list = [m] * len(encoded_img)
    # decode compressed code
    decoded_img = list(map(decode_golomb, encoded_img, m_list))
    # decompress code
    decompressed_img = list(map(decompress_code, decoded_img))
    # remove redundant element after operation
    decompressed_img.pop()
    # get 8 bits array
    decompressed_img = textwrap.wrap(''.join(decompressed_img), 8)
    # init image
    img = np.zeros(img_shape, np.uint8)
    # create decoded image
    it = 0
    for y in range(0, img_shape[0]):
        for x in range(0, img_shape[1]):
            img[y][x] = int(decompressed_img[it], 2)
            it = it + 1

    cv2.imwrite('decoded_barbara.pgm', img)
    cv2.imshow('Decoded image', img)
    cv2.waitKey(0)



