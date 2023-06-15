import pickle

import numpy as np
import cv2
import math


def get_word_length(code, m):
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
    new_code = code[q + 1:]
    r1 = []
    for i in range(k - 1):
        r1.append(new_code[i])
    r2 = [str(i) for i in r1]
    r_length = len(r2)
    r3 = "".join(r2)
    r = int(r3, 2)
    if r >= c:
        r_length += 1
    return q + 1 + r_length


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
    img = np.zeros(img_shape, np.uint8)
    max_window = 256 + math.ceil(math.log(m, 2))
    decoded_values = []
    current_index = 0
    while current_index < len(encoded_img):
        word_length = get_word_length(encoded_img[current_index:current_index + max_window], m)
        decoded_values.append(decode_golomb(encoded_img[current_index: current_index + word_length], m))
        current_index += word_length

    values_index = 0
    for y in range(0, img_shape[0]):
        for x in range(0, img_shape[1]):
            img[y][x] = decoded_values[values_index]
            values_index += 1
    cv2.imshow('Decoded image', img)
    cv2.waitKey(0)
