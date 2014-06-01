# -*- coding: utf-8 -*-
"""
Created on Fri May 30 13:05:56 2014

@author: Eelco
"""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, String, Integer, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from werkzeug import generate_password_hash, check_password_hash

engine = create_engine('sqlite:///ppadmin.db',echo=True)
Base = declarative_base()

class Persoon(Base):
    __tablename__ = 'persoon'
    id = Column(Integer, primary_key=True)
    voornaam = Column(String)
    tussenvoegsel = Column(String)
    achternaam = Column(String)
    adres = Column(String)
    woonplaats = Column(String)
    land = Column(String)
    rekeningnummer = Column(String)
    actief = Column(Boolean)
    volledig = Column(Boolean)
    
    def __init__(self, voornaam, tussenvoegsel, achternaam):
        self.voornaam = voornaam
        self.tussenvoegsel = tussenvoegsel
        self.achternaam = achternaam
    
class Gebruiker(Base):
    __tablename__ = 'gebruiker'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    password = Column(String)
    
    def __init__(self,user,password):
        self.user = user
        self.password = set_password(password)
    
    def set_password(self, password):
        self.pwdhash = generate_password_hash(password)
   
    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)
        
Base.metadata.create_all(engine)

