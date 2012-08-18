# -*- coding: utf-8 -*-

from odd.data.db import Model

from sqlalchemy.orm import relation, backref
from sqlalchemy.schema import Column, ForeignKey
from sqlalchemy.types import INT, VARCHAR, TIMESTAMP, TEXT

from datetime import datetime

class Answer(Model):
    __tablename__ = 'answers'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, ForeignKey('users.id'), nullable=False)
    question_id = Column('question_id', INT, ForeignKey('questions.id'), nullable=False)
    content = Column('content', TEXT, nullable=False)
    score = Column('score', INT, nullable=False)
    up = Column('up', INT, nullable=False)
    down= Column('down', INT, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)
    
    user = relation("User")
    comments = relation("Comment", backref=backref('answer'))

    def __init__(self, user_id, question_id, content, score=0, up=0, down=0):
        self.user_id = user_id
        self.question_id = question_id
        self.content = content
        self.score = score
        self.up = up
        self.down = down
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Answer %d,%d>' % (self.user_id, self.question_id)

class Answer_Mark(Model):
    __tablename__ = 'answer_mark'

    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT,  nullable=False)
    answer_id = Column('answer_id', INT,  nullable=False)
    mark_type = Column('mark_type', INT, nullable=False)

    def __init__(self, user_id, answer_id, mark_type):
        self.user_id = user_id
        self.answer_id = answer_id
        self.mark_type = mark_type

    def __repr__(self):
        return '<Answer_Mark %d,%d>' % (self.user_id, self.answer_id)




class Comment(Model):
    __tablename__ = 'comments'
    
    id = Column('id', INT, primary_key=True)
    user_id = Column('user_id', INT, ForeignKey('users.id'), nullable=False)
    answer_id = Column('answer_id', INT, ForeignKey('answers.id'), nullable=False)
    comment_id = Column('comment_id', INT, ForeignKey('comments.id'), nullable=False)
    content = Column('content', TEXT, nullable=False)
    create_time = Column('create_time', TIMESTAMP, nullable=False)
    
    user = relation("User")
    comment = relation("Comment")

    def __init__(self, user_id, answer_id, comment_id, content):
        self.user_id = user_id
        self.answer_id = answer_id
        self.comment_id = comment_id
        self.content = content
        self.create_time = datetime.now()

    def __repr__(self):
        return '<Comment %d,%d>' % (self.user_id, self.answer_id)
