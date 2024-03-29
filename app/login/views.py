#-*- coding: utf-8 -*-                                                                                     

from flask import render_template, request, redirect, flash
from flask.ext.login import login_user, logout_user
from app.models import  User
from app.login.forms import RegisterForm, LoginForm
from app import lm

from . import login

@lm.user_loader
def load_user(id):
    user = User.objects(id=id)
    if user:
        return user.first()
    else:
        return ''


@login.route('/Register')
def register():
    register_form = RegisterForm()
    return render_template('register.html', form=register_form)


@login.route('/handle_register', methods=['POST'])
def handle_register():
    register_form_info = RegisterForm(request.form)
    if register_form_info.validate():
        if User.objects(username=register_form_info.username.data):
            flash(u'用户名己被注册')
            return register()
        else:
            new_user = User(username=register_form_info.username.data, password=register_form_info.password.data,
                            nickname=register_form_info.nickname.data, email=register_form_info.email.data)
            new_user.save()
            login_user(user=new_user, remember=True)
            flash(u'注册成功, 登录成功')
            return redirect('/')
    else:
        flash(u'用户名或密码不符合要求')
        return register()


@login.route('/Login')
def login_index():
    login_form = LoginForm()
    return render_template('login.html', form=login_form)


@login.route('/handle_login', methods=['POST'])
def handle_login():
    login_form_info = LoginForm(request.form)
    if login_form_info.validate():
        username = login_form_info.username.data
        password = login_form_info.password.data
        if '@' in username:
            user_online = User.objects(email=username, password=password)
        else:
            user_online = User.objects(username=username, password=password)

        if user_online:
            login_user(user=user_online.first(), remember=True)
            return redirect('/')
        else:
            flash(u'帐号与密码不匹配')
            return login_index()
    else:
        flash(u'非法输入')
        return login_index()


@login.route('/Logout')
def handle_logout():
    logout_user()
    flash(u'己登出')
    return redirect('/')


