# coding:utf-8
__author__ = 'john'

import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
app = Flask(__name__)


app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql+pymysql://root:***@127.0.0.1:3306/artcms_pro'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)

'''
/*
用户表
编号，账号，密码，时间
*/
'''


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    pwd = db.Column(db.String(100), nullable=False)
    addtime = db.Column(db.DATETIME, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name

    def check_pwd(self,pwd):
        return check_password_hash(self.pwd,pwd)


class Art(db.Model):
    __tablename__ = 'art'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    cate = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    logo = db.Column(db.Integer, nullable=False)
    content = db.Column(db.TEXT, nullable=False)
    addtime = db.Column(db.DATETIME, nullable=False)

    def __repr__(self):
        return "<Art %r>" % self.title


if __name__ == '__main__':
    pass
    #db.create_all()
    #user = db.session.add(User('name' = u''))
