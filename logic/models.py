from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from logic import db

class Login(db.Model):
    __tablename__ = 'login'
    id = Column(Integer, primary_key = True)
    usern = Column(String)
    passw = Column(String)

class Alias(db.Model):
    __tablename__ = 'alias'
    id = Column(Integer, primary_key = True)
    name = Column(String)
    pic_profile = Column(String)
    description = Column(String)
    decomp = Column(String)

class Alias_Reference(db.Model):
    __tablename__ = 'alias_reference'
    id = Column(Integer)
    user = Column(Integer, ForeignKey('login.id'))
    alias = Column(Integer, ForeignKey('alias.id'))

class Thread(db.Model):
    __tablename__ = 'thread'
    id = Column(Integer)
    public = Column(Integer)
    name = Column(String)
    parent = Column(Integer)
    description = Column(String)
    banner = Column(String)

class Permissions(db.Model):
    __tablename__ = 'permissions'
    id = Column(Integer)
    thread = Column(Integer)
    user = Column(Integer)
    permissions = Column(Integer)

class Messages(db.Model):
    __tablename__ = 'messages'
    id = Column(Integer)
    alias = Column(Integer, ForeignKey('alias.id'))
    thread = Column(Integer, ForeignKey('thread.id'))
    content = Column(String)
    timestamp = Column(DateTime)
    edit = Column(Boolean)