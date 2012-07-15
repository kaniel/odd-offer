# -*- coding: utf-8 -*-

from os import listdir
from os.path import join
from datetime import datetime

from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import INT, VARCHAR, TIMESTAMP, TEXT

from flask import json, url_for

from odd import app
from odd.data.db import Model

class Resource(Model):
    __tablename__ = 'resources'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, ForeignKey('users.id'), nullable=False)
    title = Column('title', VARCHAR(128), nullable=False)
    desc = Column('description', TEXT, nullable=False)
    file_list = Column('file_list', VARCHAR(512), nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)
    download_count = Column('download_count', INT, nullable=False)
    
    user = relation('User')
    tags = relation("Resource_Tag", backref=backref('resource'), order_by='Resource_Tag.id')

    def __init__(self, user_id, title, desc, file_list, tags):
        self.user_id = user_id
        self.title = title
        self.desc = desc
        self.file_list = file_list
        self.tags = [Resource_Tag(self.id, tag) for tag in tags]
        self.create_time = datetime.now()
        self.download_count = 0

    def files(self):
        return json.loads(self.file_list)

    def zip_url(self):
        return url_for('general.zip', id=self.id)

    def file_url(self, file):
        return '/resources/%d/%s' % (self.id, file)
        
    def __repr__(self):
        return '<Resource %r>' % self.title

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
