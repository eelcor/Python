# -*- coding: utf-8 -*-
"""
Created on Fri May 23 06:13:40 2014

@author: Eelco
"""

from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///blogs.db',echo=True)

Base = declarative_base()

class Author(Base):
    
    __tablename__ = "authors"
    
    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    joindate = Column(DateTime)
    
    def __init__(self, name, password, joindate):
        self.name = name
        self.password = password
        self.joindate = joindate

class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True)
    tag_name = Column(String)
    
    def __init__(self, tag_name):
        self.tag_name = tag_name

class PostTag(Base):
    __tablename__ = "posttags"
    
    id = Column(Integer, primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id"))
    post = relationship("Post", backref=backref("posttags", order_by=id))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    tag = relationship("Tag", backref=backref("posttags", order_by=id))
      
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    header = Column(String)
    body = Column(String)
    postdate = Column(DateTime)
    author_id = Column(Integer, ForeignKey("authors.id"))
    author = relationship("Author", backref=backref("posts", order_by=id))
    
    def __init__(self, title, header, body, postdate):
        self.title = title
        self.header = header
        self.body = body
        self.postdate = postdate
        
Base.metadata.create_all(engine)