from WMCore.Configuration import Configuration
from WMCore.WMBase import getWMBASE
import os.path
import logging
from os import environ

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

# This is the config for the application
config.component_('ReqMgr')

# Define the default location for templates for the app
config.ReqMgr.tmpldir = environ['RM_TMPLPATH']
config.ReqMgr.cssdir = environ['RM_CSSPATH']
config.ReqMgr.jsdir = environ['RM_JSPATH']
config.ReqMgr.imgdir = environ['RM_IMAGESPATH']
config.ReqMgr.admin = 'vkuznet [AT] gmail com'
config.ReqMgr.title = 'CMS ReqMgr Service'
config.ReqMgr.description = 'Documentation on the ReqMgr'
config.ReqMgr.index = 'reqmgr'
config.ReqMgr.base = '/reqmgr/reqmgr'

# Views are all pages 
config.ReqMgr.section_('views')

# These are all the active pages that Root.py should instantiate 
active = config.ReqMgr.views.section_('active')
active.section_('documentation')
active.documentation.object = 'WMCore.WebTools.Documentation'

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

