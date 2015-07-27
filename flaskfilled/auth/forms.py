from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required, Length


class LoginForm(Form):
        username = StringField('username', validators=[Required(),
                                                       Length(1, 64)])
        password = PasswordField('Password', validators=[Required()])
        submit = SubmitField('Log In')
