# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flask.ext.login import LoginManager

app = Flask(__name__)

#
# Configs
#
app.config.from_object("website_config")

try:
    app.config.from_pyfile(app.config['PRODUCTION_CONFIG'], silent=False)
    print '[SUCCESS] load config file: ' + app.config['PRODUCTION_CONFIG']
except:
    print '[ERROR] load config file:' + app.config['PRODUCTION_CONFIG']


#
# Blueprints
#
from odd.views import general
from odd.views import user
from odd.views import question
from odd.views import answer
from odd.views import tag
from odd.views import search
from odd.views import follow
from odd.views import remind
from odd.views import admin
from odd.views import resource

app.register_blueprint(general.mod)
app.register_blueprint(user.mod)
app.register_blueprint(question.mod)
app.register_blueprint(answer.mod)
app.register_blueprint(tag.mod)
app.register_blueprint(search.mod)
app.register_blueprint(follow.mod)
app.register_blueprint(remind.mod)
app.register_blueprint(admin.mod)
app.register_blueprint(resource.mod)

#
# Login
#
from odd.biz.user import get_user_by_id

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "general.login"
login_manager.login_message = u"这个页面需要登录后才能访问"

#
# Handler
#
from odd.data.db import db_session

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(413)
def too_large(error):
    return render_template('413.html'), 413

@app.teardown_request
def close_db_session(exception):
    db_session.remove()

#
# Context
#
from odd.biz import getter

@app.context_processor
def insert_getter():
    return dict(getter=getter)


#
# Log
#
if not app.debug:
    import logging
    ft = logging.Formatter(app.config['ERROR_LOG_FORMAT'])
    
    fh = logging.FileHandler(app.config['ERROR_LOG'])
    fh.setFormatter(ft)
    fh.setLevel(logging.WARNING)
    app.logger.addHandler(fh)

    from logging.handlers import SMTPHandler
    sh = SMTPHandler(app.config['MAIL_HOST'], app.config['MY_ADDR'], app.config['ADMIN_ADDRS'], 'Offerduoduo Error!')
    sh.setFormatter(ft)
    sh.setLevel(logging.ERROR)
    app.logger.addHandler(sh)

'''
import logging
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())
'''
