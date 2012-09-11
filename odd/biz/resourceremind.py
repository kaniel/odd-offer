# -*- coding: utf-8 -*-
'''
Created on 2012-8-27
@author: lucast
'''

from odd.data.db import db_session

from odd.models.resourceremind import *

from odd.utils.error import *

def get_remind_by_id(id):
    res_remind = db_session.query(Resource_Remind).get(id)
    return res_remind

def get_unread_reminds(uid):
    res_reminds = db_session.query(Resource_Remind).filter_by(user_id=uid, has_read=False).all()
    return res_reminds

def new_res_remind(res_remind):
    db_session.add(res_remind)
    db_session.commit()
    return REMIND_ADD_OK

def edit_res_remind(res_remind):
    db_session.add(res_remind)
    db_session.commit()
    return REMIND_EDIT_OK

