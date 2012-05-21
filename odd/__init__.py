# -*- coding: utf-8 -*-

from flask import Flask, render_template
from flaskext.login import LoginManager

app = Flask(__name__)
app.config.from_object("websiteconfig")

#
# Blueprints
#
from odd.view import general
from odd.view import user

app.register_blueprint(general.mod)
app.register_blueprint(user.mod)

#
# Login
#
from odd.biz.user import get_user_by_id

login_manager = LoginManager()
login_manager.setup_app(app)
login_manager.login_view = "general.login"
login_manager.login_message = u"这个页面需要登录后才能访问"

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404
