#!/usr/bin/env python3

'''
apparently Lucene handles big data better
'''

from pathlib import Path
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.analysis import NgramTokenizer
import json
import os
import psutil

if not os.path.exists('index'):
    os.makedirs('index')

if ('MATHTEXT_NUM_WORKERS' in os.environ and
    os.environ['MATHTEXT_NUM_WORKERS'].strip()
):
    NUM_WORKERS = int(os.environ['MATHTEXT_NUM_WORKERS'])
else:
    NUM_WORKERS = psutil.cpu_count(logical=False)

schema = Schema(key=ID(stored=True), content=TEXT(
    analyzer=NgramTokenizer(minsize=3, maxsize=3),
    phrase=False,  # so it's trigram search not exact search
))
ix = create_in('index', schema)
writer = ix.writer(procs=NUM_WORKERS, limitmb=512, multisegment=True)
with open('../data/index.json') as f:
    index = json.load(f)
for key in index:
    text = Path('../data/documents/' + key).read_text()
    writer.add_document(key=key, content=text)
print('Writing index (slow)...')
writer.commit()

