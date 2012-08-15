# -*- coding: utf-8 -*-

import oursql

conn = oursql.connect(host='127.0.0.1', user='root', passwd='234', db='odd', port=3306)
curs = conn.cursor(oursql.DictCursor)
