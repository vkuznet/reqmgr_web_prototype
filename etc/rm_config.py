from WMCore.Configuration import Configuration
from WMCore.WMBase import getWMBASE
import os.path
import socket
import logging
from os import environ

# some useful settings
CONFIGDIR = os.path.normcase(os.path.abspath(__file__)).rsplit('/', 1)[0]
TOPDIR    = os.path.normpath(os.path.join(CONFIGDIR, '../../..'))
STATEDIR  = "%s/state/reqmgr" % TOPDIR
LOGDIR    = "%s/logs/reqmgr" % TOPDIR

serverHostName = socket.getfqdn().lower()
workDirectory = STATEDIR

config = Configuration()

# This component has all the configuration of CherryPy
config.component_('Webtools')

# This is the application
config.Webtools.port = 18765
# INADDR_ANY: listen on all interfaces (be visible outside of localhost)
config.Webtools.host = '0.0.0.0' 
config.Webtools.application = 'ReqMgr'
# uncomment lines below for more debug printouts
#config.Webtools.environment = 'development'
#config.Webtools.log_screen = True
#config.Webtools.error_log_level = logging.DEBUG

# general section
config.section_("General")
config.General.workDir = workDirectory

# This is the config for the application
config.component_('ReqMgr')

# Define the default location for templates for the app
config.ReqMgr.componentDir = config.General.workDir + "/ReqMgr"
config.ReqMgr.tmpldir = environ['RM_TMPLPATH']
config.ReqMgr.cssdir = environ['RM_CSSPATH']
config.ReqMgr.jsdir = environ['RM_JSPATH']
config.ReqMgr.imgdir = environ['RM_IMAGESPATH']
config.ReqMgr.admin = 'vkuznet [AT] gmail com'
config.ReqMgr.title = 'CMS ReqMgr Service'
config.ReqMgr.description = 'Documentation on the ReqMgr'
config.ReqMgr.index = 'reqmgr'
config.ReqMgr.base = '/reqmgr'

# Views are all pages 
config.ReqMgr.section_('views')

# These are all the active pages that Root.py should instantiate 
active = config.ReqMgr.views.section_('active')
active.section_('reqmgr')
active.reqmgr.object = 'ReqMgrService' # put Python path, e.g. web.Object... to this module if it is required

# ReqMgr WebServer configuration
rmws = config.ReqMgr.section_('rmws')
rmws.verbose = 1

# Security module stuff
config.component_('SecurityModule')
#config.SecurityModule.key_file = '/Users/vk/Work/Tools/apache/install_2.2.19/binkey'
config.SecurityModule.key_file = '/Users/vk/CMS/DMWM/GIT/FileMover/header-auth-key'
config.SecurityModule.store = 'filestore'
config.SecurityModule.store_path = '/tmp/security-store'
config.SecurityModule.mount_point = 'auth'
#config.CernOpenID.store.database = 'sqlite://'
#config.SecurityModule.session_name = 'SecurityModule'
#config.SecurityModule.oid_server = 'http://localhost:8400/'
#config.SecurityModule.handler = 'WMCore.WebTools.OidDefaultHandler'

# NEW STUFF FROM REQMGR2

views = config.section_("views")

# practical to have this kind of configuration values not in
# service related RPM (difficult/impossible to change in CMS web
# deployment) but in the deployment configuration for the service

# redirector for the REST API implemented handlers
data = views.section_("data")
data.object = "WMCore.ReqMgr.Service.RestApiHub.RestApiHub"
# The couch host is defined during deployment time.
data.couch_host = "http://127.0.0.1:5984"
# main ReqMgr CouchDB database containing all requests with spec files attached
data.couch_reqmgr_db = "reqmgr_workload_cache"
# ReqMgr database containing groups, teams, software, etc
data.couch_reqmgr_aux_db = "reqmgr_auxiliary"
# ConfigCache - database with configuration documents
data.couch_config_cache_db = "reqmgr_config_cache"
data.couch_workload_summary_db = "workloadsummary"
data.couch_wmstats_db = "wmstats"
# number of past days since when to display requests in the default view
data.default_view_requests_since_num_days = 30 # days
# resource to fetch CMS software versions and scramarch info from
data.tag_collector_url = "https://cmssdt.cern.ch/SDT/cgi-bin/ReleasesXML?anytype=1"
# another source at TC, returns directly JSON, but strangely formatted (e.g.
# keys are not present at easy item but defined in a dedicated item ...)
# https://cmssdt.cern.ch/tc/getReleasesInformation?release_state=Announced

# request related settings (e.g. default injection arguments)
data.default_sw_version = "CMSSW_5_2_5"
data.default_sw_scramarch = "slc5_amd64_gcc434"
data.dqm_url = "https://cmsweb.cern.ch/dqm/dev"
data.dbs_url = "https://cmsweb.cern.ch/dbs/prod/global/DBSReader"

# web user interface
ui = views.section_("ui")
ui.object = "WMCore.ReqMgr.WebGui.FrontPage.FrontPage"
ui.static_content_dir = path.join(path.abspath(__file__.rsplit('/', 3)[0]),
                                 "apps",
                                 main.application,
                                 "data")
