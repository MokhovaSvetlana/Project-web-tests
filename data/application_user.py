import functools
from flask import Blueprint
from flask import session
from flask import g
from flask import render_template, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import LoginForm, RegisterForm
from database import DataBase
from .users import User

bp = Blueprint("user", __name__)


def login_required(view):

    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect("/")
        return view(**kwargs)

    return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id == user_id).first()


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = DataBase().get_user_by_login(form.login.data)
        if user and check_password_hash(user.password, form.password.data):
            session.clear()
            session["user_id"] = user.id
            return redirect("/alltests")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect("/")


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == "POST":
        if form.password.data != form.repeat_password.data:
            return render_template('register.html', title='Авторизация', form=form,
                                   message="Пароли не совпадают")
        elif DataBase().get_user_by_login(form.login.data):
            return render_template('register.html', title='Авторизация', form=form,
                                   message="Этот логин уже используется")
        DataBase().add_new_user(form.login.data, generate_password_hash(form.password.data))
        user = DataBase().get_user_by_login(form.login.data)
        session["user_id"] = user.id
        return redirect("/alltests")
    return render_template('register.html', title='Регистрация', form=form)
