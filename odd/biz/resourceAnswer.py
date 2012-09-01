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

def new_answer_mark(resanswer_mark):
    au = db_session.query(Resource_Answer_Mark).filter_by(answer_id=resanswer_mark.answer_id, 
            user_id=resanswer_mark.user_id).first()
    if au:
        if resanswer_mark.mark_type == 'good' :
            return ANSWER_GOOD_DUPLICATE
        if resanswer_mark.mark_type == 'bad' :
            return ANSWER_BAD_DUPLICATE

    db_session.add(resanswer_mark)

    answer = db_session.query(Resource_Answer).get(resanswer_mark.answer_id)
    if resanswer_mark.mark_type == 'good' :
        answer.score += 1
        answer.good +=1
        db_session.commit()
        return ANSWER_GOOD_ADD_OK
    elif resanswer_mark.mark_type == 'bad' :
        answer.score -= 1
        answer.bad += 1
        db_session.commit()
        return ANSWER_BAD_ADD_OK
    

def new_comment(comment):
    db_session.add(comment)
    db_session.commit()
    return COMMENT_ADD_OK
