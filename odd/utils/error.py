# -*- coding: utf-8 -*-

from flask import flash

USER_DUPLICATE = u'用户已存在'
USER_EMAIL_DUPLICATE = u'邮箱地址已被使用'
USER_NICKNAME_DUPLICATE = u'昵称已被使用'
USER_NOT_EXIST = u'用户名或密码错误'
USER_LOGIN_OK = u'欢迎光临'
USER_EDIT_OK = u'信息修改成功'
USER_REGISTER_OK = u'注册成功'
USER_LOGOUT_OK = u'注销成功'

QUESTION_ADD_OK = u'问题发布成功'
QUESTION_EDIT_OK = u'问题修改成功'

QUESTION_EDIT_ADD_OK = u'问题修改记录添加成功'

QUESTION_TAG_ADD_OK = u'问题标签添加成功'
QUESTION_TAG_EDIT_OK = u'问题标签修改成功'

TAG_FOLLOW_ADD_OK = u'关注成功'
TAG_FOLLOW_DUPLICATE = u'已经关注'

ANSWER_ADD_OK = u'回答成功'
ANSWER_ADD_FAIL = u'回答失败'

ANSWER_UP_ADD_OK = u'Up成功'
ANSWER_UP_DUPLICATE = u'Up已存在'

ANSWER_DOWN_ADD_OK = u"Down成功"
ANSWER_DOWN_DUPLICATE = u"Down已存在" 

ANSWER_GOOD_ADD_OK = u"好评成功"
ANSWER_GOOD_DUPLICATE = u"好评失败"

ANSWER_BAD_ADD_OK = u"差评成功"
ANSWER_BAD_DUPLICATE = u"差评失败"

COMMENT_ADD_OK = u'评论成功'

TAG_FOLLOW_ADD_OK = u'关注成功'
TAG_FOLLOW_DEL_OK = u'取消关注成功'

REMIND_ADD_OK = u'提醒添加成功'
REMIND_EDIT_OK = u'提醒修改成功'

TAG_DUPLICATE = u'标签已存在'
TAG_ADD_OK = u'标签添加成功'
TAG_EDIT_OK = u'标签修改成功'

TAG_EDIT_ADD_OK = u'标签修改记录添加成功'

RESOURCE_ADD_OK = u'资源上传成功'
RESOURCE_EDIT_OK = u'资源修改成功'

RESOURCE_EDIT_ADD_OK = u'资源修改记录添加成功'

RESOURCE_DOWNLOAD_ADD_OK = u'资源下载记录添加成功'
RESOURCE_DOWNLOAD_DUPLICATE = u'资源下载记录已存在'

RESOURCE_TAG_EDIT_OK = u'资源标签修改成功'

def success(error):
    flash(error, 'success')

def fail(error):
    flash(error, 'error')
