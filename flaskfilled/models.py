from werkzeug.security import generate_password_hash, check_password_hash

from flaskfilled import db, login_manager


class Cookie(db.Model):
    __tablename__ = 'cookies'

    cookie_id = db.Column(db.Integer(), primary_key=True)
    cookie_name = db.Column(db.String(50), index=True)
    cookie_recipe_url = db.Column(db.String(255))
    quantity = db.Column(db.Integer())


class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))
    password_hash = db.Column(db.String(255))
    authenticated = db.Column(db.Boolean, default=False)

    def is_active(self):
        return True

    def get_id(self):
        return self.user_id

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

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
