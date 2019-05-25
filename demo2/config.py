# -*- coding:utf-8 -*-

import os
from flask import Flask


def create_app():
    # 定义系统路径的变量
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))+'/demo2/'
    # 定义静态文件的路径
    static_dir = os.path.join(BASE_DIR, 'static')
    # 定义模板文件的路径
    templates_dir = os.path.join(BASE_DIR, 'templates')
    # 初始化app 和manage.py文件关联
    app = Flask(__name__,static_folder=static_dir,template_folder=templates_dir)
    
    # 配置数据库
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/Htai'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/mydemo2.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

