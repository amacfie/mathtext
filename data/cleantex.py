from pathlib import Path
from shutil import copy, move
import glob
import json
import multiprocessing
import psutil
import random
import re
import shutil
import string
import tqdm

NUM_CORES = psutil.cpu_count(logical=False)

def random_string(n):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )

# https://stackoverflow.com/a/4665027
def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1: return
        yield start
        start += len(sub) # use start += 1 to find overlapping matches

def clean(fn):
    try:
        text = Path(fn).read_text()
    except:
        return
    text = re.sub(r'\s+', ' ', text)

    section_ixes = list(find_all(text, '\\section{'))
    if (section_ixes and text[section_ixes[0]:len('\\section{Introduction')]
        == '\\section{Introduction' and len(section_ixes) >= 2
    ):
        text = text[section_ixes[1]:]
    if (section_ixes and text[section_ixes[-1]:len('\\section{Conclusion')]
        == '\\section{Conclusion'
    ):
        text = text[:section_ixes[-1]]
    if '\\begin{document}' in text:
        text = text[text.index('\\begin{document}'):]
    if '\\end{document}' in text:
        text = text[:text.index('\\end{document}')]

    with open(fn, 'w') as f:
        f.write(text)

def good_or_none(fn):
    try:
        text = Path(fn).read_text()
        if ('proof' in text and
            ('theorem' in text or 'lemma' in text)
        ) or '\\begin{proof}' in text:
            return fn
        else:
            return None
    except:
        return None

if __name__ == '__main__':
    print('finding all .tex files...')
    tex_fns = glob.glob('./gzfiles/**/*.tex')
    print('processing .tex files...')
    with multiprocessing.Pool(NUM_CORES) as pool:
        list(tqdm.tqdm(pool.imap(clean, tex_fns), total=len(tex_fns)))

    with multiprocessing.Pool(NUM_CORES) as pool:
        fns = list(tqdm.tqdm(
            pool.imap(good_or_none, tex_fns),
            total=len(tex_fns),
        ))

    with open('index.json') as f:
        index = json.load(f)
    for fn in fns:
        if fn is not None:
            new_name = random_string(20)
            index[new_name] = {
                'source': 'arXiv',
                'id': fn[len('./gzfiles/'):],
            }
            shutil.move(fn, './documents/' + new_name)

    with open('index.json', 'w') as f:
        json.dump(index, f, indent=2)

