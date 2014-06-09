# -*- coding: utf-8 -*-
"""
Created on Sun Jun 08 16:12:25 2014

@author: Eelco
"""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relation, relationship, backref
import datetime

Base = declarative_base()
clientverzorger = Table('clientverzorger', Base.metadata, Column('client_id', Integer, ForeignKey('client.id')), Column('verzorger_id', Integer, ForeignKey('verzorger.id')))
clientbehandelaar = Table('clientbehandelaar', Base.metadata, Column('client_id', Integer, ForeignKey('client.id')), Column('behandelaar_id', Integer, ForeignKey('behandelaar.id')))
clientoverig = Table('clientoverig', Base.metadata, Column('client_id', Integer, ForeignKey('client.id')), Column('overig_id', Integer, ForeignKey('overig.id')))
persoonannotatie = Table('persoonannotatie', Base.metadata, Column('persoon_id', Integer, ForeignKey('persoon.id')), Column('annotatie_id', Integer, ForeignKey('annotatie.id')))
userpersoon = Table('userpersoon', Base.metadata, Column('user_id', Integer, ForeignKey('user.id')), Column('persoon_id', Integer, ForeignKey('persoon.id')))

class Persoon(Base):
    __tablename__ = "persoon"
    id = Column(Integer, primary_key=True)
    Voornaam = Column(String)
    Tussenvoegsel = Column(String)
    Achternaam = Column(String)
    Geslacht = Column(Boolean)
    Email = Column(String)
    Telefoon = Column(String)
    Adres = Column(String)
    Plaats = Column(String)
    Postcode = Column(String)
    Rekeningnummer = Column(String)
    Actief = Column(Boolean)
    Type = Column(String)
    annotaties = relationship('Annotatie',secondary='persoonannotatie',backref='annotaties')    
    __mapper_args__ = {
        'polymorphic_identity':'persoon',
        'polymorphic_on':'Type'}

class Verzorger(Persoon):
    __tablename__ = "verzorger"
    id = Column(Integer, ForeignKey('persoon.id'), primary_key=True)
    Rol = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity':'verzorger'
    }

class Behandelaar(Persoon):
    __tablename__ = "behandelaar"
    id = Column(Integer, ForeignKey('persoon.id'), primary_key=True)
    Rol = Column(String)
    Organisatie = Column(String)
    OrgEmail = Column(String)
    OrgTelefoon = Column(String)
    OrgAdres = Column(String)
    OrgPlaats = Column(String)
    OrgPostcode = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity':'behandelaar'    
    }

class Overig(Persoon):
    __tablename__ = "overig"
    id = Column(Integer, ForeignKey('persoon.id'), primary_key=True)
    Rol = Column(String)
    
    __mapper_args__ = {
        'polymorphic_identity':'overig'
    }

class Client(Persoon):
    __tablename__ = "client"
    id = Column(Integer, ForeignKey('persoon.id'), primary_key=True)
    GeboorteDatum = Column(Date)
    verzorgers = relationship('Verzorger', secondary=clientverzorger, backref='clienten')
    behandelaars = relationship('Behandelaar', secondary=clientbehandelaar, backref='clienten')
    
    __mapper_args__ = {
        'polymorphic_identity':'client'    
    }

class Annotatie(Base):
    __tablename__ = "annotatie"
    id = Column(Integer, primary_key=True)
    Onderwerp = Column(String)
    Body = Column(String)
    DateAdded = Column(DateTime)
    DateModified = Column(DateTime)
    user_id = Column(Integer, ForeignKey('user.id'))
    tag_id = Column(Integer, ForeignKey('tag.id'))
    
    def __init__(self, Onderwerp, Body):
        self.Onderwerp = Onderwerp
        self.Body = Body
        self.DateAdded = datetime.datetime.now()
    
class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    TagName = Column(String)
    
    def __init__(self, TagName):
        self.TagName = TagName

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    Username = Column(String)
    Password = Column(String)
    Expires = Column(DateTime)
    persoon_id = Column(Integer, ForeignKey('persoon.id'))
    
    def __init__(self, Username, Password):
        self.UserName = UserName
        self.PassWord = PassWord

engine = create_engine('sqlite:///testdb.sqlite')
Base.metadata.create_all(engine)