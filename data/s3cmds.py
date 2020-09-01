import sys
import xml.etree.ElementTree as ET

max_lines = int(sys.argv[1])

tree = ET.parse('arXiv_src_manifest.xml')
root = tree.getroot()
files = sorted(
    [ { 'yymm': el[-1].text, 'filename': el[1].text } for el in root[:-1] ],
    key=lambda f: f['yymm'],
    reverse=True,
)
files = [ f for f in files if f['yymm'][0] != '9' ]
num_lines = 0
for f in files:
    if num_lines >= max_lines:
        break
    print('s3cmd get s3://arxiv/{} --requester-pays'.format(f['filename']))
    num_lines += 1

