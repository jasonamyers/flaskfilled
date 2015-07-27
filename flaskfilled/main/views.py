from flask import render_template
from flask_mail import Message

from . import main
from flaskfilled.auth import admin_permission


@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route('/settings', methods=['GET'])
@admin_permission.require()
def settings():
    return render_template('main/settings.html')


@main.route('/mailme', methods=['GET'])
def mail():
    msg = Message('COOKIES!',
                  sender='from@example.com',
                  recipients=['to@example.com'])
    msg.body = 'There all mine!'
    msg.html = '<b>There all mine!</b>'
    mail.send(msg)
