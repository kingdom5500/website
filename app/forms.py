from flask_wtf import FlaskForm
from wtforms.fields import TextField, TextAreaField
from wtforms.validators import Length, DataRequired


class PostForm(FlaskForm):
    name = TextField('name', validators=[Length(max=32)])
    message = TextAreaField('message', validators=[Length(max=2048), DataRequired()])