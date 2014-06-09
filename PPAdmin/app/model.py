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
# Dit zijn kruistabellen als klassen
#==============================================================================

class AnnotatieTag(db.Model):
    __tablename__ = 'annotatietag'
    annotatie_id = db.Column(db.Integer, db.ForeignKey('annotatie.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'),primary_key=True)

class PersoonFormulier(db.Model):
    __tablename__ = 'persoonformulier'
    formulier_id = db.Column(db.Integer, db.ForeignKey('formulier.id'), primary_key=True)
    persoon_id = db.Column(db.Integer, db.ForeignKey('persoon.id'), primary_key=True)

#==============================================================================
# Authorization block
#==============================================================================

class AutorisatieLezen(db.Model):
    __tablename__= 'autorisatielezen'
    lezer_id = db.Column(db.Integer, db.ForeignKey('gebruiker.id'), primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)

class AutorisatieSchrijven(db.Model):
    __tablename__='autorisatieschrijven'
    schrijver_id = db.Column(db.Integer, db.ForeignKey('gebruiker.id'), primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)

class AutorisatieBeheer(db.Model):
    __tablename__ = 'autorisatiebeheer'
    beheerder_id = db.Column(db.Integer, db.ForeignKey('gebruiker.id'), primary_key=True)
    object_id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)

class Object(db.Model):
    __tablename__='object'
    id = db.Column(db.Integer, primary_key=True)
    lezers = db.relationship('Gebruiker', secondary='autorisatielezen', backref='objlezers')
    schrijvers = db.relationship('Gebruiker', secondary='autorisatieschrijven', backref='objschrijvers')
    beheerders = db.relationship('Gebruiker', secondary='autorisatiebeheer', backref='objbeheerders')

    def check_autorisaties(self,Gebruiker):
        autorisaties = []
        if Gebruiker in self.beheerders:
            autorisaties.append('beheer')
        if Gebruiker in self.schrijvers:
            autorisaties.append('schrijven')
        if Gebruiker in self.lezers:
            autorisaties.append('lezen')
        return autorisaties
#==============================================================================
# De gebruikers van het systeem
#==============================================================================

class Gebruiker(db.Model):
    __tablename__ = 'gebruiker'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String)
    pwdhash = db.Column(db.String)
    beheerder = db.Column(db.Boolean)
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

class Persoon(Object):
    __tablename__ = 'persoon'
    id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)
    voornaam = db.Column(db.String)
    tussenvoegsel = db.Column(db.String)
    achternaam = db.Column(db.String)
    adres = db.Column(db.String)
    woonplaats = db.Column(db.String)
    land = db.Column(db.String)
    bsn = db.Column(db.String)
    rekeningnummer = db.Column(db.String)
    actief = db.Column(db.Boolean)
    volledig = db.Column(db.Boolean)
    toegevoegd = db.Column(db.DateTime)
    gewijzigd = db.Column(db.DateTime)
    verloopt = db.Column(db.DateTime)
    type = db.Column(db.String)
    annotaties = db.relationship('Annotatie',secondary='persoonannotatie',backref='annotaties')    
    formulieren = db.relationship('Formulier',secondary='persoonformulier', backref='formpers')
    
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

class Annotatie(Object):
    __tablename__ = "annotatie"
    id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)
    Onderwerp = db.Column(db.String)
    Body = db.Column(db.String)
    DateAdded = db.Column(db.DateTime)
    DateModified = db.Column(db.DateTime)
    gebruiker_id = db.Column(db.Integer, db.ForeignKey('gebruiker.id'))
    gebruikers = db.relationship('Gebruiker',backref='annogebruikers')
    tags = db.relationship('Tag', secondary='annotatietag', backref='annotag')
    
    def __init__(self, Onderwerp, Body):
        self.Onderwerp = Onderwerp
        self.Body = Body
        self.DateAdded = datetime.datetime.now()
    
class Tag(Object):
    __tablename__ = "tag"
    id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)
    TagName = db.Column(db.String)
    annotaties = db.relationship('Annotatie', secondary='annotatietag', backref='tagannotaties')

    def __init__(self, TagName):
        self.TagName = TagName

#==============================================================================
# Standaard formulieren
#==============================================================================

class Formulier(Object):
    __tablename__ = "formulier"
    id = db.Column(db.Integer, db.ForeignKey('object.id'), primary_key=True)
    soort = db.Column(db.String)
    opmerking = db.Column(db.String)
    aangemaakt = db.Column(db.DateTime)
    gewijzigd = db.Column(db.DateTime)
    type = db.Column(db.String)
    personen = db.relationship('Persoon', secondary='persoonformulier', backref='formpersonen')

    __mapper_args__ = {
        'polymorphic_identity':'formulier',
        'polymorphic_on':'type'}

class Verwijsbrief(Formulier):
    __tablename__ = "verwijsbrief"
    id = db.Column(db.Integer, db.ForeignKey('formulier.id'), primary_key=True) 
    soort = db.Column(db.String)
    
    __mapper_args__ = {
        'polymorphic_identity':'verwijsbrief'
        }

def init_db():
    db.create_all()
