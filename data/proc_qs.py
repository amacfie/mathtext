from utils import random_string

from bs4 import BeautifulSoup
from pathlib import Path
import glob
import json
import os
import sys
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    xml_fn = sys.argv[1]
    base_url = sys.argv[2]

    tree = ET.parse(xml_fn)
    root = tree.getroot()
    for el in root:
        if str(el.attrib['PostTypeId']) == '2':
            continue
        fn = '/tmp/m_se_q_{}.txt'.format(el.attrib['Id'])
        soup = BeautifulSoup(el.attrib['Body'])
        text = soup.get_text()
        with open(fn, 'w') as f:
            f.write(text)

    with open('./index.json') as f:
        index = json.load(f)
    for el in root:
        if str(el.attrib['PostTypeId']) == '1':
            continue
        try:
            a_fn = '/tmp/m_se_q_{}.txt'.format(el.attrib['ParentId'])
            text = '<QUESTION>' + Path(a_fn).read_text() + '\n'
            name = random_string(20)
            fn = './documents/' + name
            index[name] = {
                'source': 'Stack Exchange',
                'id': base_url + '/a/' + el.attrib['Id'],
            }
            soup = BeautifulSoup(el.attrib['Body'])
            text += '<ANSWER>' + soup.get_text()
            with open(fn, 'w') as f:
                f.write(text)
        except:
            pass

    for txt in glob.glob('/tmp/m_se_q*'):
        os.remove(txt)

    with open('index.json', 'w') as f:
        json.dump(index, f, indent=2)

