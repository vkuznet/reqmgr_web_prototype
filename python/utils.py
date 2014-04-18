#!/usr/bin/env python
#-*- coding: utf-8 -*-
#pylint: disable=
"""
File       : utils.py
Author     : Valentin Kuznetsov <vkuznet AT gmail dot com>
Description:
"""

# system modules
import cgi
import json
import hashlib

def quote(data):
    """
    Sanitize the data using cgi.escape.
    """
    if  isinstance(data, int) or isinstance(data, float):
        res = data
    elif  isinstance(data, dict):
        res = data
    elif  isinstance(data, list):
        res = data
    elif  isinstance(data, long) or isinstance(data, int) or\
          isinstance(data, float):
        res = data
    else:
        try:
            if  data:
                res = cgi.escape(data, quote=True)
            else:
                res = ""
        except Exception as exc:
            print_exc(exc)
            print "Unable to cgi.escape(%s, quote=True)" % data
            res = ""
    return res

def json2table(jsondata, web_ui_map):
    """
    Convert input json dict into HTML table based on assumtion that
    input json is in a simple key:value form.
    """
    table = """<table class="table-bordered width-100">\n"""
    table += "<thead><tr><th>Field</th><th>Value</th></tr></thead>\n"
    keys = sorted(jsondata.keys())
    for key in keys:
        val = jsondata[key]
        if  isinstance(val, list):
            sel = "<select>"
            values = sorted(val)
            if  key in ['releases', 'software_releases', 'CMSSWVersion', 'ScramArch']:
                values.reverse()
            for item in values:
                sel += "<option>%s</option>" % item
            sel += "</select>"
            val = sel
        elif isinstance(val, basestring):
            if  len(val) < 80:
                val = '<input type="text" name="%s" value="%s" />' % (key, val)
            else:
                val = '<textarea name="%s" class="width-100">%s</textarea>' % (key, val)
        else:
            val = '<input type="text" name="%s" value="%s" />' % (key, val)
        if  key in web_ui_map:
            kname = web_ui_map[key]
        else:
            kname = key.capitalize().replace('_', ' ')
        table += "<tr><td>%s</td><td>%s</td></tr>\n" % (kname, val)
    table += "</table>"
    return table

def genid(kwds):
    "Generate id for given field"
    if  isinstance(kwds, dict):
        record = dict(kwds)
        data = json.JSONEncoder(sort_keys=True).encode(record)
    else:
        data = str(kwds)
    keyhash = hashlib.md5()
    keyhash.update(data)
    return keyhash.hexdigest()
