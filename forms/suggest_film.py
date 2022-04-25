from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired


class SuggestFilmForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    submit = SubmitField('Предложить')