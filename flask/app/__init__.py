# -*- coding: utf-8 -*-
"""
Created on Wed Aug 14 22:47:48 2013

@author: Eelco
"""

from flask import Flask

app = Flask(__name__)
from app import views