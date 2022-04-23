from flask import Flask, render_template, redirect
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from data.__all_models import User, Event
from data.db_session import create_session, global_init
from form.login import LoginForm
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
        db_sess = create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User()
        user.name = form.name.data
        user.surname = form.surname.data
        user.email = form.email.data
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
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
    event.users.remove(current_user)
    db_sess.merge(current_user)
    db_sess.merge(event)
    db_sess.commit()
    return redirect('/')


@app.route('/event/<int:event_id>/join')
@login_required
def join_event(event_id):
    db_sess = create_session()
    event = db_sess.query(Event).get(event_id)
    event.users.append(current_user)
    db_sess.merge(event)
    db_sess.merge(current_user)
    db_sess.commit()
    return redirect('/')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


def main():
    global_init('db/data.sqlite')
    app.run()


if __name__ == '__main__':
    main()
