# -*- coding: utf-8 -*-

from flaskext.login import logout_user, login_user

from hashlib import md5

from odd.data.db import db_session
from odd.models.user import User

from odd.utils.error import *

def get_user_by_id(id):
    user = db_session.query(User).filter_by(id=id).first()
    return user

def get_user_by_email(email):
    user = db_session.query(User).filter_by(email=email).first()
    return user

def get_user_by_name(nickname):
    user = db_session.query(User).filter_by(nickname=nickname).first()
    return user

def register_user(user):
    if get_user_by_email(user.email):
        return USER_DUPLICATE

    if get_user_by_name(user.nickname):
        return USER_DUPLICATE

    db_session.add(user)
    db_session.commit()
    return USER_REGISTER_OK

def edit_user(user):
    db_session.add(user)
    db_session.commit()
    return USER_EDIT_OK

def user_login(user, remember):
    u = db_session.query(User).filter_by(email=user.email, passwd=user.passwd).first()
    
    if not u:
        return USER_NOT_EXIST

    user.id = u.id
    user.nickname = u.nickname
    login_user(u, remember=remember)

    return USER_LOGIN_OK

def user_logout():
    logout_user()
    return USER_LOGOUT_OK
