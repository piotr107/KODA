import cv2
import math
import pickle
import numpy as np

from utils import *

M = 4


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


if __name__ == '__main__':
    # load the image
    img = cv2.imread('./barbara.pgm', 0)
    # get binary representation of image as string
    binary_code = ''.join(np.unpackbits(img).astype(str))
    # compress binary code as length of zeros arrays
    compressed_code = list(map(len, binary_code.split('1')))
    # list of M values for map function
    M_list = [M] * len(compressed_code)
    # encode compressed code
    result = list(map(encode_golomb, compressed_code, M_list))
    # save tuple (M, result) to file
    save_to_file([M, result])
