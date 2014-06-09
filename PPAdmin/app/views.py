# -*- coding: utf-8 -*-
"""
Created on Fri May 30 21:58:06 2014

@author: Eelco
"""

from app import app, db, lm, model
from flask import request, render_template, session, redirect, url_for, flash, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from config import navbar
from model import Gebruiker, Persoon

@lm.user_loader
def load_user(id):
    return Gebruiker.query.get(int(id))

@app.before_request
def before_request():
    g.user = current_user

@app.route('/')
@login_required
def index():
    naam = g.user.user.encode("ascii")
    return render_template('index.html', user=naam , navbar=navbar, active='index')

@app.route('/signin', methods=['GET','POST'])
def signin():
    if request.method == 'GET':
        return render_template('signin.html', navbar=navbar, active='signin')
    user = request.form['loginuser']
    password = request.form['loginpass']
    users = db.session.query(Gebruiker).filter(Gebruiker.user==user).all()
    if users == []:
        flash('Username or Password is unknown','error')
        return redirect(url_for('signin'))
    else:
        if users[0].check_password(password):
            flash('Succesvol ingelogd')
            login_user(users[0])
        return redirect(url_for('index'))

@app.route('/signout')
def signout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('about.html', navbar=navbar, active='about', user = 'test', password = 'Broek', status = 'Not applicable')

@app.route('/about')
@login_required
def about():
    naam = g.user.user.encode("ascii")
    return render_template('about.html', navbar=navbar, active='about', user = naam, password = 'Broek', status = 'Not applicable')

@app.route('/clienten',methods=['GET','POST'])
@login_required
def clienten():
    naam = g.user.user.encode("ascii")
    if request.method == 'GET':
        return render_template('clienten.html', navbar=navbar, active='clienten', user=naam, post_result={},mode='start')
    post_result = request.form
    match = []
    match_voornaam = []
    match_achternaam = []
    if 'query' in post_result:
        for word in post_result['query'].split():
            match_voornaam += db.session.query(model.Persoon).filter(model.Persoon.voornaam.contains(word)).all()
            match_achternaam += db.session.query(model.Persoon).filter(model.Persoon.achternaam.contains(word)).all()
        match = match_voornaam+match_achternaam
        search_result = []
        temp = []
        for p in match:
            if not(p in temp):
                temp.append(p)
                search_result.append({'voornaam':p.voornaam, 'tussen':p.tussenvoegsel, 'achternaam':p.achternaam, 'plaats':p.woonplaats, 'id':p.id})
        post_result = match_voornaam
        return render_template('clienten.html', navbar=navbar, active='clienten', user=naam, post_result=post_result, mode='zoek',search_result=search_result)
    if 'newvoornaam'in post_result:
        temp = model.Client(voornaam=post_result['newvoornaam'],tussenvoegsel=post_result['newtussen'],achternaam=post_result['newachternaam'])
        db.session.add(temp)
        db.session.commit()
        return render_template('clienten.html', navbar=navbar, active='clienten', user=naam, post_result=post_result, mode='new_detail')
    
@app.route('/behandelingen')
@login_required
def behandelingen():
    naam = g.user.user.encode("ascii")
    return render_template('behandelingen.html', navbar=navbar, user=naam, active='behandelingen')

@app.route('/facturen')
@login_required
def facturen():
    naam = g.user.user.encode("ascii")
    return render_template('facturen.html', navbar=navbar, user=naam, active='facturen')

@app.route('/beheer')
@login_required
def beheer():
    naam = g.user.user.encode("ascii")
    return render_template('beheer.html', navbar = navbar, user=naam, active = 'beheer')
