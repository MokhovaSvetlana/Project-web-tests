import sqlalchemy
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Test(SqlAlchemyBase):

    __tablename__ = 'tests'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=False, nullable=False)
    author = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('users.id'))
    content = sqlalchemy.Column(sqlalchemy.String)
    categories = orm.relationship("Category", secondary="Categories_to_Tests", backref="tests")







