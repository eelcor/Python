# -*- coding: utf-8 -*-
"""
Created on Fri May 30 21:58:06 2014

@author: Eelco
"""

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager

app = Flask(__name__)
app.config['DEBUG']=True
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///ppadmin.db?check_same_thread=False"
app.config['SECRET_KEY']='eelcos secret key'
db = SQLAlchemy(app)
lm = LoginManager()
lm.init_app(app)
lm.login_view = 'signin'

from app import views, model

