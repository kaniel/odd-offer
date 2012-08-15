# -*- coding: utf-8 -*-

from os.path import dirname,abspath

CUR_DIR = dirname(abspath(__file__))

#config
DEBUG = True
SEND_FILE_MAX_AGE_DEFAULT = 1
PRODUCTION_CONFIG = CUR_DIR + '/../website_config.py'

#upload
PHOTOS = CUR_DIR + '/../photos'
TAG_PHOTOS = CUR_DIR + '/../tag_photos'
RESOURCES = CUR_DIR + '/../resources'

#img
ALLOWED_IMGS = ['jpg', 'jpeg', 'png']
ALLOWED_DOCS = ['pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'gif']
MAX_CONTENT_LENGTH = 8 * 1024 * 1024


#secret key
SECRET_KEY = r"42a3e1376f8852d1c0620a3235886bcd712879a3"

#DB
DATABASE_URI = 'mysql+oursql://odd:odd@localhost/odd'
DATABASE_CONNECT_OPTIONS = {
        'pool_recycle': 7200,
        'pool_size': 10,
        'echo_pool': True
        }

#log
ERROR_LOG = CUR_DIR + '/../logs/flask.error.log'
ERROR_LOG_FORMAT = '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'

MAIL_HOST = '127.0.0.1'
MY_ADDR = 'odd@offerduoduo.com'
ADMIN_ADDRS = ['wsxys08@gmail.com']
