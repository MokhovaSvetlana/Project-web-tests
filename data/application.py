from flask import render_template, redirect, request
from werkzeug.security import generate_password_hash, check_password_hash
from data.forms import LoginForm, RegisterForm
from flask import g
from data.users import User
from flask import Blueprint
from data.db import db_session as db
from flask import session
import functools
from database import DataBase


bp = Blueprint("main", __name__)


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


@bp.route("/")
def index():
    return render_template("main.html", title="Главная")


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
        user = User()
        user.login = form.login.data
        user.password = generate_password_hash(form.password.data)
        db.add(user)
        db.commit()
        session["user_id"] = user.id
        return redirect("/alltests")
    return render_template('register.html', title='Регистрация', form=form)


@bp.route("/userpage")
def user_page():
    tests = []
    for test in DataBase().get_tests_by_author_id(g.user.id):
        test['author'] = DataBase().get_login_by_id(test['author'])
        tests.append(test)
    return render_template("user_page.html", title="Личная страница",
                           user_tests=tests)


@bp.route("/alltests")
@bp.route("/alltests/<category>")
def all_tests(category=None):
    tests = []
    for test in DataBase().get_tests(category):
        test['author'] = DataBase().get_login_by_id(test['author'])
        tests.append(test)
    return render_template("all_tests.html", tests=tests,
                           categories=DataBase().get_categories(), title="Все тесты")


@bp.route("/selectcategory")
def select_category():
    return render_template("select_category.html", categories=DataBase().get_categories(),
                           title="Выберите категорию")


@bp.route("/dotest/<test_id>", methods=['GET', 'POST'])
def do_test(test_id):
    if request.method == "POST":
        print(request.form)
    return render_template("do_test.html", test=DataBase().get_test_by_id(id=test_id),
                           title="Прохождение теста")


@bp.route("/resulttes/<all_score>/<score>")
def result_test(all_score, score):
    return render_template("result_test.html", all_score=all_score, score=score)

