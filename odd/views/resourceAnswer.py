#-*- coding:utf-8 -*-
'''
Created on 2012-8-21
@author: lucast
'''

from flask import Blueprint, url_for, redirect, render_template, abort, request, jsonify
from flask.ext.login import login_required, current_user

from odd.utils.error import *

from odd.biz.resourceAnswer import *
from odd.biz.resourceremind import *

from functools import wraps

from re import match

mod = Blueprint('resourecanswer', __name__, url_prefix='/resource/resanswer')

@mod.route('/')
@login_required
def index():
    return ''

@mod.route('/new', methods=['POST'])
@login_required
def new():
    form = request.form
    resource_id = form.get('resource_id')
    content = form.get('content')
    if not resource_id or not content:
        return jsonify(errno='FAIL')

    answer = Resource_Answer(current_user.id, resource_id, content)
    ret = new_answer(answer)
    if ret != ANSWER_ADD_OK:
        return jsonify(errno='FAIL')

    resource = answer.resource
    res_remind = Resource_Remind(resource.user.id, resource.id, resource.title, 
                               answer.id, answer.content, -1, '')
    new_res_remind(res_remind)

    return jsonify(errno='SUCCESS')

@mod.route('/comment', methods=['POST'])
@login_required
def comment():
    form = request.form
    answer_id = form.get('answer_id')
    comment_id = form.get('comment_id')
    content = form.get('content')
    if not answer_id or not comment_id or not content:
        return jsonify(errno='FAIL')

    comm = Resource_Comment(current_user.id, answer_id, comment_id, content)
    ret = new_comment(comm)
    if ret != COMMENT_ADD_OK:
        return jsonify(errno='FAIL')

    user_id = comm.comment.user.id if comm.comment else comm.resourceanswer.user.id
    resanswer = comm.resourceanswer
    res = resanswer.resource
    resremind = Resource_Remind(user_id, res.id, res.title, resanswer.id, resanswer.content, comm.id, comm.content)
    new_res_remind(resremind)

    return jsonify(errno='SUCCESS')


