from pathlib import Path
from unidecode import unidecode
import glob
import json
import multiprocessing
import os
import psutil

NUM_CORES = psutil.cpu_count(logical=False)

def proc(key):
    fn = './documents/' + key
    print(fn)
    try:
        text = Path(fn).read_text()
        text = unidecode(text)
        with open(fn, 'w') as f:
            f.write(text)
    except:
        return key

with open('index.json') as f:
    index = json.load(f)

with multiprocessing.Pool(NUM_CORES) as pool:
    results = pool.map(proc, index.keys())
    for result in results:
        if result is not None:
            os.remove('./documents/' + result)
            del index[result]

with open('./index.json', 'w') as f:
    json.dump(index, f, indent=2)

