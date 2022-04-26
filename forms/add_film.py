from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired


class AddFilmForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    genres = StringField('Жанры', validators=[DataRequired()])
    festival = StringField('Название фестиваля', validators=[DataRequired()])
    submit = SubmitField('Создать')
