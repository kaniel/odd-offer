# -*- coding: utf-8 -*-
'''
Created on 2012-8-27
@author: lucast
'''

from odd.data.db import db_session

from odd.models.resourceremind import *

from odd.utils.error import *

def get_remind_by_id(id):
    resremind = db_session.query(ResourceRemind).get(id)
    return resremind

def get_unread_reminds(uid):
    resreminds = db_session.query(ResourceRemind).filter_by(user_id=uid, has_read=False).all()
    return resreminds

def new_resremind(resremind):
    db_session.add(resremind)
    db_session.commit()
    return REMIND_ADD_OK

def edit_resremind(resremind):
    db_session.add(resremind)
    db_session.commit()
    return REMIND_EDIT_OK

