from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user
from serv import db, bcrypt, Config
from serv.models import User
from serv.users.forms import RegisterForm, LoginForm
from serv import logger


users = Blueprint('users', __name__)


@users.route('/register', methods=['GET', 'POST'])
def register():
    # Can't be logged in to view register page
    if current_user.is_authenticated:
        return redirect(url_for('uploads.home'))

    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(registerForm.password.data)
        user = User(username=registerForm.username.data, email=registerForm.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        logger.log.info('Created user- username: {}, email: {}'.format(registerForm.username.data, registerForm.email.data))
        flash("New user created", 'success')
        return redirect(url_for('uploads.login'))
    return render_template('users/register.html', title="Register", form=registerForm)


@users.route('/login', methods=['GET', 'POST'])
def login():
    # Login page can only be accessed when the user is not logged in
    if current_user.is_authenticated:
        return redirect(url_for('uploads.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            if user.permLevel == Config.permissionLevels['suspended']:
                flash('Account suspended')
                return redirect(url_for('users.login'))
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash('Logged in')
            logger.log.info('User with id {} logged in'.format(current_user.id))
            return redirect(next_page) if next_page else redirect(url_for('uploads.home'))
        else:
            flash('Login unsuccessful, Please check email and password')
    return render_template('users/login.html', form=form)


@users.route('/logout')
def logout():
    logger.log.info('User with id {} logged out'.format(current_user.id))
    logout_user()
    flash('Logged out')
    return redirect(url_for('uploads.home'))
