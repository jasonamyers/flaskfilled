from flask import render_template

from . import main
from flaskfilled.auth import admin_permission


@main.route('/', methods=['GET'])
def index():
    return render_template('main/index.html')


@main.route('/settings', methods=['GET'])
@admin_permission.require()
def settings():
    return render_template('main/settings.html')
