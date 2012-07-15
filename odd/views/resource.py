# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, redirect, render_template, abort, request, jsonify, json
from flask.ext.login import login_required, current_user
from flask.ext.wtf import Form, TextField, TextAreaField, FileField, FieldList, Required, Length

from odd.utils.error import *
from odd.utils.tools import *

from odd.models.resource import *
from odd.biz.resource import *

mod = Blueprint('resource', __name__, url_prefix='/resource')

@mod.route('/<id>')
@login_required
def index(id):
    resource = get_resource_by_id(id)
    if not resource:
        abort(404)

    return render_template('resource/index.html', resource=resource)

@mod.route('/<id>/download', methods=['POST'])
@login_required
def download(id):
    resource = get_resource_by_id(id)
    if not resource:
        return jsonify(errno='FAIL')
    
    rd = Resource_Download(id, current_user.id)
    new_resource_download(rd)

    return jsonify(errno='SUCCESS')

@mod.route('/list')
@login_required
def list():
    latest_res = get_latest_resources(20)
    hotest_res = get_hotest_resources(20)
    return render_template('resource/list.html', latest_resources=latest_res, hotest_resources=hotest_res)

def clean_tags(tags):
    tags_clean = []
    for t in tags:
        t = t.strip()
        if t and t not in tags_clean:
            tags_clean.append(t)
    return tags_clean

@mod.route('/<int:id>/tags', methods=['POST'])
@login_required
def tags(id):
    tags = request.form.get('tags')
    if not tags:
        return jsonify(status='ERROR', msg=u'label can\'t be empty')

    tags = clean_tags(tags.split(','))

    ret = edit_resource_tags(id, tags)
    if ret != RESOURCE_TAG_EDIT_OK:
        return jsonify(status='ERROR', msg=ret)
    
    resource_edit = Resource_Edit(current_user.id, id, tags)
    new_resource_edit(resource_edit)

    return jsonify(status='OK')

def clean_files(files):
    files_clean = []
    for f in files:
        ext = file_type(f.filename)
        if ext in app.config['ALLOWED_DOCS']:
            f.filename = secure_filename(f.filename)
            files_clean.append(f)
    return files_clean

@mod.route('/new', methods=['GET','POST'])
@login_required
def new():

    form = NewResForm()
    files = clean_files(request.files.getlist('files'))

    if not form.validate_on_submit() or not files:
        if form.is_submitted() and not files:
            form.errors['files'] = [u'请选择文件']

        return render_template('resource/new.html', form=form)
    
    title = form.title.data
    desc = form.desc.data
    file_list = [{'name':f.filename} for f in files]
    tags = clean_tags(form.tags.data.split(','))

    resource = Resource(current_user.id, title, desc, file_list, tags)
    ret = new_resource(resource, tags)
    if ret != RESOURCE_ADD_OK:
        fail(ret)
        return render_template('resource/new.html', form=form)

    save_resource(resource.id, files)

    return redirect(url_for('.index', id=resource.id))

class NewResForm(Form):
    title = TextField(u'标题*', validators=[Required(), Length(max=128)])
    desc = TextAreaField(u'描述*', validators=[Required()])
    tags = TextField(u'Label*', validators=[Required()])
