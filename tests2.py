# testy skupione na obliczaniu m dla poszczegolnych obrazow

from encoder import *

def calc_p_m(filename):
    img = cv2.imread(filename, 0)
    h = img.shape[0]
    w = img.shape[1]

    num_0 = 0
    num_1 = 0
    for y in range(0, h):
        for x in range(0, w):
            num_0 += unary(img[y, x]).count('0')
            num_1 += unary(img[y, x]).count('1')
    bit_len = num_0 + num_1
    p = num_0 / bit_len
    m = -math.log(p, 2)
    m = math.ceil(m)
    return p, m

if __name__ == '__main__':
    results = []

    with open('./output/results.txt', 'w') as f:
        cols = ['file', 'm', 'original size', 'encoded size', 'coding ratio']
        for col in cols:
            f.write(col + '\t')
        f.write('\n')
        filenames = ['solid_dots.pgm', 'geometr_05.pgm', 'geometr_09.pgm', 'geometr_099.pgm']
        for filename in filenames:
            p, m = calc_p_m(filename)
            print((p, m))
            org_size, encoded_size, ratio = run_encode(filename, m)
            results.append((org_size, m, encoded_size, ratio))

        for i in range(len(filenames)):
            f.write(filenames[i] + '\t')
            f.write(str(results[i][0]) + '\t')
            f.write(str(results[i][1]) + '\t')
            f.write(str(results[i][2]) + '\t')
            f.write(str(results[i][3]) + '\t')
            f.write('\n')