import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


association_table = sqlalchemy.Table(
    'CompletedTests_to_Users',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('tests.id')),
    sqlalchemy.Column('tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('result', sqlalchemy.String)
)


class User(SqlAlchemyBase):

    __tablename__ = 'users'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    login = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    completed_tests = orm.relationship("Test", secondary="CompletedTests_to_Users", backref="users")
    offered_tests = orm.relationship("OfferedTest", secondary="OfferedTests_to_Users", backref="users")
