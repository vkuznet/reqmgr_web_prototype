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
export WEB_PORT=8765
export WEB_HOST='0.0.0.0'
python -u python/server.py
