#!/bin/bash

# usage:
# Q1='first query' Q2='second query' ./search.sh
# Q1 goes to csearch, Q2 goes to grep on results from csearch
# set Q1='' to disable csearch

set -e

# https://stackoverflow.com/a/6703730
if [[ -z "$Q1" ]]; then
  read -p "csearch query (Q1): " Q1
else
  read -e -i "$Q1" -p "csearch query (Q1): " Q1
fi
if [[ -z "$Q2" ]]; then
  read -p "grep query (Q2): " Q2
else
  read -e -i "$Q2" -p "grep query (Q2): " Q2
fi

# https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself#comment54598418_246128
dirpath="$(dirname "$(readlink -f "$0")")"
results_file=$(mktemp)
temp_file=$(mktemp)
if [[ -z "$Q1" ]]; then
  rg -l --multiline --pcre2 "$Q2" "${dirpath}/../data/documents" > $results_file
else
  csearch -l "$Q1" > ${temp_file}
  if [[ -s ${temp_file} ]]; then
    # https://unix.stackexchange.com/a/494689
    xargs -d '\n' -a ${temp_file} rg -l --multiline --pcre2 "$Q2" > $results_file
  else
    echo -n "" > $results_file
  fi
fi

{
python3 - "${dirpath}" "${results_file}" << EOF
import json
import pathlib
import sys
import urllib

dirpath = sys.argv[1]
results_file = sys.argv[2]

results = pathlib.Path(results_file).read_text().split('\n')

with open(dirpath + '/../data/index.json') as f:
    docs = json.load(f)

links = set()
for result in results:
    if not result:
        continue
    key = result.split('/')[-1]
    value = docs[key]
    if value['source'] == 'arXiv':
        if '/' in value['id']:
            arxiv_code = value['id'].split('/')[0]
        else:
            arxiv_code = value['id'][:-4]
        links.add('http://google.com/search?q={}'.format(urllib.parse.quote(
            'site:arxiv.org ' + arxiv_code
        )))
    elif value['source'] == 'Stack Exchange':
        links.add(value['id'])
    else:
        links.add(value['source'])
print('\n'.join(links))
EOF
} > ${temp_file}


if [[ -s ${temp_file} ]]; then
  $EDITOR ${temp_file}
fi
rm ${temp_file} ${results_file}

