#-*- coding:utf-8 -*-
'''
Created on 2012-8-21
@author: lucast
'''

from odd.data.db import db_session

from odd.models.resourceAnswer import *
from odd.models.resource import *

from odd.utils.error import *

def new_answer(resourceanswer):
    db_session.add(resourceanswer)

    resource = db_session.query(Resource).get(resourceanswer.resource_id)
    resource.answer_count += 1
    
    db_session.commit()
    return ANSWER_ADD_OK
    

def new_comment(comment):
    db_session.add(comment)
    db_session.commit()
    return COMMENT_ADD_OK
