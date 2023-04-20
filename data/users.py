import sqlalchemy
from .db import Base
from sqlalchemy import orm
from .tests import association_table_offered_tests


association_table_results = sqlalchemy.Table(
    'Results_of_CompletedTests',
    Base.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('results.id')),
    sqlalchemy.Column('results', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id'))
)


class User(Base):

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    completed_tests = orm.relationship("Result", secondary="Results_of_CompletedTests", backref="users")
    offered_tests = orm.relationship("Test", secondary="OfferedTests", backref="users")