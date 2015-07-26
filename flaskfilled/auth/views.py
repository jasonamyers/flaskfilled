from flask import render_template, redirect, request, url_for, flash

from flask.ext.login import login_user, logout_user, login_required

from . import auth
from flaskfilled.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        password = request.form.get('password', '')
        user = User.query.filter_by(username=username).first()
        if user is not None and user.verify_password(password):
            login_user(user)
            next = request.args.get('next')
            return redirect(next or url_for('main.index'))
        else:
            flash('Wrong username or password.')
    return render_template('auth/login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
