from flask import render_template, redirect, request, url_for
from flask import g
from flask import Blueprint
from .checking_results import checking_results
from .checking_creating_test import do_result_table

from database import DataBase
from data.application_user import login_required


bp = Blueprint("tests", __name__)


@bp.route("/")
def index():
    return render_template("main.html", title="Главная")


@bp.route("/alltests", methods=['GET', 'POST'])
@bp.route("/alltests/<category>", methods=['GET', 'POST'])
@login_required
def all_tests(category=None):
    if request.method == "POST":
        string = request.form['string']
        if string:
            tests = DataBase.set_names_to_authors_in_test(DataBase().search_test(string))
            return render_template("all_tests.html", tests=tests, title=f"Тесты по запросу: {string}")

    tests = DataBase.set_names_to_authors_in_test(DataBase().get_tests(category))
    return render_template("all_tests.html", tests=tests, title="Все тесты")


@bp.route("/selectcategory")
@login_required
def select_category():
    return render_template("select_category.html", categories=DataBase().get_categories(),
                           title="Выберите категорию")


@bp.route("/dotest/<test_id>", methods=['GET', 'POST'])
@login_required
def do_test(test_id):
    if request.method == "POST":
        answers = [str(request.form[ix]).split("||")[1] for ix in request.form]
        result_of_user = checking_results(DataBase().get_test_by_id(id=test_id), answers)
        res_id = DataBase().add_result(test_id, g.user.id, result_of_user)
        return redirect(url_for('tests.result_test', res_id=res_id))
    return render_template("do_test.html", test=DataBase().get_test_by_id(id=test_id),
                           title="Прохождение теста")


@bp.route("/resulttest/<res_id>")
@login_required
def result_test(res_id):
    if "/" in DataBase().get_result_by_id(res_id).result:
        points = DataBase().get_result_by_id(res_id).result.split(". ")[0]
        result = DataBase().get_result_by_id(res_id).result[len(points) + 2:]
        user_points, all_points = points.split("/")
    else:
        result = DataBase.get_result_by_id(res_id).result
        user_points, all_points = '', ''
    return render_template("result_test.html", result=result, score=user_points, all_score=all_points)


@bp.route("/userpage")
@login_required
def user_page():
    tests = []
    for test in DataBase().get_tests_by_author_id(g.user.id):
        test['author'] = DataBase().get_login_by_id(test['author'])
        tests.append(test)
    completed_tests = DataBase().get_completed_tests_by_id(g.user.id)
    return render_template("user_page.html", title="Личная страница",
                           user_tests=tests, completed_tests=completed_tests)


@bp.route("/creatingtest", methods=['GET', 'POST'])
@login_required
def creating_test():
    if request.method == "POST":
        try:
            DataBase().offer_test(g.user.id, request.form, do_result_table(request.form))
        except ValueError:
            return render_template("creating_test.html", title="Создание теста",
                                   message="Не назначены баллы в вопросах или результатах ")
        return redirect(url_for('tests.test_sent'))
    return render_template("creating_test.html", title="Создание теста")


@bp.route("/testsent")
def test_sent():
    return render_template("test_sent.html", title="Тест отправлен")


@bp.route("/approvingtests")
def approving_tests():
    tests = DataBase().set_names_to_authors_in_test(DataBase().get_disapproved_tests())
    return render_template("approving_tests.html", tests=tests, title="Одобрить тесты")


@bp.route("/approvetest/<test_id>")
def approve_test(test_id):
    DataBase().approve_test(test_id)
    return redirect(url_for('tests.approving_tests'))
