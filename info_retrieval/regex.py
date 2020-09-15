#!/usr/bin/env python3
from whoosh import index
from whoosh.qparser import QueryParser
from whoosh.scoring import Frequency
from pathlib import Path
import argparse
import json
import multiprocessing
import os
import psutil
import re
import sys
import tqdm

if ('MATHTEXT_NUM_WORKERS' in os.environ and
    os.environ['MATHTEXT_NUM_WORKERS'].strip()
):
    NUM_WORKERS = int(os.environ['MATHTEXT_NUM_WORKERS'])
else:
    NUM_WORKERS = psutil.cpu_count(logical=False)

parser = argparse.ArgumentParser(description=('Search corpus.'))
parser.add_argument('regex', help='Python regular expression.')
parser.add_argument(
    '--trigramquery',
    default='',
    help=('Broken into trigrams and only documents with those trigrams are '
        'searched with the regex. See '
        'https://whoosh.readthedocs.io/en/latest/querylang.html for syntax.'
    ),
)
args = parser.parse_args()

with open('../data/index.json') as f:
    docs = json.load(f)

def search(key):
    fn = '../data/documents/' + key
    text = Path(fn).read_text()
    if re.search(args.regex, text):
        return key
    else:
        return None

if __name__ == '__main__':  # req'd apparently
    # since there are many small documents, they can be processed in parallel,
    # each worker need only have one document open at a time for low memory
    # usage

    if args.trigramquery:
        if not index.exists_in('index'):
            print('Run ./create_index.py first to do trigram filtering.')
            sys.exit(1)
        else:
            local_index = index.open_dir('index')
            with local_index.searcher(weighting=Frequency()) as searcher:
                query = QueryParser('content', local_index.schema).parse(
                    args.trigramquery)
                results = searcher.search(query, limit=None)
                keys = [ result['key'] for result in results ]
    else:
        keys = docs.keys()

    with multiprocessing.Pool(NUM_WORKERS) as pool:
        # https://stackoverflow.com/a/45276885
        results = list(tqdm.tqdm(pool.imap(search, keys), total=len(keys)))
    positives = [ result for result in results if result is not None ]
    print(f'{len(positives)} matches found.')
    print(json.dumps({
        positive: docs[positive] for positive in positives
    }, indent=2))

