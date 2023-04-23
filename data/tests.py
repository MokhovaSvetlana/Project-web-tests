import sqlalchemy
from .db import Base
from sqlalchemy import orm
import json


association_table_offered_tests = sqlalchemy.Table(
    'OfferedTests',
    Base.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class Test(Base):
    '''Structure of content: list of questions (dicts):
        [
        {
         'number': <type int, number of question>,
         'question': <type string, question>,
         'answers': {'answer <text of answer>': points <type int>,
                     '...': ...},
         },
         {...}]'''

    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    content = sqlalchemy.Column(sqlalchemy.String)
    categories = orm.relationship("Category", secondary="Categories_to_Tests", backref="tests")
    with_points = sqlalchemy.Column(sqlalchemy.Boolean, default=0)
    results = sqlalchemy.Column(sqlalchemy.String)
    approved = sqlalchemy.Column(sqlalchemy.Boolean, default=1)

    def to_json(self, test):
        '''return dict of title, author_id and questions'''
        return {'id': test.id, 'name': test.name, 'author': test.author, 'questions': json.loads(test.content),
                'with_points': test.with_points, 'results': test.results, 'approved': test.approved,
                'categories': ', '.join([cat.name for cat in test.categories])}

    def to_json_for_results(self, test):
        return {'id': test.id, 'name': test.name, 'author': test.author}
