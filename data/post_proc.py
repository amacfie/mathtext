from pathlib import Path
from unidecode import unidecode
import multiprocessing
import os
import pickle
import psutil
import re
import tqdm

NUM_CORES = psutil.cpu_count(logical=False)

def proc(key):
    fn = './documents/' + key
    try:
        text = Path(fn).read_text()
        text = unidecode(text)

        # clean whitespace
        # https://en.wikibooks.org/wiki/LaTeX/Basics#Spaces
        text = re.sub(r'\t', ' ', text)
        text = re.sub(
            r'\s+\n\s*\n\s*|\s*\n\s+\n\s*|\s*\n\s*\n\s+', '\n\n', text
        )
        # doesn't get rid of single newlines just cleans spaces around them
        text = re.sub(r' +\n *| *\n +', '\n', text)
        text = re.sub(r' {2,}', ' ', text)

        text = text.strip()
        with open(fn, 'w') as f:
            f.write(text)
    except:
        return key

if __name__ == '__main__':
    with open('metadata.pickle', 'rb') as f:
        metadata = pickle.load(f)

    with multiprocessing.Pool(NUM_CORES) as pool:
        results = list(tqdm.tqdm(
            pool.imap(proc, metadata.keys()),
            total=len(metadata),
        ))
        for result in results:
            if result is not None:
                os.remove('./documents/' + result)
                del metadata[result]

    with open('./metadata.pickle', 'wb') as f:
        pickle.dump(metadata, f, pickle.HIGHEST_PROTOCOL)

    print(f'Corpus has {len(metadata)} files.')

