# -*- coding: utf-8 -*-

from odd.data.db import db_session

from odd.models.tag import *

from odd.utils.error import *

def get_tag_by_id(id):
    return db_session.query(Tag).filter_by(id=id).first()

def get_all_tags():
    return db_session.query(Tag).all()

def get_tag_by_tag(tag):
    return db_session.query(Tag).filter_by(tag=tag).first()

def get_tag_by_tags(tags):
    return db_session.query(Tag).filter(Tag.tag.in_(tags)).all()

def get_latest_tags(count, page=0):
    return db_session.query(Tag).order_by(Tag.id.desc()).limit(count).offset(page*count).all()

def new_tag(tag):
    try:
        db_session.begin()
        db_session.add(tag)
        db_session.commit()
        return TAG_ADD_OK
    except:
        db_session.rollback()
        return TAG_DUPLICATE

def new_tags(tags):
    for tag in tags:
        new_tag(Tag(tag))
    return TAG_ADD_OK

def new_tag_edit(tag_edit):
    db_session.begin()
    db_session.add(tag_edit)
    db_session.commit()
    return TAG_EDIT_ADD_OK

def edit_tag(tag):
    db_session.begin()
    db_session.add(tag)
    db_session.commit()
    return TAG_EDIT_OK
