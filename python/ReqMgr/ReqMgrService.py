#!/usr/bin/env python
#-*- coding: ISO-8859-1 -*-

"""
web server.
"""

__author__ = "Valentin Kuznetsov"

# system modules
import os
import sys
import time
import json
import pprint

# cherrypy modules
import cherrypy
from cherrypy import expose, response, tools
from cherrypy.lib.static import serve_file
from cherrypy import config as cherryconf

from ReqMgr.tools import exposecss, exposejs, exposejson, TemplatedPage
from ReqMgr.utils import json2table, genid
from ReqMgr.url_utils import getdata
from ReqMgr.cms import dqm_urls, dbs_urls, releases, architectures, scenarios, cms_groups
from ReqMgr.cms import web_ui_names, next_status

def set_headers(itype, size=0):
    """
    Set response header Content-type (itype) and Content-Length (size).
    """
    if  size > 0:
        response.headers['Content-Length'] = size
    response.headers['Content-Type'] = itype
    response.headers['Expires'] = 'Sat, 14 Oct 2017 00:59:30 GMT'

def minify(content):
    """
    Remove whitespace in provided content.
    """
    content = content.replace('\n', ' ')
    content = content.replace('\t', ' ')
    content = content.replace('   ', ' ')
    content = content.replace('  ', ' ')
    return content

def menus(active='search'):
    "Return dict of menus"
#    items = ['admin', 'assign', 'approve', 'create', 'requests', 'search', 'validate']
    items = ['admin', 'assign', 'approve', 'create', 'requests']
    mdict = dict(zip(items, ['']*len(items)))
    mdict[active] = 'active'
    return mdict

