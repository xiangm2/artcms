# coding:utf-8
__author__ = 'john'

from flask_wtf import Form as FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired,EqualTo,ValidationError
from models import User
from flask import session

'''
登录表单：账号，密码，登录按钮
注册表单：账号，密码，二次密码，验证码，注册按钮
发布文章：标题，分类，logo，内容，提交按钮
'''


class LoginForm(FlaskForm):
    name = StringField(label=u'账号', validators=[DataRequired(u'账号不能为空!')],description=u'账号',
                       render_kw={'class': 'form-control','placeholder': u'请输入账号！'})
    pwd = PasswordField(label=u'密码', validators=[DataRequired(u'密码不能为空!')],description=u'密码',
                        render_kw={'class': 'form-control','placeholder': u'请输入密码！'})
    submit = SubmitField(u'登录', render_kw={'class': 'btn btn-primary'})

    def validate_pwd(self,field):
        pwd = field.data
        print self.name.data
        user = User.query.filter_by(name = self.name.data).first()

        if not user.check_pwd(pwd):
            raise ValidationError(u'密码不正确！')



class RegisterForm(FlaskForm):
    name = StringField(label=u'账号', validators=[DataRequired(u'账号不能为空!')],description=u'账号',
                       render_kw={'class': 'form-control','placeholder': u'请输入账号！'})
    pwd = PasswordField(label=u'密码', validators=[DataRequired(u'密码不能为空!')],description=u'密码',
                        render_kw={'class': 'form-control','placeholder': u'请输入密码！'})
    repwd = PasswordField(label=u'确认密码', validators=[DataRequired(u'确认密码不能为空!'),EqualTo('pwd',message=u'两次输入密码不一致！')],
                          description=u'确认密码', render_kw={'class': 'form-control','placeholder': u'请输入密码！'})
    code = StringField(label=u'验证码', validators=[DataRequired(u'验证码不能为空！')], description=u'验证码',
                       render_kw={'class': 'form-contorl', 'placeholder': u'请输入验证码！'})

    submit = SubmitField(u'注册', render_kw={'class': 'btn btn-success'})
    #自定义
    def validate_name(self,field):
        name = field.data
        user = User.query.filter_by(name=name).count()
        if user > 0:
            raise ValidationError(u'账号已经存在，不能重复注册！')

    def validate_code(self,field):
        code = field.data
        if not session.has_key('code'):
            raise ValidationError(u'没有验证码！')
        if session.has_key('code') and  session['code'].lower() != str(code.lower()):
            raise ValidationError(u'验证码不正确！')



class ArtForm(FlaskForm):
    title = StringField(label=u'标题', description=u'标题', validators=[ValidationError(u'标题不能为空')],
                        render_kw={'class': 'form-control', 'placeholder': u'请输入标题！'})
    cata = SelectField(label=u'分类', description=u'分类', validators=[ValidationError(u'分类不能为空')],
                       choices=[(1, u'科技'), (2, u'搞笑'), (3, u'军事')], default=3,
                       coerce=int,
                       render_kw={'class': 'form-control'})
    logo = FileField(label=u'封面', validators=[ValidationError(u'封面不能为空')], description=u'封面',
                     render_kw={'class': 'form-control-file'})
    content = TextAreaField(label=u'内容', validators=[ValidationError(u'内容不能为空')], description=u'内容',
                            render_kw={'style': "height:300px;", 'id': 'content'})

    submit = SubmitField(u'发布文章', render_kw={'class': 'btn btn-primary'})








