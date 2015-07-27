from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.login import UserMixin, current_user
from flask.ext.principal import identity_loaded, RoleNeed, UserNeed

from flaskfilled import db, login_manager


class Cookie(db.Model):
    __tablename__ = 'cookies'

    cookie_id = db.Column(db.Integer(), primary_key=True)
    cookie_name = db.Column(db.String(50), index=True)
    cookie_recipe_url = db.Column(db.String(255))
    quantity = db.Column(db.Integer())


roles_users = db.Table('roles_users',
                       db.Column('user_id', db.Integer(),
                                 db.ForeignKey('users.user_id')),
                       db.Column('role_id', db.Integer(),
                                 db.ForeignKey('roles.id')))


class Role(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, default=False)
    roles = db.relationship('Role', secondary=roles_users,
                            primaryjoin=user_id == roles_users.c.user_id,
                            backref='users')

    def get_id(self):
        return self.user_id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(userid):
    return User.query.get(userid)


@identity_loaded.connect
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))
