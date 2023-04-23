import json
from werkzeug.security import generate_password_hash

from data.users import User
from data.tests import Test
from data.categories import Category
from data.results import Result
from data.db import db_session as db


class DataBase:

    @staticmethod
    def get_completed_tests_by_id(id):
        user = User.query.filter(User.id == id).first()
        completed_tests = list()
        for res in user.completed_tests:
            completed_test = Test.query.filter(Test.id == res.test_id).first()
            info = Test().to_json_for_results(completed_test)
            author_login = DataBase().get_login_by_id(info['author'])
            info['author_login'] = author_login
            info['result'] = res.result
            completed_tests.append(info)
        completed_tests = sorted(completed_tests, key=lambda t: t['id'])
        return completed_tests

    @staticmethod
    def get_login_by_id(id):
        user = User.query.filter(User.id == id).first()
        return user.login

    @staticmethod
    def get_test_by_id(id):
        test = Test.query.filter(Test.id == id).first()
        return Test().to_json(test)

    @staticmethod
    def get_tests_by_author_id(id):
        tests = Test.query.all()
        tests_to_return = list()
        for test in tests:
            if test.author == id:
                tests_to_return.append(Test().to_json(test))
        return tests_to_return

    @staticmethod
    def get_user_by_login(login):
        return User.query.filter(User.login == login).first()

    @staticmethod
    def get_user_by_id(id):
        return User.query.filter(User.id == id).first()

    @staticmethod
    def get_categories():
        return Category.query.all()

    @staticmethod
    def get_tests(category=None):
        tests = Test.query.all()
        tests_to_return = list()
        if not category:
            for test in tests:
                tests_to_return.append(Test().to_json(test))
        else:
            for test in tests:
                categories = [c.name for c in test.categories]
                if category in categories:
                    tests_to_return.append(Test().to_json(test))
        return tests_to_return

    @staticmethod
    def get_result_by_id(id):
        return Result.query.filter(Result.id == id).first()

    @staticmethod
    def add_new_user(login, password):
        user = User()
        user.login = login
        user.password = password
        db.add(user)
        db.commit()

    @staticmethod
    def add_result(test_id, user_id, result):
        res = Result()
        res.test_id = test_id
        if 'points' in result:
            res.result = f"{result['points']}/{result['max_points']}. {result['result']}"
        else:
            res.result = result['result']
        db.add(res)
        db.commit()
        user = User.query.filter(User.id == user_id).first()
        user.completed_tests.append(res)
        db.commit()
        return res.id

    @staticmethod
    def set_names_to_authors_in_test(tests_without_author):
        tests = []
        for test in tests_without_author:
            if test['approved']:
                test['author'] = DataBase().get_login_by_id(test['author'])
                tests.append(test)
        return tests

    @staticmethod
    def offer_test(author_id, offered_test, results):
        new_test = Test()
        new_test.name = offered_test['test_name']
        new_test.author = author_id
        new_test.with_points = 1 if 'with_points' in offered_test else 0
        new_test.approved = 0
        content = []
        new_question = {}
        for key in offered_test:
            if 'question' in key:
                if new_question:
                    content.append(new_question)
                new_question = {}
                number = int(key[8:])
                new_question['number'] = number
                question = offered_test[key]
                new_question['question'] = question
                new_question['answers'] = {}
            if 'answer' in key:
                answer = offered_test[key]
            if 'score' in key:
                new_question['answers'][answer] = int(offered_test[key])
        content.append(new_question)
        new_test.content = json.dumps(content)
        offered_results = dict()
        for score, r in results:
            offered_results[score] = r
        new_test.results = json.dumps(offered_results)

        db.add(new_test)
        db.commit()
        user = DataBase().get_user_by_id(author_id)
        user.offered_tests.append(new_test)
        db.commit()

    @staticmethod
    def search_test(string):
        tests = DataBase().get_tests()
        required_tests = list()
        words_in_string = string.split()
        for test in tests:
            if string in test['name'].lower():
                required_tests.insert(0, test)
            else:
                for word in words_in_string:
                    if word in test['name']:
                        required_tests.append(test)
        return required_tests


def add_test_info():
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
    test.content = json.dumps([{'number': 1,
                                'question': 'Как говорит кошка?',
                                'answers': {'гав': 0, 'мяууу': 0, 'Кошки не говорят!': 1}},
                               {'number': 2,
                                'question': 'На каждой ветке березы растет по три яблока, всего веток 7. Сколько яблок растет на березе?',
                                'answers': {'21': 0, '7': 0, 'На березе яблоки не растут!': 1}}])
    test.with_points = 1
    test.results = json.dumps({'0': 'Да Вы гуманитарий!',
                               '1': 'В вас есть потенциал математика!',
                               '2': 'Вы - профи в логике!'})
    cat = Category()
    cat.name = 'Logic'
    cat1 = Category()
    cat1.name = 'Math'
    res = Result()
    res.result = '8/10'
    res.test_id = 1
    user1.completed_tests.append(res)
    test.categories.append(cat)
    db.add(test)
    db.add(user1)
    db.add(user2)
    db.add(user3)
    db.add(cat)
    db.add(cat1)
    db.commit()
    DataBase().get_login_by_id(1)
    DataBase().get_tests('Logic')


def add_test():
    test = Test()
    test.name = 'Animal'
    test.author = 3
    test.content = json.dumps([{'number': 1,
                                'question': 'Вы любите кошек?',
                                'answers': {'нет': 0, 'да': 1}},
                               {'number': 2,
                                'question': 'А собак?',
                                'answers': {'нет': 1, 'да': 0}},
                                {'number': 3,
                                 'question': 'А кого больше?',
                                 'answers': {'кошек': 1, 'собак': 0}}])
    test.results = json.dumps({'3': 'Вы - чистый кошатник!',
                               '2': 'Вы любите кошечек, но не против собак!',
                               '1': 'Собаки ближе Вашему сердцу, но Вы не против кошек!',
                               '0': 'Вы - чистый любитель милых пёсиков!'})
    db.add(test)
    db.commit()
