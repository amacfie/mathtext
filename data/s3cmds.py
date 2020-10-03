import json
import sys
import xml.etree.ElementTree as ET

max_lines = int(sys.argv[1])

with open('./arxiv_log.json') as f:
    arxiv_log = json.load(f)

def yyyymm(yymm):
    return '19' + yymm if yymm[0] == '9' else '20' + yymm

tree = ET.parse('arXiv_src_manifest.xml')
root = tree.getroot()
files = sorted(
    [ { 'yymm': el[-1].text, 'filename': el[1].text } for el in root[:-1] ],
    key=lambda f: yyyymm(f['yymm']),
    reverse=True,
)
num_lines = 0
for f in files:
    if num_lines >= max_lines:
        break
    cmd = 's3cmd get s3://arxiv/{} --requester-pays'.format(f['filename'])
    if cmd in arxiv_log:
        continue
    else:
        print(cmd)
        arxiv_log.append(cmd)
        num_lines += 1

with open('./arxiv_log.json', 'w') as f:
    json.dump(arxiv_log, f)

