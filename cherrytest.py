# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 21:59:55 2013

@author: Eelco
"""

import cherrypy
class HelloWorld:
    def index(self):
        return "Hello World!"
    index.exposed = True

cherrypy.quickstart(HelloWorld())