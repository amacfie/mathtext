#!/bin/bash

sudo apt update
sudo apt install s3cmd p7zip-full parallel
pip3 install unp beautifulsoup4 unidecode
if [ -z "$(s3cmd --dump-config | grep -P '^access_key' | cut -d' ' -f3)" ]
then
  s3cmd --configure
fi
