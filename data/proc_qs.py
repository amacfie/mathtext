from utils import random_string

from bs4 import BeautifulSoup
from pathlib import Path
import glob
import os
import pickle
import sys
import tqdm
import xml.etree.ElementTree as ET

if __name__ == '__main__':
    base_url = sys.argv[1]

    with open('./metadata.pickle', 'rb') as f:
        metadata = pickle.load(f)

    for xml_fn in glob.glob(base_url + '/out*'):
        if xml_fn == base_url + '/out-00.xml': continue
        print('Parsing XML chunk...')
        root = ET.parse(xml_fn).getroot()
        for el in tqdm.tqdm(root):
            if str(el.attrib['PostTypeId']) != '1': continue
            fn = '/tmp/mt_se_q_{}.txt'.format(el.attrib['Id'])
            soup = BeautifulSoup(el.attrib['Body'], features='lxml')
            with open(fn, 'w') as f:
                f.write(soup.get_text())
        del root, el

    for xml_fn in glob.glob(base_url + '/out*'):
        if xml_fn == base_url + '/out-00.xml': continue
        print('Parsing XML chunk once more...')
        root = ET.parse(xml_fn).getroot()
        for el in tqdm.tqdm(root):
            if str(el.attrib['PostTypeId']) != '2': continue
            try:
                q_fn = '/tmp/mt_se_q_{}.txt'.format(el.attrib['ParentId'])
                text = '<QUESTION>' + Path(q_fn).read_text() + '\n'
                name = random_string(20)
                fn = './documents/' + name
                metadata[name] = {
                    'source': 'Stack Exchange',
                    'id': base_url + '/a/' + el.attrib['Id'],
                }
                soup = BeautifulSoup(el.attrib['Body'], features='lxml')
                text += '<ANSWER>' + soup.get_text()
                with open(fn, 'w') as f:
                    f.write(text)
            except FileNotFoundError:
                pass
        del root, el

    for txt in glob.glob('/tmp/mt_se_q*'):
        os.remove(txt)

    with open('metadata.pickle', 'wb') as f:
        pickle.dump(metadata, f, pickle.HIGHEST_PROTOCOL)

