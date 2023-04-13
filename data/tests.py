import sqlalchemy
from data.db import Base
from sqlalchemy import orm


class Test(Base):

    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    content = sqlalchemy.Column(sqlalchemy.String)
    categories = orm.relationship("Category", secondary="Categories_to_Tests", backref="tests")







