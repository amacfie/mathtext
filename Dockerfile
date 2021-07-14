FROM ubuntu:20.04
ENV PYTHONUNBUFFERED 1
RUN apt update -y
ENV DEBIAN_FRONTEND="noninteractive" TZ="America/New_York"
RUN apt install -y s3cmd p7zip-full parallel pv xml-twig-tools python3-pip git golang silversearcher-ag wget neovim
ENV EDITOR="nvim"
RUN wget https://github.com/BurntSushi/ripgrep/releases/download/13.0.0/ripgrep_13.0.0_amd64.deb
RUN dpkg -i ripgrep_13.0.0_amd64.deb
RUN pip3 install wheel
RUN pip3 install unp beautifulsoup4 unidecode tqdm psutil lxml
RUN go get github.com/junkblocker/codesearch/cmd/...
RUN go install github.com/junkblocker/codesearch/cmd/cindex
RUN go install github.com/junkblocker/codesearch/cmd/csearch
ENV PATH="/root/go/bin:/usr/local/go/bin:${PATH}"
WORKDIR /code
