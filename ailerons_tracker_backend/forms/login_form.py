
from flask_wtf import FlaskForm
from wtforms import PasswordField, validators


class LoginForm(FlaskForm):
    password = PasswordField("Mot de passe:", [validators.data_required()])
