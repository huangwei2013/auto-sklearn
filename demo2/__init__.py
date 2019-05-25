#encoding=utf8

from flask_script import Manager,Server

from demo2.controller import *
from demo2.config import *
app = create_app()

# 初始化db
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)
db.create_all()

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


# 注册蓝图

from demo2.utils.ensemble import create_models
from demo2.controller.models import models
from demo2.controller.automl import automl
from demo2.controller.sys import sys

app.register_blueprint(blueprint=models, url_prefix='/models')
app.register_blueprint(blueprint=automl, url_prefix='/automl')
app.register_blueprint(blueprint=sys, url_prefix='/sys')

manager = Manager(app=app)
manager.add_command("runserver", Server(use_debugger=True))

from flask import render_template
@app.errorhandler(404)
def miss(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def error(e):
    return render_template('500.html'), 500
