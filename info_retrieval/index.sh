#!/bin/bash

# creates a copy of the corpus with all sequences of whitespace converted to
# newlines -- after indexing, `data/documents` is not required for searching
# so delete it unneeded

dirpath="$(dirname "$(readlink -f "$0")")"
cd ${dirpath}
rm -rf ./index
mkdir ./index
cp -r ../data/documents ./index/documents_no_newline
python3 ./multiline.py

python3 <<EOF
from pathlib import Path
import glob
import math
import os
import random
import shutil

total_bytes = sum(
    f.stat().st_size
    for f in Path('./index/documents_no_newline').glob('*')
)
num_parts = math.ceil(total_bytes / 10_000_000_000)
doc_dirs = [ './index/docs_' + str(i) for i in range(num_parts) ]
for doc_dir in doc_dirs:
    os.mkdir(doc_dir)

for fn in glob.glob('./index/documents_no_newline/*'):
    doc_dir = random.choice(doc_dirs)
    shutil.move(fn, doc_dir)
EOF

rm -rf ./index/documents_no_newline

for doc_dir in ./index/*; do
  cindex -maxlinelen 1000000 -indexpath ./index/index_$(basename ${doc_dir}) $doc_dir
done

