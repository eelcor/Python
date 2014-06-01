# -*- coding: utf-8 -*-
"""
Created on Fri May 30 13:05:56 2014

@author: Eelco
"""
"""
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
"""
from werkzeug import generate_password_hash, check_password_hash
from app import db
import datetime

"""
engine = create_engine('sqlite:///ppadmin.db',echo=True)
Base = declarative_base()
"""

class Gebruiker(db.Model):
    __tablename__ = 'gebruiker'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    pwdhash = db.Column(db.String)
    email = db.Column(db.String)
    toegevoegd = db.Column(db.DateTime)
    gewijzigd = db.Column(db.DateTime)
    verloopt = db.Column(db.DateTime)
    rollen = db.relationship("Autorisatiematrix", backref='gebruiker')

    def __init__(self,user,password):
        self.user = user
        self.password = self.set_password(password)
        self.toegevoegd = datetime.datetime.now()
        self.gewijzigd = datetime.datetime.now()
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
    
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def get_id(self):
        return unicode(self.id)
        
    def __repr__(self):
        return('Usernaam %r' % self.user)    

class Persoon(db.Model):
    __tablename__ = 'persoon'
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String)
    tussenvoegsel = db.Column(db.String)
    achternaam = db.Column(db.String)
    adres = db.Column(db.String)
    woonplaats = db.Column(db.String)
    land = db.Column(db.String)
    rekeningnummer = db.Column(db.String)
    actief = db.Column(db.Boolean)
    volledig = db.Column(db.Boolean)
    toegevoegd = db.Column(db.DateTime)
    gewijzigd = db.Column(db.DateTime)
    verloopt = db.Column(db.DateTime)
    
    def __init__(self, voornaam, tussenvoegsel, achternaam):
        self.voornaam = voornaam
        self.tussenvoegsel = tussenvoegsel
        self.achternaam = achternaam
        self.actief = True
        self.toegevoegd = datetime.datetime.now()
        self.gewijzigd = datetime.datetime.now()
    
    def __repr__(self):
        return('Persoon: %r' % self.achternaam)
    
class Autorisatie(db.Model):
    __tablename__= 'autorisatie'
    id = db.Column(db.Integer,primary_key=True)
    description = db.Column(db.String)
    item = db.Column(db.String)
    
    def __init__(self,item):
        self.item = item

class Journaalitem(db.Model):
     __tablename__ = 'journaalitem'
     id = db.Column(db.Integer,primary_key=True)
     geplaatst = db.Column(db.DateTime)
     verslagdatum = db.Column(db.DateTime)
     extra_titel = db.Column(db.String)
     body = db.Column(db.String)
     auteur_id = db.Column(db.Integer, db.ForeignKey('gebruiker.id'))
     client_id = db.Column(db.Integer, db.ForeignKey('persoon.id'))
     auteurs = db.relationship("Gebruiker", backref='journaalitem')
     clienten = db.relationship("Persoon", backref='journaalitem')
     
     def __init__(self,body,verslagdatum):
         self.body = body
         self.verslagdatum = verslagdatum
         self.geplaatst = datetime.datetime.now()

class Autorisatiematrix(db.Model):
    __tablename__ = 'autorisatiematrix'
    gebruiker_id = db.Column(db.Integer,db.ForeignKey('gebruiker.id'), primary_key=True)
    autorisatie_id = db.Column(db.Integer,db.ForeignKey('autorisatie.id'),primary_key=True)
    verloopt = db.Column(db.DateTime)
    autorisatie = db.relationship("Autorisatie", backref="autorisatiematrix")
    
class Gebruikermatrix(db.Model):
    __tablename__ = 'gebruikermatrix'
    persoon_id = db.Column(db.Integer,db.ForeignKey('gebruiker.id'), primary_key=True)
    gebruiker_id = db.Column(db.Integer,db.ForeignKey('persoon.id'), primary_key=True)
    verloopt = db.Column(db.DateTime)
    gebruiker = db.relationship("Gebruiker",backref="gebruikermatrix",uselist=False)

