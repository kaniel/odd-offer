# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, abort, request, jsonify
from flask.ext.login import login_required, current_user

from odd.utils.error import *

from odd.biz.tag import *
from odd.biz.question import *
from odd.biz.resource import *

mod = Blueprint('search', __name__, url_prefix='/search')

@mod.route('/')
@login_required
def index():
    query = request.args.get('query')
    if not query:
        abort(404)

    count = 10

    tags = get_tag_by_like(query, count)
    resources = get_resource_by_like(query, count)
    questions = get_question_by_like(query, count)

    return render_template('search/index.html', query=query, tags=tags, questions=questions, resources=resources)

@mod.route('/tips')
def tips():

    query = request.args.get('query')
    if not query:
        return jsonify(status='FAIL')

    count = 10

    tags = [{
        'id': t.id, 
        'tag': t.tag, 
        'photo': t.tag_photo(20)
        } for t in get_tag_by_like(query, count)]
            

    questions = [{
        'id': q.id,
        'title': q.title,
        } for q in get_question_by_like(query, count)]
    
    resources = [{
        'id': r.id,
        'title': r.title,
        } for r in get_resource_by_like(query, count)]

    return jsonify(status='SUCCESS', tags=tags, questions=questions, resources=resources)
