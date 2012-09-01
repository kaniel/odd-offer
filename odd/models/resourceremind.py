# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import INT, Boolean, TIMESTAMP, VARCHAR

from odd.data.db import Model
'''
Created on 2012-8-27
@author: lucast
'''
class ResourceRemind(Model):
    __tablename__ = 'resource_reminds'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, nullable=False)
    resource_id = Column('resource_id', INT, nullable=False)
    resource_title = Column('resource_title', VARCHAR(10), nullable=False)
    answer_id = Column('answer_id', INT, nullable=False)
    answer_content = Column('answer_content', VARCHAR(10), nullable=False)
    comment_id = Column('comment_id', INT, nullable=False)
    comment_content = Column('comment_content', VARCHAR(10), nullable=False)
    has_read = Column('has_read', Boolean, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)

    def __init__(self, user_id, resource_id, resource_title, answer_id, answer_content, comment_id, comment_content,  has_read=0):
        self.user_id = user_id
        self.resource_id = resource_id
        self.resource_title = resource_title[0:10]
        self.answer_id = answer_id
        self.answer_content = answer_content[0:10]
        self.comment_id = comment_id
        self.comment_content = comment_content[0:10]
        self.has_read = has_read
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Resource_Remind %d,%d>' % (self.user_id, self.resource_id)