class ReqMgrService(TemplatedPage):
    """
    Request Manager web service class
    """
    def __init__(self, config=None):
        self.base   = os.environ.get('WEB_BASE', '') # defines base path for HREF in templates
        if  config and not isinstance(config, dict):
            config = config.dictionary_()
        if  not config:
            config = {'base': self.base}
        print "\n### Configuration:"
        pprint.pprint(config)
        TemplatedPage.__init__(self, config)
        imgdir = os.environ.get('RM_IMAGESPATH', os.getcwd()+'/images')
        self.imgdir = config.get('imgdir', imgdir)
        cssdir = os.environ.get('RM_CSSPATH', os.getcwd()+'/css')
        self.cssdir = config.get('cssdir', cssdir)
        jsdir  = os.environ.get('RM_JSPATH', os.getcwd()+'/js')
        self.jsdir = config.get('jsdir', jsdir)
        yuidir = os.environ.get('YUI_ROOT', os.getcwd()+'/yui')
        self.yuidir = config.get('yuidir', yuidir)

        # To be filled at run time
        self.cssmap = {}
        self.jsmap  = {}
        self.imgmap = {}
        self.yuimap = {}

        # Update CherryPy configuration
        mime_types  = ['text/css']
        mime_types += ['application/javascript', 'text/javascript',
                       'application/x-javascript', 'text/x-javascript']
        cherryconf.update({'tools.encode.on': True,
                           'tools.gzip.on': True,
                           'tools.gzip.mime_types': mime_types,
                          })
        self._cache    = {}

    def user(self):
        "Return user name associated with this instance"
        return 'testuser'

    def abs_page(self, tmpl, content):
        """generate abstract page"""
        menu = self.templatepage('menu', menus=menus(tmpl))
        if  tmpl == 'main':
            body = self.templatepage('generic', menu=menu, content=content)
            page = self.templatepage('main', content=body, user=self.user())
        else:
            body = self.templatepage(tmpl, menu=menu, content=content)
            page = self.templatepage('main', content=body, user=self.user())
        return page

    def page(self, content):
        """
        Provide page wrapped with top/bottom templates.
        """
        return self.templatepage('main', content=content)

    def error(self, content):
        "Generate common error page"
        content = self.templatepage('error', content=content)
        return self.abs_page('generic', content)

    @expose
    def index(self, **kwargs):
        """Main page"""
        apis = {}
        scripts = {}
        for idx in range(5):
            key = 'api_%s' % idx
            val = '%s description' % key
            apis[key] = val
            skey = 'script_%s' % idx
            sval = '%s description' % skey
            scripts[skey] = sval
        content = self.templatepage('apis', apis=apis, scripts=scripts)
        return self.abs_page('generic', content)

    ### Admin actions ###

    @expose
    def admin(self, **kwargs):
        """admin page"""
        content = self.templatepage('admin')
        return self.abs_page('generic', content)

    @expose
    def add_user(self, **kwargs):
        """add_user action"""
        rid = genid(kwargs)
        content = self.templatepage('confirm', ticket=rid, user=self.user())
        return self.abs_page('generic', content)

    @expose
    def add_group(self, **kwargs):
        """add_group action"""
        rid = genid(kwargs)
        content = self.templatepage('confirm', ticket=rid, user=self.user())
        return self.abs_page('generic', content)

    @expose
    def add_team(self, **kwargs):
        """add_team action"""
        rid = genid(kwargs)
        content = self.templatepage('confirm', ticket=rid, user=self.user())
        return self.abs_page('generic', content)

    ### Request actions ###

    @expose
    def assign(self, **kwargs):
        """assign page"""
        content = self.templatepage('assign')
        return self.abs_page('generic', content)

    @expose
    def approve(self, **kwargs):
        """
        Approve page: get list of request associated with user DN.
        Fetch their status list from ReqMgr and display if requests
        were seen by data-ops.
        """
        requests = []
        for rstat in ['new', 'new', 'assigned', 'running']:
            wdict = dict(date=time.ctime(), team='Team-A', status=rstat, ID=genid(time.time()))
            requests.append(wdict)
        print "Env:", os.environ['PYTHONPATH']
        content = self.templatepage('approve', requests=requests)
        return self.abs_page('generic', content)

    @expose
    def create(self, **kwargs):
        """create page"""
        req_form = kwargs.get('form', 'rereco')
        fname = 'json/%s' % str(req_form)
        # request form
        jsondata = self.templatepage(fname,
                user=json.dumps(self.user()),
                groups=json.dumps(cms_groups()),
                releases=json.dumps(releases()),
                arch=json.dumps(architectures()),
                scenarios=json.dumps(scenarios()),
                dqm_urls=json.dumps(dqm_urls()),
                dbs_urls=json.dumps(dbs_urls()),
                )
        try:
            jsondata = json.loads(jsondata)
        except Exception as exp:
            msg  = '<div class="color-gray">Fail to load JSON for %s workflow</div>\n' % req_form
            msg += '<div class="color-red">Error: %s</div>\n' % str(exp)
            msg += '<div class="color-gray-light">JSON: %s</div>' % jsondata
            return self.error(msg)

        # create templatized page out of provided forms
        content = self.templatepage('create', table=json2table(jsondata, web_ui_names()),
                jsondata=json.dumps(jsondata, indent=2), name=req_form)
        return self.abs_page('generic', content)

    @expose
    def confirm_create(self, **kwargs):
        """create page"""
        rid = genid(kwargs)
        content = self.templatepage('confirm', ticket=rid, user=self.user())
        return self.abs_page('generic', content)

    @expose
    def generate_objs(self, **kwargs):
        """create page interface: generate objects from givem JSON template"""
        jsondict = json.loads(kwargs.get('jsondict'))
        code = kwargs.get('code')
        if  code.find('def genobjs(jsondict)') == -1:
            return self.error("Improper python snippet, your code should start with <b>def genobjs(jsondict)</b> function")
        exec(code)
        objs = genobjs(jsondict)
        rids = []
        for iobj in objs:
            print "### generate JSON"
            print iobj
            rids.append(genid(iobj))
        content = self.templatepage('confirm', ticket=rids, user=self.user())
        return self.abs_page('generic', content)

    @expose
    def requests(self, **kwargs):
        """Check status of requests"""
        wdict = dict(date=time.ctime(), team='Team-A', status='Pending', ID=genid(time.time()))
        requests = [wdict, wdict, wdict]
        content = self.templatepage('requests', requests=requests)
        return self.abs_page('generic', content)

    @expose
    def request(self, **kwargs):
        "Get data example and expose it as json"
        dataset = kwargs.get('uinput', '')
        if  not dataset:
            return {'error':'no input dataset'}
        url = 'https://cmsweb.cern.ch/reqmgr/rest/outputdataset/%s' % dataset
        params = {}
        headers = {'Accept': 'application/json;text/json'}
        wdata = getdata(url, params)
        wdict = dict(date=time.ctime(), team='Team-A', status='Running', ID=genid(wdata))
        winfo = self.templatepage('workflow', wdict=wdict,
                dataset=dataset, code=pprint.pformat(wdata))
        content = self.templatepage('search', content=winfo)
        return self.abs_page('generic', content)

    ### Aux methods ###

    @expose
    def images(self, *args, **kwargs):
        """
        Serve static images.
        """
        args = list(args)
        self.check_scripts(args, self.imgmap, self.imgdir)
        mime_types = ['*/*', 'image/gif', 'image/png',
                      'image/jpg', 'image/jpeg']
        accepts = cherrypy.request.headers.elements('Accept')
        for accept in accepts:
            if  accept.value in mime_types and len(args) == 1 \
                and args[0] in self.imgmap:
                image = self.imgmap[args[0]]
                # use image extension to pass correct content type
                ctype = 'image/%s' % image.split('.')[-1]
                cherrypy.response.headers['Content-type'] = ctype
                return serve_file(image, content_type=ctype)

    def serve(self, kwds, imap, idir, datatype='', minimize=False):
        "Serve files for high level APIs (yui/css/js)"
        args = []
        for key, val in kwds.items():
            if  key == 'f': # we only look-up files from given kwds dict
                if  isinstance(val, list):
                    args += val
                else:
                    args.append(val)
        scripts = self.check_scripts(args, imap, idir)
        return self.serve_files(args, scripts, imap, datatype, minimize)

    @exposecss
    @tools.gzip()
    def css(self, **kwargs):
        """
        Serve provided CSS files. They can be passed as
        f=file1.css&f=file2.css
        """
        resource = kwargs.get('resource', 'css')
        if  resource == 'css':
            return self.serve(kwargs, self.cssmap, self.cssdir, 'css', True)
        elif resource == 'yui':
            return self.serve(kwargs, self.yuimap, self.yuidir)

    @exposejs
    @tools.gzip()
    def js(self, **kwargs):
        """
        Serve provided JS scripts. They can be passed as
        f=file1.js&f=file2.js with optional resource parameter
        to speficy type of JS files, e.g. resource=yui.
        """
        resource = kwargs.get('resource', 'js')
        if  resource == 'js':
            return self.serve(kwargs, self.jsmap, self.jsdir)
        elif resource == 'yui':
            return self.serve(kwargs, self.yuimap, self.yuidir)

    def serve_files(self, args, scripts, resource, datatype='', minimize=False):
        """
        Return asked set of files for JS, YUI, CSS.
        """
        idx = "-".join(scripts)
        if  idx not in self._cache.keys():
            data = ''
            if  datatype == 'css':
                data = '@CHARSET "UTF-8";'
            for script in args:
                path = os.path.join(sys.path[0], resource[script])
                path = os.path.normpath(path)
                ifile = open(path)
                data = "\n".join ([data, ifile.read().\
                    replace('@CHARSET "UTF-8";', '')])
                ifile.close()
            if  datatype == 'css':
                set_headers("text/css")
            if  minimize:
                self._cache[idx] = minify(data)
            else:
                self._cache[idx] = data
        return self._cache[idx]

    def check_scripts(self, scripts, resource, path):
        """
        Check a script is known to the resource map
        and that the script actually exists
        """
        for script in scripts:
            if  script not in resource.keys():
                spath = os.path.normpath(os.path.join(path, script))
                if  os.path.isfile(spath):
                    resource.update({script: spath})
        return scripts
