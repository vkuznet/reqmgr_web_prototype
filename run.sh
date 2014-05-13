#!/bin/sh
if [ -f "setup.sh" ]; then
    source $PWD/setup.sh
else
    export PATH=$PWD/soft/bin:$PATH
fi
export PYTHONPATH=$PWD/python:$PYTHONPATH
export RM_TMPLPATH=$PWD/templates
export RM_IMAGESPATH=$PWD/images
export RM_CSSPATH=$PWD/css
export RM_JSPATH=$PWD/js
export YUI_ROOT=/Users/vk/CMS/yui
export WEB_PORT=18765
export WEB_HOST='0.0.0.0'
export WEB_BASE='' # modify if want to mount server on different base
python -u python/ReqMgr/server.py
