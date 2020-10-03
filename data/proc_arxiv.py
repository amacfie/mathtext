from clean_tex import rewrite_or_delete
from utils import random_string

from pathlib import Path
from shutil import move
import glob
import multiprocessing
import pickle
import psutil
import shutil
import tqdm

NUM_CORES = psutil.cpu_count(logical=False)

if __name__ == '__main__':
    print('finding all .tex files...')
    tex_fns = glob.glob('./gzfiles/**/*.tex', recursive=True)
    print('processing .tex files...')
    with multiprocessing.Pool(NUM_CORES) as pool:
        fns = list(tqdm.tqdm(
            pool.imap(rewrite_or_delete, tex_fns),
            total=len(tex_fns),
        ))

    with open('metadata.pickle', 'rb') as f:
        metadata = pickle.load(f)
    for fn in fns:
        if fn is not None:
            new_name = random_string(20)
            metadata[new_name] = {
                'source': 'arXiv',
                'id': fn[len('./gzfiles/'):],
            }
            shutil.move(fn, './documents/' + new_name)

    with open('metadata.pickle', 'wb') as f:
        json.dump(metadata, f, pickle.HIGHEST_PROTOCOL)

