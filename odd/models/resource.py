# -*- coding: utf-8 -*-

from os import listdir
from os.path import join
from datetime import datetime

from sqlalchemy import *
from sqlalchemy.orm import relation, backref

from flask import json, url_for

from odd import app
from odd.data.db import Model

class JSON(TypeDecorator):
    impl = String
    
    def process_bind_param(self, value, dialect):
        return json.dumps(value)

    def process_result_value(self, value, dialect):
        return json.loads(value)

class Resource(Model):
    __tablename__ = 'resources'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, ForeignKey('users.id'), nullable=False)
    title = Column('title', VARCHAR(128), nullable=False)
    desc = Column('description', TEXT, nullable=False)
    file_list = Column('file_list', JSON, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)
    download_count = Column('download_count', INT, nullable=False)
    answer_count = Column('answer_count', INT, nullable=False)
    score = Column('score', INT, nullable=False)
    good = Column('good', INT, nullable=False)
    bad= Column('bad', INT, nullable=False)

    user = relation('User')
    tags = relation("Resource_Tag", backref=backref('resource'), order_by='Resource_Tag.id')
    resanswers = relation('Resource_Answer', backref=backref('resource'))

    def __init__(self, user_id, title, desc, file_list, tags):
        self.user_id = user_id
        self.title = title
        self.desc = desc
        self.file_list = file_list
        self.tags = [Resource_Tag(self.id, tag) for tag in tags]
        self.create_time = datetime.now()
        self.download_count = 0
        self.answer_count = 0

    def zip_url(self):
        return url_for('general.zip', id=self.id)

    def file_url(self, name):
        return url_for('general.file', id=self.id, name=name)
        
    def __repr__(self):
        return '<Resource %r>' % self.title
    
class Resource_Mark(Model):
    __tablename__ = 'resource_mark'

    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT,  nullable=False)
    resource_id = Column('resource_id', INT,  nullable=False)
    mark_type = Column('mark_type', Enum('good','bad'), nullable=False)
#    mark_type = Column('mark_type', INT, nullable=False)

    def __init__(self, user_id, resource_id, mark_type):
        self.user_id = user_id
        self.resource_id = resource_id
        self.mark_type = mark_type

    def __repr__(self):
        return '<Resource_Answer_Mark %d,%d>' % (self.user_id, self.answer_id)

class Resource_Tag(Model):
    __tablename__ = 'resource_tags'
    
    id = Column('id', INT, primary_key=True)
    resource_id = Column('resource_id', INT, ForeignKey('resources.id'), nullable=False)
    tag = Column('tag', VARCHAR(50), nullable=False)

    def __init__(self, resource_id, tag):
        self.resource_id = resource_id
        self.tag = tag

    def __repr__(self):
        return '<Resource_Tag %d %s>' % (self.resource_id,self.tag)

class Resource_Download(Model):
    __tablename__ = 'resource_downloads'
    
    id = Column('id', INT, primary_key=True)
    resource_id = Column('resource_id', INT, nullable=False)
    user_id = Column('user_id', INT, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)

    def __init__(self, resource_id, user_id):
        self.resource_id = resource_id
        self.user_id = user_id
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Resource_Download %d %s>' % (self.resource_id,self.user_id)

class Resource_Edit(Model):
    __tablename__ = 'resource_edits'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, nullable=False)
    resource_id = Column('resource_id', INT, nullable=False)
    tags = Column('tags', TEXT, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)

    def __init__(self, user_id, resource_id, tags):
        self.user_id = user_id
        self.resource_id = resource_id
        self.tags = ','.join(tags)
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Resource_Edit %s>' % self.id
