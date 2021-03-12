#!/bin/bash
sudo apt update
sudo apt install s3cmd p7zip-full parallel pv xml-twig-tools
pip3 install wheel
pip3 install unp beautifulsoup4 unidecode tqdm psutil lxml
if [ -z "$(s3cmd --dump-config | grep -P '^access_key' | cut -d' ' -f3)" ]
then
  s3cmd --configure
fi
