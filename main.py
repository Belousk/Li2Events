from flask import Flask, render_template, redirect
from requests import post, get, put
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from api import users_api
from data.__all_models import User, Event
from data.db_session import create_session, global_init
from form.login import LoginForm
from form.profile import ProfileForm
from form.user import RegisterForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.debug = True
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    db_sess = create_session()
    events = db_sess.query(Event).all()
    return render_template('index.html', title='Главная', current_user=current_user, events=events)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")

        if not form.email.data.endswith('@litsey2.ru'):
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Извините, но эти мероприятия только для учеников ЛИ2")

        users = get(f'http://localhost:5000/api/users/{current_user.id}').json()['user']
        if list(filter(lambda item: item['email'] == user['email'], users))[0]:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Почта занята. Может у вас уже есть аккаунт")

        post('http://localhost:5000/api/users', json={
            "name": form.name.data,
            "surname": form.surname.data,
            "email": form.email.data,
            "password": form.password.data
        })
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    db_sess = create_session()
    user = db_sess.query(User).get(user_id)
    return user


@app.route('/login', methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")

        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)

    return render_template('login.html', title='Авторизация', form=form)


@app.route('/event/<int:event_id>/quit')
@login_required
def quit_event(event_id):
    db_sess = create_session()
    event = db_sess.query(Event).get(event_id)
    user = db_sess.query(User).get(current_user.id)
    event.users.remove(user)
    db_sess.merge(user)
    db_sess.merge(event)
    db_sess.commit()
    return redirect('/')


@app.route('/event/<int:event_id>/join')
@login_required
def join_event(event_id):
    db_sess = create_session()
    event = db_sess.query(Event).get(event_id)
    user = db_sess.query(User).get(current_user.id)
    event.users.append(user)
    db_sess.merge(event)
    db_sess.merge(user)
    db_sess.commit()
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/profile', methods=['POST', 'GET'])
@login_required
def profile():
    form = ProfileForm()
    user = get(f'http://localhost:5000/api/users/{current_user.id}').json()['user']

    if form.validate_on_submit():
        users = get('http://localhost:5000/api/users').json()['users']

        if list(filter(lambda item: item['email'] == form.email.data, users)) and user['email'] != form.email.data:
            return render_template('edit_profile.html', title='Профиль',
                                   form=form,
                                   message="Такой email уже используется другим пользователем")

        if not form.email.data.endswith('@litsey2.ru'):
            return render_template('edit_profile.html', title='Профиль',
                                   form=form,
                                   message="Извините, но эти мероприятия только для учеников ЛИ2")

        put(f'http://localhost:5000/api/users/{current_user.id}', json={
            "name": form.name.data,
            "surname": form.surname.data,
            "email": form.email.data,
        })

        return redirect('/')
    form.name.data = user['name']
    form.surname.data = user['surname']
    form.email.data = user['email']

    return render_template('edit_profile.html', title='Профиль', form=form)


def main():
    global_init('db/data.sqlite')
    app.register_blueprint(user_api.blueprint)
    app.run()


if __name__ == '__main__':
    main()
