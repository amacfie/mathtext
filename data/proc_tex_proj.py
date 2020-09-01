import glob
import json
import random
import shutil
import string
import sys

def random_string(n):
    return ''.join(
        random.choice(string.ascii_uppercase + string.digits)
        for _ in range(n)
    )

if __name__ == '__main__':
    folder = sys.argv[1]
    source = sys.argv[2]

    with open('../index.json') as f:
        index = json.load(f)
    for fn in glob.glob(folder + '/**/*.tex') + glob.glob(folder + '/**/*.md'):
        name = random_string(20)
        new_fn = '../documents/' + name
        index[name] = {
            'source': source,
            'id': fn[len(folder + '/'):],
        }
        shutil.move(fn, new_fn)

    shutil.rmtree(folder)

    with open('../index.json', 'w') as f:
        json.dump(index, f, indent=2)

