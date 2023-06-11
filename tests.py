import os
import numpy as np
import cv2
import matplotlib.pyplot as plt
from encoder import *
from decoder import *

def generate_histogram_entropy(filename):
    img = cv2.imread(filename, 0)
    arr = np.array(img, dtype=np.uint8) 
    
    hist, bins = np.histogram(arr, bins=256, density=False)
    f = os.path.join('./output/histograms/', filename.replace('.pgm', '_hist.png'))
    if os.path.isfile(f):
        pass
    else:
        width = np.diff(bins)
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center, hist, align='center', width=width)
        plt.savefig('./output/histograms/'+filename.replace('.pgm', '_hist.png'))
        plt.clf()
    
    prob_dist = hist / hist.sum()

    img_ent = 0
    for i in prob_dist:
        x = i * np.ma.log(abs(i))
        if x != 0:
            img_ent -= x
    
    return img_ent

if __name__ == '__main__':
    
    M = 10

    # wyznaczyc histogram i entropie danych wejsciowych
    entropies = {}
    code_averages = {}
    results = []
    filenames = [file for file in os.listdir('./') if file[len(file)-4:] == '.pgm']
    for filename in filenames:
        f = os.path.join('./', filename)
        if os.path.isfile(f):
            ent = generate_histogram_entropy(filename)
            entropies[filename[:len(filename)-4]] = ent
            org_size, encoded_size, avg, ratio = run_encode(filename, M)
            results.append((org_size, encoded_size, ratio))
            code_averages[filename[:len(filename)-4]] = avg

    for filename in filenames:
        print(filename + ': ' + str(entropies[filename[:len(filename)-4]]))

    # cut off values to keep chart in scale
    print(M)
    print(code_averages['solid_black'])
    print(code_averages['solid_dots'])
    if code_averages['solid_black'] > 10:
        code_averages['solid_black'] = 10
    if code_averages['solid_dots'] > 10:
        code_averages['solid_dots'] = 10

    # porownac entropie ze srednia dlugoscia bitowa kodu wyjsciowego
    plt.bar([(2.5*i)+0.4 for i in range(len(entropies))], list(code_averages.values()), align='center', label='Average')
    plt.bar([(2.5*i)-0.4 for i in range(len(entropies))], list(entropies.values()), align='center', label='Entropy')
    plt.xticks([2.5*i for i in range(len(entropies))], list(entropies.keys()), rotation=70)
    plt.legend()
    plt.title('Porównanie entropii i długości dla M=' + str(M))
    plt.tight_layout()
    plt.savefig('./output/entropies_' + str(M) + '.png')
    
    # przetestowac algorytm na obrazach
    with open('./output/results_' + str(M) + '.txt', 'w') as f:
        cols = ['file', 'original size', 'encoded size', 'coding ratio']
        for col in cols:
            f.write(col + '\t')
        f.write('\n')
        for i in range(len(filenames)):
            f.write(filenames[i] + '\t')
            f.write(str(results[i][0]) + '\t')
            f.write(str(results[i][1]) + '\t')
            f.write(str(results[i][2]) + '\t')
            f.write('\n')
        
    # ocenic efektywnosc algorytmu do kodowania obrazow naturalnych

    print('done.')