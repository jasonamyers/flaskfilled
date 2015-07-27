from flask import (render_template, redirect, request, url_for, flash,
                   current_app)

from flask.ext.login import login_user, logout_user, login_required
from flask.ext.principal import identity_changed, Identity

from . import auth
from .forms import LoginForm
from flaskfilled.models import User


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            identity_changed.send(current_app._get_current_object(),
                                  identity=Identity(user.user_id))
            next = request.args.get('next')
            return redirect(next or url_for('main.index'))
        else:
            flash('Wrong username or password.')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))
