#-*- coding:utf-8 -*-
'''
Created on 2012-8-21
@author: lucast
'''

from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import INT, VARCHAR, TIMESTAMP, TEXT, Enum
from odd.data.db import Model
from datetime import datetime

class Resource_Answer(Model):
    __tablename__ = 'resource_answers'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, ForeignKey('users.id'), nullable=False)
    resource_id = Column('resource_id', INT, ForeignKey('resources.id'), nullable=False)
    content = Column('content', TEXT, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False) 
    
    user = relation("User")
    comments = relation("Resource_Comment", backref=backref('resourceanswer'))

    def __init__(self, user_id, resource_id, content):
        self.user_id = user_id
        self.resource_id = resource_id
        self.content = content
        self.create_time = datetime.now()
    
    def __repr__(self):
        return '<Resource_Answer %d,%d>' % (self.user_id, self.resource_id)
    
    
class Resource_Comment(Model):
    __tablename__ = 'resource_comments'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, ForeignKey('users.id'), nullable=False)
    answer_id = Column('answer_id', INT, ForeignKey('resource_answers.id'), nullable=False)
    comment_id = Column('comment_id', INT, ForeignKey('resource_comments.id'), nullable=False)
    content = Column('content', TEXT, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)
    
    user = relation("User")
    comment = relation("Resource_Comment")

    def __init__(self, user_id, answer_id, comment_id, content):
        self.user_id = user_id
        self.answer_id = answer_id
        self.comment_id = comment_id
        self.content = content
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Resource_Comment %d,%d>' % (self.user_id, self.answer_id)