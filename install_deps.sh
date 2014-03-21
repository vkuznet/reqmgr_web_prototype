#!/bin/bash

# make clean environment
unset PYTHONPATH

# download virtualenv and install pip
venv=virtualenv-1.11.4
curl -O https://pypi.python.org/packages/source/v/virtualenv/$venv.tar.gz
tar xfz $venv.tar.gz
python $venv/virtualenv.py soft
. soft/bin/activate

# now we're ready to go
export PATH=$PWD/soft/bin:$PATH
pip install cherrypy
pip install Cheetah
rm -rf $venv*
