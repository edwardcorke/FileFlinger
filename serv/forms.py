from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from serv import db, models
from serv.models import User


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
    submit = SubmitField('Submit upload')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    submit = SubmitField('Login')

    # def search_user_by_email(self, email):
    #     user = User.query.filter_by(email=email.data).first()
    #     if user is None:
    #         raise ValidationError('No user found with that email')
