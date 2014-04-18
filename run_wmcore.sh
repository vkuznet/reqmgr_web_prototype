#!/bin/sh
export WMCOREROOT=/Users/vk/CMS/DMWM/GIT/WMCore
export PYTHONPATH=$WMCOREROOT/src/python:$PWD/python/
export RM_TMPLPATH=$PWD/templates/
export RM_IMAGESPATH=$PWD/images
export RM_CSSPATH=$PWD/css
export RM_JSPATH=$PWD/js
export YUI_ROOT=/Users/vk/CMS/yui
python -u $WMCOREROOT/src/python/WMCore/WebTools/Root.py --ini=$PWD/etc/rm_config.py
