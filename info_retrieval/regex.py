from pathlib import Path
import glob
import multiprocessing
import psutil

NUM_CORES = psutil.cpu_count(logical=False)
QUERY = '\sqrt{x} + \sqrt{y} + \sqrt{z}'

def search(fn):
    text = Path(fn).read_text()
    if QUERY in text:
        return fn
    else:
        return None

with multiprocessing.Pool(NUM_CORES) as pool:
    results = pool.map(search, glob.glob('../data/documents/*'))
    print(f'Searched {len(results)} files.')
    positives = [ result for result in results if result is not None ]
    if positives:
        print(''.join(positives))
    else:
        print('No matches found.')

