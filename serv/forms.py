from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class ExampleForm(FlaskForm):
    name = StringField('name',
                       validators=[DataRequired(),
                                           Length(min=2, max=30)])
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    submit = SubmitField('Submit form')
