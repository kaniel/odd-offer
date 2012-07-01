# -*- coding: utf-8 -*-

from odd.data.db import db_session

from odd.models.resource import *
from odd.models.tag import *

from odd.biz.tag import new_tags

from odd.utils.error import *

def get_resource_by_id(id):
    resource = db_session.query(Resource).get(id)
    return resource

def get_resource_by_uid(uid):
    resources = db_session.query(Resource).filter_by(user_id=uid).order_by(Resource.id.desc()).all()
    return resources

def get_resource_by_tag(tag):
    tags = db_session.query(Resource_Tag).filter_by(tag=tag).all()
    return [t.resource for t in tags]

def get_resource_by_tags(tags):
    tag_objs = []
    if tags:
        tag_objs = db_session.query(Resource_Tag).filter(Resource_Tag.tag.in_(tags)).order_by(Resource_Tag.id.desc()).all()
    rs = []
    for t in tag_objs:
        if not t.resource in rs:
            rs.append(t.resource)
    return rs

def get_latest_resources(count, page=0):
    resources = db_session.query(Resource).order_by(Resource.id.desc()).limit(count).offset(page*count).all()
    return resources

def get_hotest_resources(count):
    resources = db_session.query(Resource).order_by(Resource.download_count.desc(), Resource.id.desc()).limit(count).all()
    return resources

def get_resource_titles(count):
    resources = db_session.query(Resource.id, Resource.title).order_by(Resource.id.desc()).limit(count).all()
    return resources

def new_resource(resource, tags):
    new_tags(tags)
    db_session.add(resource)
    db_session.commit()
    return RESOURCE_ADD_OK

def new_resource_download(rd):
    download = db_session.query(Resource_Download).filter_by(resource_id=rd.resource_id, 
            user_id=rd.user_id).first()
    if download:
        return RESOURCE_DOWNLOAD_DUPLICATE
    
    db_session.add(rd)

    resource = db_session.query(Resource).get(rd.resource_id)
    resource.download_count += 1
    
    db_session.commit()
    return RESOURCE_DOWNLOAD_ADD_OK

def edit_resource_tags(rid, tags):
    new_tags(tags)
    db_session.query(Resource_Tag).filter_by(resource_id=rid).delete()
    db_session.add_all([Resource_Tag(rid,tag) for tag in tags])
    db_session.commit()
    return RESOURCE_TAG_EDIT_OK

def new_resource_edit(resource_edit):
    db_session.add(resource_edit)
    db_session.commit()
    return RESOURCE_EDIT_ADD_OK
