# coding:utf-8
__author__ = 'john'

import datetime, os,sys
reload(sys)
sys.setdefaultencoding('utf-8')
from flask import Flask, render_template, redirect, flash, session, Response,url_for,request
from forms import LoginForm, RegisterForm, ArtForm
from models import User, db
from werkzeug.security import generate_password_hash
from coode import Code
from functools import wraps
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ming504102'

#登录装饰器
def user_login_req(f):
    @wraps(f)
    def login_req(*args,**kwargs):
        if 'user' not  in session:
            return redirect(url_for('login',next = request.url))
        return f(*args,**kwargs)
    return login_req


#登录
@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        session['user'] = data['name']
        flash(u'登录成功，Ok！','ok')
        return redirect('/art/list/')
    return render_template('login.html', title=u'登录', form=form)


#注册
@app.route('/register/', methods=['GET', "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        #保存数据
        user = User(name=data['name'],
                    pwd=generate_password_hash(data['pwd']),
                    addtime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
        db.session.add(user)
        db.session.commit()
        #会话闪现
        flash(u'注册成功，请登录！', 'ok')
        return redirect('login/')
    else:
        flash(u'输入正确信息注册！', 'err')
    return render_template('register.html', title=u'注册', form=form)


#退出
@app.route('/logout', methods=['GET'])
@user_login_req
def logout():
    session.pop('user',None)
    return redirect('/login')


#发布文章
@app.route('/art/add/', methods=['GET', 'POST'])
@user_login_req
def art_add():
    form = ArtForm()
    return render_template('art_add.html', title=u'发布文章', form=form)


#编辑文章
@app.route('/art/edit/<int:id>', methods=['GET', 'POST'])
@user_login_req
def art_edit(id):
    form = ArtForm()
    if form.validate_on_submit():
        data = form.data
    return render_template('art_edit.html',form = form)


#文章列表
@app.route('/art/list/', methods=['GET'])
@user_login_req
def art_list():
    if not session.has_key('user'):
        name = u'Stranger'
    else:
        name = session['user']
    return render_template('art_list.html', title=u'文章列表',name = name)


#删除文章
@app.route('/art/del/<int:id>/', methods=["GET"])
@user_login_req
def art_del(id):
    return redirect('/art/list/')


#验证码
@app.route('/code/', methods=['GET'])
def coode():
    c = Code()
    info = c.create_code()
    image = os.path.join(os.path.dirname(__file__), 'static/code') + '/' + info['imge_name']
    print image
    with open(image,'rb') as f:
        image = f.read()
    session['code'] = info['code']
    return Response(image,mimetype='jpeg')


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8080)