# -*- coding: utf-8 -*-

from flask import flash

USER_DUPLICATE = u'用户已存在'
USER_NOT_EXIST = u'用户名或密码错误'
USER_LOGIN_OK = u'欢迎光临'
USER_EDIT_OK = u'信息修改成功'
USER_REGISTER_OK = u'注册成功'
USER_LOGOUT_OK = u'注销成功'

QUESTION_ADD_OK = u'问题发布成功'
QUESTION_TAG_ADD_OK = u'tag添加成功'

def success(error):
    flash(error, 'success')

def fail(error):
    flash(error, 'error')