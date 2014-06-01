# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 22:48:47 2013

@author: Eelco
"""

from app import app

@app.route('/')
@app.route('/index')
def index():
    return "Hello, World again!"

@app.route('/test')
def test():
    return "Dit is een test!"