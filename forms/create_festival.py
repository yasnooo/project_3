from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField
from wtforms.validators import DataRequired


class CreateFestivalForm(FlaskForm):
    title = StringField('Название', validators=[DataRequired()])
    description = StringField('Описание', validators=[DataRequired()])
    genres = StringField('Жанры фестиваля', validators=[DataRequired()])
    start_date = DateField('Дата начала (формат: год-месяц-день)', validators=[DataRequired()])
    end_date = DateField('Дата конца (формат: год-месяц-день)', validators=[DataRequired()])
    submit = SubmitField('Создать')
