from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from serv import db, models
from serv.models import User
import re as regex


class UploadFile(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    message = StringField('Message', validators=[Length(max=512)])
    expirationLength = SelectField('Expiration_Duraction',
                                   validators=[DataRequired()],
                                   coerce=int,
                                   default=30,
                                   choices=[(30, "30 days"),
                                            (14, "14 days"),
                                            (7, "7 days"),
                                            (5, "5 days"),
                                            (2,"2 days"),
                                            (1,"1 day")],)
    password = PasswordField('Password', validators=[Length(max=64)])
    submit = SubmitField('Submit upload')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(max=256)])
    password = PasswordField('Password', validators=[DataRequired(), Length(max=256)])
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')

    def validate_email(self, email):
        user = User.query.filter_by(username=email.data).first()
        if user:
            raise ValidationError('Email already taken')

    def validate_password(form, field):
        """
        Validates the given password against a predefined list of rules
        as defined by the specification
        :param form: Form object to validate
        :param field: Specific field to validate
        :return: None or raises a ValidationError
        """
        password = field.data
        for x in range(len(password)):
            if len(password) < 8:
                raise ValidationError('Password not long enough')
            if len(password) > 64:
                raise ValidationError('Password too long')
            elif not regex.search("[a-z]", password):
                raise ValidationError('Password does not contain any lowercase characters')
            elif not regex.search("[A-Z]", password):
                raise ValidationError('Password does not contain any uppercase characters')
            elif not regex.search("[0-9]", password):
                raise ValidationError('Password does not contain any numbers')
            elif not regex.search("[{(_@$%&~#£*^?!)}]", password):
                raise ValidationError('Password does not contain any (valid) symbols')
            elif regex.search("\s", password):
                raise ValidationError('Password contains whitespace')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    submit = SubmitField('Login')

    # def search_user_by_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError('No user found with that email')


class DownloadPasswordForm(FlaskForm):
    password = PasswordField('Password')
    submit = SubmitField('start download')
