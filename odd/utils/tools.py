# -*- coding: utf-8 -*-

from os import makedirs
from os.path import splitext, join, isdir, sep, altsep
from subprocess import call
from re import compile
from odd import app

_filename_strip_re = compile(r'[^A-Za-z0-9_.-]')

def secure_filename(filename, default):
    for s in sep, altsep:
        if s:
            filename = filename.replace(s, ' ')
    filename = '_'.join(filename.split()).strip('._')
    #filename = str(_filename_strip_re.sub('', filename))
    if not filename:
        filename = default
    return filename


def file_type(file_name):
    ext = splitext(file_name)[1][1:].lower()
    return ext

def save_photo(id, img):
    photo_path = app.static_folder+'/photos'
    ext = file_type(img.filename)
    if not ext in app.config['ALLOWED_IMGS']:
        return False
    img_name = '%d.%s' % (id, ext)
    path = join(photo_path, img_name)
    img.save(path)
    cv = 'cd %s && convert -size 20x20 %s -resize 20x20 %d-20.jpg && convert -size 90x90 %s -resize 90x90 %d-90.jpg'
    call(cv % (photo_path, img_name, id, img_name, id), shell=True)
    return True

def save_tag_photo(id, img):
    photo_path = app.static_folder+'/tag_photos'
    ext = file_type(img.filename)
    if not ext in app.config['ALLOWED_IMGS']:
        return False
    img_name = '%d.%s' % (id, ext)
    path = join(photo_path, img_name)
    img.save(path)
    cv = 'cd %s && convert -size 20x20 %s -resize 20x20 %d-20.jpg && convert -size 90x90 %s -resize 90x90 %d-90.jpg'
    call(cv % (photo_path, img_name, id, img_name, id), shell=True)
    return True

def save_resource(id, files):
    resources_path = app.static_folder+'/resources'
    res_path = join(resources_path, str(id))
    if not isdir(res_path):
        makedirs(res_path)
    for f in files:
        filename = secure_filename(f.filename, 'file')
        f.save(join(res_path, filename))
    zip_cmd = 'cd %s && zip -r %d.zip %d'
    call(zip_cmd % (resources_path, id, id), shell=True)
    return True
