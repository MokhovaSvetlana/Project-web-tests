import sqlalchemy
from data.db import Base
from sqlalchemy import orm
from .offered_tests import association_table


association_table = sqlalchemy.Table(
    'CompletedTests_to_Users',
    Base.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('result', sqlalchemy.String)
)


class User(Base):

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    completed_tests = orm.relationship("Test", secondary="CompletedTests_to_Users", backref="users")
    offered_tests = orm.relationship("OfferedTest", secondary="OfferedTests_to_Users", backref="users")
