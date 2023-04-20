import sqlalchemy
from .db import Base


class Result(Base):

    __tablename__ = 'results'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    result = sqlalchemy.Column(sqlalchemy.String)
    test_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('tests.id'))