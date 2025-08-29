"""
IID test using permutation testing theory.
Ref. NIST Special Publication 800-90B,
(https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-90B.pdf) ,
Recommendation for the Entropy Sources Used for Random Bit Generation,
Sections 5.1 & 5.1.1.

Ho is that the data is IID.

This only works for continuous binary data.  ASCII data with  words and
line terminations (and delimiters like tabs, commas and spaces) is obviously
correlated. Aim for a sample file of 10 MB size which allows the
compressor to work on a 1 MB sub-set.

See https://www.statology.org/binomial-test-python/ for the main test.

This program runs from the command line as:-
python  iid-test.py  sample-filename

You may experience errors like "libGL error: MESA-LOADER: failed to open iris: /usr..."
which is to do with your particular Python environment. The program will still work :-)
See https://askubuntu.com/questions/1352158/libgl-error-failed-to-load-drivers-iris-and-swrast-in-ubuntu-20-04
and  setting "export MESA_LOADER_DRIVER_OVERRIDE=i965" worked for me.
"""

import bz2
import random
import sys
from pathlib import Path

import matplotlib.pyplot as plt  # Notice this import!   <<<<<<<<<<<
from scipy.stats import binomtest  # Notice this import!   <<<<<<<<<<<

heads = tails = edges = 0.0
FILENAME = sys.argv[1]
P_MIN = 0.05  # as per standard statistics alpha confidence level.
NO_TESTS = 10
NO_COMPRESSORS = 1

# Check the size of the sample file.
# There is no official lower bound on the size.
file = Path(FILENAME)
file_size = file.stat().st_size
segment_size = file_size // NO_TESTS

nts = []

print('\n\nRunning tests...')
with open(FILENAME, 'rb') as f:
    for i in range(NO_TESTS):
        segment = bytearray(f.read(segment_size))
        compressed_segment_size = len(bz2.compress(segment, compresslevel=9))
        random.shuffle(segment)
        compressed_shuffled_segment_size = len(bz2.compress(segment, compresslevel=9))
        ratio = compressed_shuffled_segment_size / compressed_segment_size
        nts.append(ratio)
        print("NTS =", ratio)
        # print(compressed_shuffled_segment_size, ",", compressed_segment_size)

# Tally the results as edges, heads and tails.
for test_score in nts:
    if test_score < 1:
        heads += 1
    elif test_score > 1:
        tails += 1
    else:
        heads += 0.5
        tails += 0.5
        edges += 1

# Summary results.
print('-----------------------------------')
print('Broke file into {:,}'.format(segment_size), 'byte segments.')
print('Tested {:,}'.format(NO_TESTS * segment_size), 'bytes for each compressor.')
print('Using', NO_COMPRESSORS, 'compressors.')
print('Minimum NTS =', min(nts))
print('Maximum NTS =', max(nts))
print('Mean NTS =', sum(nts) / len(nts))
print('{:.1%}'.format(edges / len(nts)), 'unchanged by shuffle.')

# Perform Binomial test.
# Decimals get rounded to the nearest integers. That's a max. error of 1/2 head. I can live with that.
h = round(heads)
t = (NO_TESTS * NO_COMPRESSORS) - h
result = binomtest(h, n=(NO_TESTS * NO_COMPRESSORS), p=0.5)  # p = 0.5 assuming a fair coin, Ho.
pv = result.pvalue
print('Probability of', h, 'heads and', t, 'tails =', '{:.4f}'.format(pv))

# Result
if pv < P_MIN:
    print('\n\nReject Ho.  Not IID!')
else:
    print('\n\n*** Accept Ho. The data file looks like IID ***')

# Graphs.
nts.sort()
tally = [h, t]
fig, (ay1, ay2) = plt.subplots(2, 1)
ay1.bar(range(NO_TESTS * NO_COMPRESSORS), nts, color='purple')
ay1.set_ylabel('Normalised test statistic')
ay1.set_xlabel('Ordered #permutation')
ay1.set_ylim(min(nts), max(nts))  # Scale axis to look interesting.
ay1.grid(True)

# ay2.title('Coin equivalence')
labels = ['Heads', 'Tails']
colors = ['blue', 'red']
patches, texts = ay2.pie(tally, colors=colors)
ay2.legend(patches, labels, loc="best")
ay2.text(1.7, 0, 'p = {:.4f}'.format(pv), fontsize=14)
ay2.axis('equal')

plt.tight_layout()
plt.show()
