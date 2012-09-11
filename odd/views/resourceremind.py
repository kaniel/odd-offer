# -*- coding: utf-8 -*-
'''
Created on 2012-8-27

@author: lucast
'''

from time import sleep

from flask import Blueprint, url_for, redirect, render_template, abort, request, jsonify
from flask.ext.login import login_required, current_user

from odd.utils.error import *

from odd.biz.resourceremind import *

mod = Blueprint('resremind', __name__, url_prefix='/resremind')

@mod.route('/', methods=['GET'])
@login_required
def index():
    '''
    while True:
        reminds = get_unread_reminds(current_user.id)
        if reminds:
            break
        sleep(5)
    '''
    reminds = get_unread_reminds(current_user.id)
    rdicts = []
    for r in reminds:
        rdicts.append({
            'id': r.id,
            'type': 'answer' if r.comment_id==-1 else 'comment',
            'resource': r.resource_title,
            'answer': r.answer_content,
            'comment': r.comment_content
            })
    return jsonify(errno='SUCCESS', reminds = rdicts)

@mod.route('/read', methods=['GET'])
@login_required
def read():
    args = request.args
    id = args.get('id')
    if not id:
        return abort(404)
    
    remind = get_remind_by_id(id)
    remind.has_read = True
    edit_res_remind(remind)
    
    return redirect(url_for('resource.index', id=remind.resource_id, answer_id=remind.answer_id, comment_id=remind.comment_id))
