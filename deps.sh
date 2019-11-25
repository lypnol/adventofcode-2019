#!/bin/bash

set -ev

# Install Rust if not present via cache
curl https://sh.rustup.rs -sSf -o rustup.sh
sh rustup.sh -y
export PATH=$PATH:~/.cargo/bin

# Install golang
(cd /tmp && wget https://dl.google.com/go/go1.13.3.linux-amd64.tar.gz)
sudo tar -xvf /tmp/go1.13.3.linux-amd64.tar.gz
sudo mv /tmp/go /usr/local

export PYENV_VERSION=3.7

npm install
sudo apt-get install python3-setuptools
python3 -m pip install wheel
python3 -m pip install --user -r requirements.txt

mkdir -p .deps/chached
