#!/bin/sh
export PATH=$PWD/soft/bin:$PATH
export PYTHONPATH=$PWD/python
export IMG_ROOT=$PWD/images
export CSS_ROOT=$PWD/css
export JS_ROOT=$PWD/js
export TMPL_ROOT=$PWD/templates
export WEB_PORT=8765
export WEB_HOST='0.0.0.0'
python -u python/server.py
