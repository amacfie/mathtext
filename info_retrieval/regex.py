from pathlib import Path
import glob
import json
import multiprocessing
import psutil
import re
import sys
import tqdm

NUM_CORES = psutil.cpu_count(logical=False)
if len(sys.argv) < 2:
    sys.exit('pass regex as argument')
QUERY = sys.argv[1]
print(f'Searching for {QUERY}')

with open('../data/index.json') as f:
    index = json.load(f)

def search(key):
    fn = '../data/documents/' + key
    text = Path(fn).read_text()
    if re.search(QUERY, text):
        return key
    else:
        return None

if __name__ == '__main__':  # req'd apparently
    with multiprocessing.Pool(NUM_CORES) as pool:
        # https://stackoverflow.com/a/45276885
        results = list(tqdm.tqdm(
            pool.imap(search, index.keys()),
            total=len(index.keys()),
        ))
    positives = [ result for result in results if result is not None ]
    print(f'{len(positives)} matches found.')
    print(json.dumps({
        positive: index[positive] for positive in positives
    }, indent=2))

