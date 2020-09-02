from pathlib import Path
import glob
import os
import random

try:
    os.remove('./train.txt')
except OSError:
    pass
try:
    os.remove('./test.txt')
except OSError:
    pass
with open('./test.txt', 'w') as f:
    f.write('<|endoftext|>')
with open('./train.txt', 'w') as f:
    f.write('<|endoftext|>')

for fn in glob.glob('./m_se_a_*.txt'):
    print(fn)
    if random.random() <= 0.8:
        with open('./train.txt', 'a') as f:
            f.write(Path(fn).read_text() + '<|endoftext|>')
    else:
        with open('./test.txt', 'a') as f:
            f.write(Path(fn).read_text() + '<|endoftext|>')

