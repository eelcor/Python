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

#==============================================================================
# Dit zijn de verschillende kruistabellen om gegevens aan elkaar te linken
#==============================================================================

clientverzorger = db.Table('clientverzorger', db.Model.metadata, db.Column('client_id', db.Integer, db.ForeignKey('client.id')), db.Column('verzorger_id', db.Integer, db.ForeignKey('verzorger.id')))
clientbehandelaar = db.Table('clientbehandelaar', db.Model.metadata, db.Column('client_id', db.Integer, db.ForeignKey('client.id')), db.Column('behandelaar_id', db.Integer, db.ForeignKey('behandelaar.id')))
clientoverig = db.Table('clientoverig', db.Model.metadata, db.Column('client_id', db.Integer, db.ForeignKey('client.id')), db.Column('overig_id', db.Integer, db.ForeignKey('overig.id')))
persoonannotatie = db.Table('persoonannotatie', db.Model.metadata, db.Column('persoon_id', db.Integer, db.ForeignKey('persoon.id')), db.Column('annotatie_id', db.Integer, db.ForeignKey('annotatie.id')))
gebruikerpersoon = db.Table('gebruikerpersoon', db.Model.metadata, db.Column('gebruiker_id', db.Integer, db.ForeignKey('gebruiker.id')), db.Column('persoon_id', db.Integer, db.ForeignKey('persoon.id')))


#==============================================================================
# De gebruikers van het systeem
#==============================================================================

class Gebruiker(db.Model):
    __tablename__ = 'gebruiker'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    pwdhash = db.Column(db.String)
    email = db.Column(db.String)
    toegevoegd = db.Column(db.DateTime)
    gewijzigd = db.Column(db.DateTime)
    verloopt = db.Column(db.DateTime)
    profielen = db.relationship('Persoon',secondary=gebruikerpersoon,backref='profiel')    

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

#==============================================================================
# De basisklasse persoon
#==============================================================================

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
    type = db.Column(db.String)
    annotaties = db.relationship('Annotatie',secondary='persoonannotatie',backref='annotaties')    

    __mapper_args__ = {
        'polymorphic_identity':'persoon',
        'polymorphic_on':'type'}
    
#    def __init__(self, voornaam, tussenvoegsel, achternaam):
#        self.voornaam = voornaam
#        self.tussenvoegsel = tussenvoegsel
#        self.achternaam = achternaam
#        self.actief = True
#        self.toegevoegd = datetime.datetime.now()
#        self.gewijzigd = datetime.datetime.now()
    
    def __repr__(self):
        return('Persoon: %r' % self.achternaam)

#==============================================================================
# De vier "personages" die in het systeem gezet kunnen worden
#==============================================================================

class Verzorger(Persoon):
    __tablename__ = "verzorger"
    id = db.Column(db.Integer, db.ForeignKey('persoon.id'), primary_key=True)
    Rol = db.Column(db.String)
    
    __mapper_args__ = {
        'polymorphic_identity':'verzorger'
    }

class Behandelaar(Persoon):
    __tablename__ = "behandelaar"
    id = db.Column(db.Integer, db.ForeignKey('persoon.id'), primary_key=True)
    Rol = db.Column(db.String)
    Organisatie = db.Column(db.String)
    OrgEmail = db.Column(db.String)
    OrgTelefoon = db.Column(db.String)
    OrgAdres = db.Column(db.String)
    OrgPlaats = db.Column(db.String)
    OrgPostcode = db.Column(db.String)
    
    __mapper_args__ = {
        'polymorphic_identity':'behandelaar'    
    }

class Overig(Persoon):
    __tablename__ = "overig"
    id = db.Column(db.Integer, db.ForeignKey('persoon.id'), primary_key=True)
    Rol = db.Column(db.String)
    
    __mapper_args__ = {
        'polymorphic_identity':'overig'
    }

class Client(Persoon):
    __tablename__ = "client"
    id = db.Column(db.Integer, db.ForeignKey('persoon.id'), primary_key=True)
    GeboorteDatum = db.Column(db.Date)
    verzorgers = db.relationship('Verzorger', secondary=clientverzorger, backref='clienten')
    behandelaars = db.relationship('Behandelaar', secondary=clientbehandelaar, backref='clienten')
    
    __mapper_args__ = {
        'polymorphic_identity':'client'    
    }

#==============================================================================
# Opmerkingen, die bij de personen kunnen worden toegevoegd
#==============================================================================

class Annotatie(db.Model):
    __tablename__ = "annotatie"
    id = db.Column(db.Integer, primary_key=True)
    Onderwerp = db.Column(db.String)
    Body = db.Column(db.String)
    DateAdded = db.Column(db.DateTime)
    DateModified = db.Column(db.DateTime)
    gebruiker_id = db.Column(db.Integer, db.ForeignKey('gebruiker.id'))
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    
    def __init__(self, Onderwerp, Body):
        self.Onderwerp = Onderwerp
        self.Body = Body
        self.DateAdded = datetime.datetime.now()
    
class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    TagName = db.Column(db.String)
    
    def __init__(self, TagName):
        self.TagName = TagName

def init_db():
    db.create_all()
