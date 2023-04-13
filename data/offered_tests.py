import sqlalchemy
from data.db import Base
from sqlalchemy import orm


association_table = sqlalchemy.Table(
    'OfferedTests_to_Users',
    Base.metadata,
    sqlalchemy.Column('offered_tests', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('offered_tests.id'))
)


class OfferedTest(Base):
    __tablename__ = 'offered_tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    categories = orm.relationship("Category", secondary="Categories_to_Offered_Tests", backref="offered_tests")
    status = sqlalchemy.Column(sqlalchemy.String, default='Ожидание проверки')
