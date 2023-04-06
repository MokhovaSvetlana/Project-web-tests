# from flask import Flask
from data import db_session
from data.users import User
from data.tests import Test
from data.categories import Category
import json
from pprint import pprint


# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'



    # db_sess.commit()


class DataBase:

    # not ready
    @staticmethod
    def get_completed_tests_by_id(id):   # return names of tests and results (list of dicts?)
        db_session.global_init("db/tests.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        tests = list()
        print(user.completed_tests[0].result)  # --- результат???
            # tests.append({'title': test.name,
            #               'result': test.r})
        # data = json.loads(test.content)
        # return data

    @staticmethod
    def get_login_by_id(id):
        db_session.global_init("db/tests.db")
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.id == id).first()
        return user.login

    # not ready
    @staticmethod
    def get_offered_tests_by_id(id):   # return tests and statuses (list of dicts?)
        pass

    @staticmethod
    def get_tests(category=None):
        db_session.global_init("db/tests.db")
        db_sess = db_session.create_session()
        tests = db_sess.query(Test).all()
        tests_to_return = list()
        if not category:
            for test in tests:
                tests_to_return.append({'title': test.name,
                                        'author': test.author,
                                        'questions': json.loads(test.content)})
        else:
            for test in tests:
                categories = [c.name for c in test.categories]
                if category in categories:
                    tests_to_return.append({'title': test.name,
                                            'author': test.author,
                                            'questions': json.loads(test.content)})
        return tests_to_return


def main():
    db_session.global_init("db/tests.db")
    # user1 = User()
    # user1.login = 'Voldemort'
    # user1.password = 'Forever_and_ever'
    # user2 = User()
    # user2.login = 'Harry_Potter'
    # user2.password = 'Gold_Boy'
    # user3 = User()
    # user3.login = 'Hermiona'
    # user3.password = 'LoveBooks'

    # test = Test()
    # test.name = 'First Test'
    # test.author = 1
    # test.content = json.dumps([{'number': 1, 'question': 'Как говорит кошка?', " \
    #                "'answers': {'false': ['гав', 'ауууу', 'мяу'], 'true': 'Кошки не говорят'}},
    #                 {'number': 2, 'question': 'На каждой ветке березы растет по три яблока, всего веток 7. Сколько яблок растет на березе?',
    #                  'answers': {'false': ['21', '7'], 'true': 'На березе яблоки не растут!'}}])

    # cat = Category()
    # cat.name = 'Logic'


    # db_sess = db_session.create_session()

    # test = db_sess.query(Test).filter(Test.id == 1).first()
    # user = db_sess.query(User).filter(User.id == 1).first()
    # user.completed_tests.append(test)
    # cat = db_sess.query(Category).filter(Category.id == 1).first()
    # test.categories.append(cat)

    # db_sess.add(test)

    # db_sess.add(user1)
    # db_sess.add(user2)
    # db_sess.add(user3)

    # db_sess.add(cat)

    # db_sess.commit()

    # DataBase().get_completed_tests_by_id(1)   --- ?
    # DataBase().get_login_by_id(1)
    # DataBase().get_tests('Logic')


if __name__ == '__main__':
    main()