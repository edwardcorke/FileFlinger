from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class UploadFile(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(),
                                    Email()])
    message = StringField('Message', validators=[Length(max=512)])
    submit = SubmitField('Submit upload')
