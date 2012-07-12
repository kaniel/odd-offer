# -*- coding: utf-8 -*-

from db import *

import json
from os import listdir
from os.path import isdir

resource_path = u'/home/odd/release/resources'

file_list = []
for f in  listdir(resource_path):
    path = resource_path + '/' + f
    if isdir(path):
        file_list.append({
            'id': f,
            'list': json.dumps([{'name':n}  for n in listdir(path)])
            })

#更新资源的file_list
sql = 'update resources set file_list=? where id=?'
for f in file_list:
    curs.execute(sql,(f['list'],f['id']))
    print f
