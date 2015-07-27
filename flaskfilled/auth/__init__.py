from flask import Blueprint
from flask.ext.principal import Permission, RoleNeed

auth = Blueprint('auth', __name__)

from . import views

admin_permission = Permission(RoleNeed('admin'))
