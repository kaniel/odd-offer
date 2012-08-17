# -*- coding: utf-8 -*-

from odd.data.db import db_session

from odd.models.answer import *
from odd.models.question import *

from odd.utils.error import *

def new_answer(answer):
    db_session.add(answer)

    question = db_session.query(Question).get(answer.question_id)
    question.answer_count += 1
    
    db_session.commit()
    return ANSWER_ADD_OK



def new_answer_mark(answer_mark):
    au = db_session.query(Answer_Marks).filter_by(answer_id=answer_mark.answer_id, 
            user_id=answer_mark.user_id).first()
    if au:
        if answer_mark.answer_type == 0 :
            return ANSWER_UP_DUPLICATE
        if answer_mark.answer_type == 1 :
            return ANSWER_DOWN_DUPLICATE

    db_session.add(answer_mark)

    answer = db_session.query(Answer).get(answer_mark.answer_id)
    if answer_mark.answer_type == 0 :
        answer.score += 1
        answer.up +=1
        db_session.commit()
        return ANSWER_UP_ADD_OK
    elif answer_mark.answer_type == 1 :
        answer.score -= 1
        answer.down += 1
        db_session.commit()
        return ANSWER_DOWN_ADD_OK


def new_comment(comment):
    db_session.add(comment)
    db_session.commit()
    return COMMENT_ADD_OK
