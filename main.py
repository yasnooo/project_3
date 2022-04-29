import datetime
from kinopoisk_api import KP
from flask import Flask, render_template, redirect, request, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data import db_session
from data.users import User
from data.films import Films
from data.festivals import Festival
from forms.login import LoginForm
from forms.register import RegisterForm
from forms.create_festival import CreateFestivalForm
from forms.suggest_film import SuggestFilmForm
from forms.add_film import AddFilmForm

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'rainer_sit_down'
kinopoisk = KP(token='707d0842-b312-41ee-9529-bddf754af883')


def main():
    db_session.global_init("db/films_base.db")
    app.run()


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/main_page')
def main_page():
    db_sess = db_session.create_session()
    user = db_sess.query(User).all()
    return render_template('main_page.html', user=user)


@app.route("/")
def index():
    db_sess = db_session.create_session()
    festival = db_sess.query(Festival).filter(datetime.date.today() <= Festival.end_date).first()
    if festival:
        films = db_sess.query(Films).filter(Films.festival_id == festival.id).all()
    else:
        films = None
    return render_template("index.html", fest=festival, films=films)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            surname=form.surname.data,
            date_of_birth=form.date_of_birth.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/create_festival', methods=['GET', 'POST'])
def create_festival():
    form = CreateFestivalForm()
    if form.validate_on_submit():
        if form.start_date.data >= form.end_date.data:
            return render_template('create_festival.html', title='Новый фестиваль',
                                   form=form,
                                   message="Дата начала должна быть раньше даты окончания")
        if form.start_date.data <= datetime.date.today():
            return render_template('create_festival.html', title='Новый фестиваль',
                                   form=form,
                                   message="Извените, но у нас нет машины времени ¯\_(ツ)_/¯")
        db_sess = db_session.create_session()
        if db_sess.query(Festival).filter(Festival.end_date >= form.start_date.data).first():
            return render_template('create_festival.html', title='Новый фестиваль',
                                   form=form,
                                   message="На эту дату уже запланированн фестиваль")
        festival = Festival(
            title=form.title.data,
            description=form.description.data,
            genres=form.genres.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data
        )
        db_sess.add(festival)
        db_sess.commit()
        return redirect('/')
    return render_template('create_festival.html', title='Новый фестиваль', form=form)


@app.route('/add_film', methods=['GET', 'POST'])
def add_film():
    form = AddFilmForm()
    db_sess = db_session.create_session()
    if form.validate_on_submit():
        if form.festival.data != db_sess.query(Festival).filter(
                datetime.date.today() <= Festival.end_date).first().title():
            return render_template('reg_film.html', title='Новый фильм',
                                   form=form,
                                   message="Такого фестиваля нет")
        try:
            film = kinopoisk.search(form.title)
        except Exception:
            return render_template('reg_film.html', title='Новый фильм',
                                   form=form,
                                   message="Мы не нашли такого фильма. Возможно вы неправильно ввели название.")
        film = Films(
            kinopoisk_id=film.kp_id,
            festival_id=db_sess.query(Festival).filter(datetime.date.today() <= Festival.end_date).first().id(),
            title=film.name,
        )
        db_sess.add(film)
        db_sess.commit()
        return redirect('/')
    return render_template('reg_film.html', title='Новый фестиваль', form=form)


@app.route('/suggest_film', methods=['GET', 'POST'])
def suggest_film():
    form = SuggestFilmForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()

        return redirect('/')
    return render_template('suggest_film.html', title='Предложить фильм', form=form)


@app.route('/show/<film_name>')
def show(film_name):
    pass


if __name__ == '__main__':
    main()
