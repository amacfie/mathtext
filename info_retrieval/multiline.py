import glob
import multiprocessing
import psutil
import pathlib
import re
import tqdm

NUM_CORES = psutil.cpu_count(logical=False)

def proc(fn):
    text = pathlib.Path(fn).read_text()
    text = re.sub(r'\n+', ' ', text)
    with open(fn, 'w') as f:
        f.write(text)

if __name__ == '__main__':
    fns = glob.glob(str(pathlib.Path(__file__).parent) +
        '/index/documents_no_newline/*')

    with multiprocessing.Pool(NUM_CORES) as pool:
        list(tqdm.tqdm(pool.imap(proc, fns), total=len(fns)))

