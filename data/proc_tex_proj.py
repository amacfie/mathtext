from clean_tex import rewrite_or_delete
from utils import random_string

import glob
import json
import shutil
import sys

if __name__ == '__main__':
    folder = sys.argv[1]
    source = sys.argv[2]

    with open('../metadata.json') as f:
        index = json.load(f)
    # excludes hidden folders
    for fn in glob.glob(folder + '/**/*.tex', recursive=True):
        rewrite_or_delete(fn)
    for fn in (glob.glob(folder + '/**/*.tex', recursive=True) +
        glob.glob(folder + '/**/*.md', recursive=True)
    ):
        name = random_string(20)
        new_fn = '../documents/' + name
        index[name] = {
            'source': source,
            'id': fn[len(folder + '/'):],
        }
        shutil.move(fn, new_fn)

    shutil.rmtree(folder)

    with open('../metadata.json', 'w') as f:
        json.dump(index, f, indent=2)

