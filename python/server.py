#!/usr/bin/env python

import os
import cherrypy
from webmgr import WebManager

def main():
    "Main function"
    port = os.environ.get('WEB_PORT', 8080)
    print "port", port
    cherrypy.config.update({'server.socket_port': int(port)})
    conf={'/': {'tools.staticdir.root': os.getcwd(),
                'tools.response_headers.on':True,
                'tools.response_headers.headers':
                 [('Expires','Thu, 15 Apr 2010 20:00:00 GMT'),
                  ('Cache-Control','no-store, no-cache, must-revalidate,post-check=0, pre-check=0')]
              }, 
        }
    cherrypy.quickstart(WebManager(), '/', config=conf)

if __name__ == '__main__':
    main()

