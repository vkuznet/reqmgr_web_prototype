#!/bin/sh
if [ -f "setup.sh" ]; then
    source $PWD/setup.sh
else
    export PATH=$PWD/soft/bin:$PATH
fi
export PYTHONPATH=$PWD/python:$PYTHONPATH
export IMG_ROOT=$PWD/images
export CSS_ROOT=$PWD/css
export JS_ROOT=$PWD/js
export TMPL_ROOT=$PWD/templates
export WEB_PORT=18765
export WEB_HOST='0.0.0.0'
export WEB_BASE='' # modify if want to mount server on different base
python -u python/server.py
