from data.users import User
from data.tests import Test
from data.categories import Category
import json
from data.db import db_session as db
from werkzeug.security import generate_password_hash


class DataBase:

    # not ready
    @staticmethod
    def get_completed_tests_by_id(id):  # return
        user = User.query.filter(User.id == id).first()
        tests = list()
        print(user.completed_tests[0].result)  # --- результат???
        # tests.append({'title': test.name,
        #               'result': test.r})
        # data = json.loads(test.content)
        # return data

    @staticmethod
    def get_login_by_id(id):
        user = User.query.filter(User.id == id).first()
        return user.login

    @staticmethod
    def get_test_by_id(id):
        test = Test.query.filter(Test.id == id).first()
        return {'id': test.id,
                'title': test.name,
                'author': test.author,
                'questions': json.loads(test.content)}

    @staticmethod
    def get_tests_by_author_id(id):
        tests = Test.query.all()
        tests_to_return = list()
        for test in tests:
            if test.author == id:
                tests_to_return.append({'id': test.id,
                                        'title': test.name,
                                        'author': test.author,
                                        'questions': json.loads(test.content)})
        return tests_to_return

    @staticmethod
    def get_user_by_login(login):
        return User.query.filter(User.login == login).first()

    @staticmethod
    def get_categories():
        return Category.query.all()

    # not ready
    @staticmethod
    def get_offered_tests_by_id(id):  # return tests and statuses (list of dicts?)
        pass

    @staticmethod
    def get_tests(category=None):
        tests = Test.query.all()
        tests_to_return = list()
        if not category:
            for test in tests:
                tests_to_return.append({'id': test.id,
                                        'title': test.name,
                                        'author': test.author,
                                        'questions': json.loads(test.content)})
        else:
            for test in tests:
                categories = [c.name for c in test.categories]
                if category in categories:
                    tests_to_return.append({'id': test.id,
                                            'title': test.name,
                                            'author': test.author,
                                            'questions': json.loads(test.content)})
        return tests_to_return


def add_info():
    user1 = User()
    user1.login = 'Voldemort'
    user1.password = generate_password_hash('Forever_and_ever')
    user2 = User()
    user2.login = 'Harry_Potter'
    user2.password = generate_password_hash('Gold_Boy')
    user3 = User()
    user3.login = 'Hermiona'
    user3.password = generate_password_hash('LoveBooks')

    test = Test()
    test.name = 'First Test'
    test.author = 1
    test.content = json.dumps([{'number': 1, 'question': 'Как говорит кошка?', 'answers': {'false': ['гав', 'ауууу', 'мяу'], 'true': 'Кошки не говорят'}},
                               {'number': 2,
                                'question': 'На каждой ветке березы растет по три яблока, всего веток 7. Сколько яблок растет на березе?',
                                'answers': {'false': ['21', '7'], 'true': 'На березе яблоки не растут!'}}])

    cat = Category()
    cat.name = 'Logic'

    user1.completed_tests.append(test)
    test.categories.append(cat)

    db.add(test)

    db.add(user1)
    db.add(user2)
    db.add(user3)

    db.add(cat)

    db.commit()

    DataBase().get_login_by_id(1)
    DataBase().get_tests('Logic')
