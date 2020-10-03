#!/bin/bash

# usage:
# MATHTEXT_Q1='first query' MATHTEXT_Q2='second query' ./search.sh
# MATHTEXT_Q1 goes to csearch, MATHTEXT_Q2 goes to ag on results from csearch.

set -e

# https://stackoverflow.com/questions/59895/how-to-get-the-source-directory-of-a-bash-script-from-within-the-script-itself#comment54598418_246128
dirpath="$(dirname "$(readlink -f "$0")")"
cd $dirpath

[[ -f  ~/.mathtext_q1_history ]] || touch ~/.mathtext_q1_history
[[ -f  ~/.mathtext_q2_history ]] || touch ~/.mathtext_q2_history
history -r ~/.mathtext_q1_history
read -r -e -i "$MATHTEXT_Q1" -p "csearch query (MATHTEXT_Q1): " MATHTEXT_Q1
history -s "$MATHTEXT_Q1"
history -w ~/.mathtext_q1_history
history -c
history -r ~/.mathtext_q2_history
read -r -e -i "$MATHTEXT_Q2" -p "ag query (MATHTEXT_Q2): " MATHTEXT_Q2
history -s "$MATHTEXT_Q2"
history -w ~/.mathtext_q2_history

function mathtext_csearch {
  for f in "${dirpath}"/index/index_*; do
    sem -j +0 "csearch -l -indexpath $f \"${1}\""
  done
  sem --wait
}

results_file=$(mktemp)
temp_file=$(mktemp)
if [[ -z "$MATHTEXT_Q1" ]] && [[ -z "$MATHTEXT_Q2" ]]; then
  exit 1
elif [[ -z "$MATHTEXT_Q1" ]]; then
  rg --multiline --pcre2 -l "$MATHTEXT_Q2" "${dirpath}/index/docs_*" > $results_file
elif [[ -z "$MATHTEXT_Q2" ]]; then
  mathtext_csearch "$MATHTEXT_Q1" > ${results_file}
else
  mathtext_csearch "$MATHTEXT_Q1" > ${temp_file}
  if [[ -s ${temp_file} ]]; then
    # rg has been slow for long command lines
    # https://unix.stackexchange.com/a/494689
    # yes if there are multiple ag calls `$results_file` has output from all
    xargs -d '\n' -a ${temp_file} ag -l "$MATHTEXT_Q2" > $results_file
  else
    echo -n "" > $results_file
  fi
fi

{
python3 - "${dirpath}" "${results_file}" << EOF
import pathlib
import pickle
import sys
import urllib

dirpath = sys.argv[1]
results_file = sys.argv[2]

results = pathlib.Path(results_file).read_text().split('\n')

# this is kinda slow but on a server we'd keep it in memory
with open(dirpath + '/../data/metadata.pickle', 'rb') as f:
    docs = pickle.load(f)

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
        links.add('https://' + value['id'])
    else:
        if 'github' in value['source']:
            links.add(value['source'] + '/' + value['id'])
        else:
            links.add(value['source'])
print('\n'.join(sorted(links)))
EOF
} > ${temp_file}


if [[ -s ${temp_file} ]]; then
  $EDITOR ${temp_file}
fi
rm ${temp_file} ${results_file}

