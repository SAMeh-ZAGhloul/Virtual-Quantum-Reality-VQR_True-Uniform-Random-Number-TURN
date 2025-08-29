# Loads and displays the results from our slow Java IID test program.
#  Reads the json results file:
#         rank
#         T_i value
#         other T test statistics

import json

import matplotlib.pyplot as plt
import numpy as np

FILENAME = '/tmp/results.json'
with open(FILENAME) as f:
    data = json.load(f)
    rank = data['rank']
    Ti = data['ti']
    print('Rank =', rank)
    statistics = np.array(data['statistics'])
    statistics = statistics / Ti  # Normalise the results
    plt.plot(rank, 1, 'o', color='red', label='Baseline, Ti')
    plt.plot(statistics[2:], color='purple', label='Statistics, T')
    plt.xlabel('Ordered #permutation')
    plt.ylabel('Normalised test statistic')
    plt.legend()
    plt.tight_layout()
    plt.show()
