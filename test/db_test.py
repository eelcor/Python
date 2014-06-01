# -*- coding: utf-8 -*-
"""
Created on Fri May 23 12:02:03 2014

@author: Eelco
"""
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask import abort, request, views, jsonify, make_response, render_template

engine = create_engine('sqlite:///blogs.db')
Session = sessionmaker(bind=engine)
session = Session()


app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
    return('hello world!')

@app.route('/new_post')
def new_post():
    

@app.route('/name/<username>')
def get_username(username):
    return 'My name is %s' % username
    
@app.route('/about')
def about():
    return('<H1>This site belongs to Eelco</H1>')

@app.route('/set/<name>')
def zet_koekje(name):
    resp = make_response(render_template('index.html'))
    resp.set_cookie('username',name, expires=(datetime.datetime.today()+datetime.timedelta(31)))
    return resp

@app.route('/get')
def neem_koekje():
    username = request.cookies.get('username')
    return('Hier is een koekje van %s!' % username)
    
@app.route('/error')
def error():
    abort(401)
    
@app.route('/test')
def test():
    print("Testing the Flask install")
    return('<H1>Test</H1>')
    
if __name__ == "__main__":
    app.run()


