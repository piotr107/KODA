import cv2
import math
import pickle

from utils import *

M = 3


def encode_golomb(n, m):
    q1 = (n / m)
    q = math.floor(q1)
    unary_code = unary(q)
    k1 = math.log(m, 2)
    k = math.ceil(k1)
    c = ((2 ** k) - m)
    r = n % m
    if 0 <= r < c:
        r1 = rem_trun(r, k - 1)
    else:
        r1 = rem_trun(r + c, k)
    res = unary_code + r1
    return res


def save_to_file(data):
    with open('./encoded_data.data', 'wb') as filehandle:
        # Store the data as a binary data stream
        pickle.dump(data, filehandle)


def run_encode(filename, m):
    img = cv2.imread('./barbara.pgm', 0)
    h = img.shape[0]
    w = img.shape[1]

    result = ''
    for y in range(0, h):
        for x in range(0, w):
            result += encode_golomb(img[y, x], M)
    save_to_file([img.shape, M, result])

    # original image size in bits
    org_size = h * w * 8
    encoded_size = len(result)
    coding_ratio = encoded_size / org_size
    return org_size, encoded_size, coding_ratio


if __name__ == '__main__':
    result = run_encode('barbara.pgm', M)
    print(result)
