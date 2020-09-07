import sys
import xml.etree.ElementTree as ET

max_lines = int(sys.argv[1])

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
    print('s3cmd get s3://arxiv/{} --requester-pays'.format(f['filename']))
    num_lines += 1

